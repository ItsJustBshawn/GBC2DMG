import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import zlib
import converter
from build_recipe import make_delta

class ConverterTests(unittest.TestCase):
    def test_relocated_copy_and_literals(self):
        source = bytes(range(256)) * 20
        target = source[1200:2400] + b'new code' + source[:1000]
        self.assertEqual(converter.apply_delta(source, make_delta(source, target)), target)

    def test_invalid_compression(self):
        with self.assertRaises(ValueError):
            converter.apply_delta(b"source", b"not zlib")

    def test_malformed_recipes(self):
        for raw in [b'', b'D2M1L', b'D2M1C' + struct.pack('<II', 40, 100),
                    b'D2M1L' + struct.pack('<I', converter.LIMIT + 1), b'D2M1X' + struct.pack('<I', 1)]:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                converter.apply_delta(b'a', zlib.compress(raw))

    def test_approval_hash_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source, output = root/'source.gbc', root/'out.gb'
            source.write_bytes(b'original')
            patch_data = make_delta(b'original', b'converted')
            (root/'test.d2m').write_bytes(patch_data)
            entry = dict(approved=False, source_sha256=converter.digest(b'original'),
                         output_sha256=converter.digest(b'converted'), recipe='test.d2m',
                         recipe_sha256=converter.digest(patch_data))
            with patch.object(converter, 'ROOT', root):
                with self.assertRaises(ValueError): converter.convert(source, output, entry)
                entry['approved'] = True
                converter.convert(source, output, entry)
                self.assertEqual(output.read_bytes(), b'converted')

                with self.assertRaises(FileExistsError): converter.convert(source, output, entry)
                source.write_bytes(b'wrong')
                with self.assertRaises(ValueError): converter.convert(source, root/'wrong.gb', entry)
                self.assertFalse((root/'wrong.gb').exists())
                self.assertEqual(output.read_bytes(), b'converted')

    def test_testing_does_not_require_public_approval(self):
        self.assertFalse(converter.enabled({'approved': False}))
        self.assertTrue(converter.enabled({'approved': False, 'testing_enabled': True}))
        self.assertFalse(converter.enabled({'approved': False, 'testing_enabled': 'true'}))

if __name__ == '__main__': unittest.main()

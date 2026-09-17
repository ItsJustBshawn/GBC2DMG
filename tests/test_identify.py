from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import converter


def rom(revision):
    data = bytearray(512)
    data[0x134:0x13e] = b'PM_CRYSTAL'
    data[0x143] = 0xc0
    data[0x14c] = revision
    data[0x14d] = (-sum(data[0x134:0x14d])-25)&255
    data[0x14e:0x150] = (sum(data[:0x14e])+sum(data[0x150:])).to_bytes(2, 'big')
    return bytes(data)


class IdentificationTests(unittest.TestCase):
    def test_hash_wins_over_filename_and_header(self):
        source = rom(1)
        entry = dict(id='test', name='Crystal test', version='1.1', aliases=['Rev A', 'Rev 1'],
                     release='test', approved=True, source_sha256=converter.digest(source), output_sha256='0'*64)
        with tempfile.TemporaryDirectory() as tmp, patch.object(converter, 'catalog', return_value=[entry]):
            p = Path(tmp)/'claimed-v1.0.gbc'
            p.write_bytes(source)
            report = converter.identify(p)
            self.assertEqual(report['version'], '1.1')
            self.assertTrue(report['can_convert'])
            self.assertTrue(report['header_checksum_valid'])
            self.assertTrue(report['global_checksum_valid'])
            changed = bytearray(source)
            changed[-1] = 1
            p.write_bytes(changed)
            report = converter.identify(p)
            self.assertEqual(report['kind'], 'unknown')
            self.assertEqual(report['header_revision'], 1)
            self.assertFalse(report['can_convert'])

    def test_converted_rom_is_not_offered_for_reconversion(self):
        data = rom(0)
        entry = dict(id='test', name='Crystal test', version='1.0', aliases=[], release='test',
                     approved=True, source_sha256='0'*64, output_sha256=converter.digest(data))
        with tempfile.TemporaryDirectory() as tmp, patch.object(converter, 'catalog', return_value=[entry]):
            p = Path(tmp)/'output.gb'
            p.write_bytes(data)
            result = converter.identify(p)
            self.assertEqual(result['kind'], 'converted')
            self.assertFalse(result['can_convert'])

    def test_short_files_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'short.gbc'
            p.write_bytes(b'not a ROM')
            with self.assertRaises(ValueError): converter.identify(p)


if __name__ == '__main__':
    unittest.main()

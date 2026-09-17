import tempfile
import time
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

import app


class GuiTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(str(exc))
        self.root.withdraw()
        self.ui = app.ConverterApp(self.root)

    def tearDown(self):
        if hasattr(self, 'root'):
            self.root.destroy()

    def wait(self):
        deadline = time.monotonic()+5
        while self.ui.busy and time.monotonic() < deadline:
            self.root.update()
            time.sleep(.01)
        self.assertFalse(self.ui.busy, 'Worker did not finish')

    def report(self, kind='source'):
        game = self.ui.games[0]
        return dict(file='test.gbc', size_bytes=2097152, sha256=game['source_sha256'],
                    kind=kind, recognized=True, can_convert=kind=='source',
                    game=game['name'], version=game['version'], header_revision=0,
                    header_checksum_valid=True, global_checksum_valid=True)

    def test_failed_selection_cannot_reuse_previous_approved_rom(self):
        with patch.object(app, 'identify', return_value=self.report()):
            self.ui.choose('test.gbc')
            self.wait()
        self.assertFalse(self.ui.convert_button.instate(['disabled']))
        with patch.object(app, 'identify', side_effect=ValueError('Invalid ROM')):
            self.ui.choose('bad.gbc')
            self.wait()
        self.assertIsNone(self.ui.entry)
        self.assertIsNone(self.ui.report)
        self.assertTrue(self.ui.convert_button.instate(['disabled']))
        self.assertTrue(self.ui.save_button.instate(['disabled']))
        self.assertEqual(self.ui.status.get(), 'Invalid ROM')

    def test_already_converted_file_has_report_but_cannot_convert(self):
        with patch.object(app, 'identify', return_value=self.report('converted')):
            self.ui.choose('converted.gb')
            self.wait()
        self.assertTrue(self.ui.convert_button.instate(['disabled']))
        self.assertFalse(self.ui.save_button.instate(['disabled']))

    def test_conversion_worker_delivers_success_and_preserves_existing_file(self):
        with patch.object(app, 'identify', return_value=self.report()):
            self.ui.choose('test.gbc')
            self.wait()
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)/'converted.gb'
            def convert(source, destination, entry):
                with Path(destination).open('xb') as f:
                    f.write(b'test')
                return 'a'*64
            with patch.object(app, 'convert', side_effect=convert):
                self.ui.run_conversion(dest)
                self.assertTrue(self.ui.choose_button.instate(['disabled']))
                self.wait()
                self.assertTrue(self.ui.status.get().startswith('Converted and verified:'))
                self.ui.run_conversion(dest)
                self.wait()
                self.assertIn('already exists', self.ui.status.get())
                self.assertEqual(dest.read_bytes(), b'test')


if __name__ == '__main__':
    unittest.main()

"""Plain Tk interface for local ROM conversion."""
from pathlib import Path
import json
import queue
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from converter import catalog, convert, identify

APP_VERSION = '0.4-beta.2'


class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.games = catalog()
        self.source = self.entry = self.report = None
        self.busy = False
        self.results = queue.Queue()
        root.title('GBC2DMG')
        root.geometry('600x235')
        root.minsize(480, 235)
        panel = ttk.Frame(root, padding=18)
        panel.pack(fill='both', expand=True)
        ttk.Label(panel, text='ROM file').pack(anchor='w')
        self.filename = tk.StringVar(value='No file selected')
        ttk.Entry(panel, textvariable=self.filename, state='readonly').pack(fill='x', pady=(5, 12))
        buttons = ttk.Frame(panel)
        buttons.pack(fill='x')
        self.choose_button = ttk.Button(buttons, text='Choose ROM…', command=self.choose)
        self.choose_button.pack(side='left')
        self.convert_button = ttk.Button(buttons, text='Convert…', command=self.run_conversion, state='disabled')
        self.convert_button.pack(side='left', padx=8)
        self.save_button = ttk.Button(buttons, text='Save report…', command=self.save_report, state='disabled')
        self.save_button.pack(side='left')
        self.status = tk.StringVar(value='Choose a ROM to check whether it is supported.')
        self.status_label = ttk.Label(panel, textvariable=self.status, wraplength=560)
        self.status_label.pack(anchor='w', fill='x', pady=(15, 8))
        ttk.Label(panel, text='Crystal clock: runs during play; pauses when powered off.').pack(side='bottom', anchor='w')
        panel.bind('<Configure>', lambda e: self.status_label.configure(wraplength=max(200, e.width-36)))
        root.bind('<Control-o>', lambda e: self.choose())
        root.protocol('WM_DELETE_WINDOW', self.close)
        root.after(60, self._poll)

    def close(self):
        if self.busy:
            self.status.set('Please wait for the file operation to finish before closing.')
        else:
            self.root.destroy()

    def _set_busy(self, busy):
        self.busy = busy
        self.choose_button.configure(state='disabled' if busy else 'normal')
        self.convert_button.configure(state='normal' if self.entry and not busy else 'disabled')
        self.save_button.configure(state='normal' if self.report and not busy else 'disabled')

    def _job(self, kind, function):
        self._set_busy(True)
        def work():
            try:
                result = function()
            except Exception as exc:
                self.results.put((kind, None, exc))
            else:
                self.results.put((kind, result, None))
        threading.Thread(target=work, daemon=True).start()

    def _poll(self):
        try:
            kind, result, error = self.results.get_nowait()
        except queue.Empty:
            pass
        else:
            self._set_busy(False)
            if error:
                self.status.set('That filename already exists. Choose a new name.' if isinstance(error, FileExistsError) else str(error))
            elif kind == 'identify':
                self._show_report(*result)
            else:
                destination, sha = result
                self.status.set('Converted and verified: '+destination.name)
        self.root.after(60, self._poll)

    def choose(self, path=None):
        if self.busy:
            return
        path = path or filedialog.askopenfilename(parent=self.root, title='Choose a ROM', filetypes=[('Game Boy ROMs', '*.gbc *.gb'), ('All files', '*.*')])
        if not path:
            return
        self.source = self.entry = self.report = None
        self.filename.set(Path(path).name)
        self.status.set('Checking ROM…')
        self._job('identify', lambda: (Path(path), identify(path)))

    def _show_report(self, path, report):
        self.source, self.report = path, report
        self.entry = next((g for g in self.games if g['source_sha256'] == report['sha256']), None) if report['can_convert'] else None
        if self.entry:
            self.status.set('Supported: '+report['game'])
        elif report['kind'] == 'converted':
            self.status.set('Already converted: '+report['game'])
        else:
            self.status.set('Not supported. This ROM does not match a supported version.')
        self._set_busy(False)

    def save_report(self):
        if self.busy or not self.report:
            return
        path = filedialog.asksaveasfilename(parent=self.root, initialfile='rom-version.json', defaultextension='.json', filetypes=[('Version report', '*.json')])
        if path:
            try:
                Path(path).write_text(json.dumps(self.report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
            except OSError as exc:
                messagebox.showerror('Could not save report', str(exc), parent=self.root)

    def run_conversion(self, destination=None):
        if self.busy or not self.entry:
            return
        path = destination or filedialog.asksaveasfilename(parent=self.root, title='Save DMG copy', initialfile=self.source.stem+' - DMG.gb', defaultextension='.gb', filetypes=[('Game Boy ROM', '*.gb')])
        if not path:
            return
        source, entry, destination = self.source, self.entry, Path(path)
        self.status.set('Converting…')
        self._job('convert', lambda: (destination, convert(source, destination, entry)))


def main():
    if sys.version_info < (3, 11):
        raise SystemExit('GBC2DMG needs Python 3.11 or newer.')
    root = tk.Tk()
    app = ConverterApp(root)
    if len(sys.argv) == 2:
        root.after(100, lambda: app.choose(sys.argv[1]))
    root.mainloop()


if __name__ == '__main__':
    main()

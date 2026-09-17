"""Desktop ROM identification and conversion. No network access."""
from pathlib import Path
import json
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from converter import catalog, convert, identify


def main():
    root = tk.Tk()
    root.title('GBC2DMG')
    root.geometry('820x720')
    root.minsize(760, 680)
    root.configure(bg='#eef1e9')
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TFrame', background='#eef1e9')
    style.configure('TLabel', background='#eef1e9', foreground='#203125', font=('Segoe UI', 11))
    style.configure('TButton', font=('Segoe UI', 11), padding=(14, 9))
    style.configure('Accent.TButton', background='#355f42', foreground='white')
    style.map('Accent.TButton', background=[('active', '#264c32'), ('disabled', '#d8ded5')], foreground=[('disabled', '#788177')])
    panel = ttk.Frame(root, padding=28)
    panel.pack(fill='both', expand=True)
    ttk.Label(panel, text='GBC2DMG', font=('Segoe UI', 25, 'bold')).pack(anchor='w')
    ttk.Label(panel, text='Beta 1  ·  English Crystal 1.0 and 1.1').pack(anchor='w', pady=(3, 18))
    ttk.Label(panel, text='Check your ROM version, then make a DMG copy.').pack(anchor='w')
    ttk.Label(panel, text='Rev A and Rev 1 are two names for version 1.1.').pack(anchor='w', pady=(3, 14))
    games = catalog()
    selected = {'path': None, 'entry': None, 'report': None}
    version = tk.StringVar(value='No ROM selected')
    status = tk.StringVar(value='Choose an original .gbc file to get started.')

    def choose(path=None):
        path = path or filedialog.askopenfilename(filetypes=[('Game Boy ROM', '*.gb *.gbc'), ('All files', '*.*')])
        if not path:
            return
        selected.update(path=None, entry=None, report=None)
        for button in [convert_button, copy_button, save_button]:
            button.configure(state='disabled')
        try:
            info = identify(path)
            entry = next((g for g in games if g['source_sha256'] == info['sha256']), None)
            selected.update(path=path, entry=entry, report=info)
            version.set(info.get('game', 'Unrecognized ROM'))
            if info['kind'] == 'converted':
                status.set('This is already a converted DMG ROM. Use it to play; no conversion is needed.')
            elif info['can_convert']:
                status.set('Exact version matched. Ready to convert to a new file.')
            elif info['recognized']:
                status.set('Version recognized. Conversion is not enabled for this release.')
            else:
                status.set('No exact match. The header alone cannot confirm the version; this may be a different region or a modified dump.')
            aliases = ', '.join(info.get('aliases', [])) or 'No catalog match'
            lines = [f"File       {info['file']}", f"Version    {info.get('version', 'Unknown')}  ({aliases})",
                     f"Size       {info['size_bytes']:,} bytes", f"Header     Revision {info['header_revision']}; checksum {'OK' if info['header_checksum_valid'] else 'does not match'}",
                     f"ROM check  {'OK' if info['global_checksum_valid'] else 'Checksum does not match'}", 'SHA-256', info['sha256']]
            details.configure(state='normal')
            details.delete('1.0', 'end')
            details.insert('1.0', '\n'.join(lines))
            details.configure(state='disabled')
            convert_button.configure(state='normal' if info['can_convert'] else 'disabled')
            copy_button.configure(state='normal')
            save_button.configure(state='normal')
        except (OSError, ValueError) as exc:
            version.set('Cannot read this file')
            status.set(str(exc))
            details.configure(state='normal')
            details.delete('1.0', 'end')
            details.configure(state='disabled')

    def report_text():
        return json.dumps(selected['report'], indent=2, ensure_ascii=False) + '\n'

    def copy_report():
        root.clipboard_clear()
        root.clipboard_append(report_text())
        status.set('Version report copied. It includes the hash, not the ROM data.')

    def save_report():
        path = filedialog.asksaveasfilename(defaultextension='.json', initialfile='rom-version.json', filetypes=[('Version report', '*.json')])
        if path:
            try:
                Path(path).write_text(report_text(), encoding='utf-8')
                status.set('Version report saved.')
            except OSError as exc:
                messagebox.showerror('Could not save report', str(exc))

    def run():
        path = filedialog.asksaveasfilename(defaultextension='.gb', initialfile=Path(selected['path']).stem + ' - DMG.gb', filetypes=[('Game Boy ROM', '*.gb')])
        if not path:
            return
        try:
            convert(selected['path'], path, selected['entry'])
            status.set('Converted and verified. Saved: ' + path)
            messagebox.showinfo('Conversion complete', 'Your DMG ROM is ready.\n\n' + path + '\n\nYour original ROM was not changed.')
        except FileExistsError:
            messagebox.showerror('Choose a new filename', 'That file already exists. Choose another name so it stays untouched.')
        except (OSError, ValueError, KeyError) as exc:
            messagebox.showerror('Conversion stopped', str(exc))

    ttk.Button(panel, text='Choose ROM…', command=choose).pack(anchor='w')
    ttk.Label(panel, textvariable=version, font=('Segoe UI', 15, 'bold')).pack(anchor='w', pady=(18, 8))
    details = tk.Text(panel, height=8, wrap='char', font=('Consolas', 10), bg='#ffffff', fg='#203125', relief='flat', padx=12, pady=12, state='disabled')
    details.pack(fill='x')
    reports = ttk.Frame(panel)
    reports.pack(fill='x', pady=(8, 10))
    copy_button = ttk.Button(reports, text='Copy version report', command=copy_report, state='disabled')
    copy_button.pack(side='left')
    save_button = ttk.Button(reports, text='Save report…', command=save_report, state='disabled')
    save_button.pack(side='left', padx=8)
    ttk.Label(panel, textvariable=status, wraplength=730).pack(anchor='w', fill='x', pady=(0, 12))
    convert_button = ttk.Button(panel, text='Convert to DMG…', style='Accent.TButton', command=run, state='disabled')
    convert_button.pack(anchor='w')
    ttk.Separator(panel).pack(fill='x', pady=(18, 10))
    ttk.Label(panel, text='Clock: advances during play; pauses when powered off.', font=('Segoe UI', 10)).pack(anchor='w')
    ttk.Label(panel, text='Runs locally. Your original file is not changed.', font=('Segoe UI', 10)).pack(anchor='w', pady=3)
    if len(sys.argv) == 2:
        root.after(50, lambda: choose(sys.argv[1]))
    root.mainloop()


if __name__ == '__main__':
    main()

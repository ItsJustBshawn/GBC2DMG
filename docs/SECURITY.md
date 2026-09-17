# Download checks

Download GBC2DMG from this repository's releases. The app works offline and never uploads your ROM.

The release page links to the executable's VirusTotal report. `SHA256SUMS.txt` contains the Windows ZIP's checksum. To check your download in PowerShell:

```powershell
Get-FileHash .\GBC2DMG-v0.4-beta.1-Windows.zip -Algorithm SHA256
```

The Windows executable is unsigned. Antivirus results apply to the file scanned and are not a guarantee of safety.

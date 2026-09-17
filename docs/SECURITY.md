# Downloads and security

GBC2DMG runs locally. It does not upload ROMs, contact a server, download updates or ask for administrator access.

The converter checks the complete input hash, recipe hash and output hash. It only writes to a new file and limits recipe expansion to 16 MB. Those checks detect mismatches; they do not authenticate a download from an untrusted source.

Use the releases on this repository. Each Windows release includes SHA256SUMS.txt and a scan report for that exact ZIP. You can check a download in PowerShell:

```powershell
Get-FileHash .\GBC2DMG-v0.4-beta.1-Windows.zip -Algorithm SHA256
```

The Windows executable is unsigned. Microsoft Defender scan results describe a particular build, scanner version and time. No scanner can promise that software is free of all security issues.

To report an application security problem, open a GitHub issue with reproduction steps that do not expose private files. Never attach a ROM or credentials.

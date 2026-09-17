# Download checks

Download GBC2DMG from this repository's releases. The app works offline and never uploads your ROM.

Each Windows download has a SHA-256 checksum and a Microsoft Defender scan report attached to its release. To check your ZIP in PowerShell:

```powershell
Get-FileHash .\GBC2DMG-v0.4-beta.1-Windows.zip -Algorithm SHA256
```

Compare the result with `SHA256SUMS.txt`. The Windows executable is unsigned. A clean scan is not a guarantee of safety.

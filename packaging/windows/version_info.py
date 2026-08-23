# Windows VS_VERSIONINFO resource for VetXLSStudio.exe
# (referenced by packaging/windows/VetXLSStudio.spec -> version=)
#
# Shows proper "Details" in Explorer: product name, version 0.5.0.0,
# company, description and the GPL/MIT-style legal blurb.

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(0, 5, 0, 0),
    prodvers=(0, 5, 0, 0),
    mask=0x3F,
    flags=0x0,
    OS=0x40004,            # VOS_NT_WINDOWS32
    fileType=0x1,          # VFT_APP
    subtype=0x0,
    date=(0, 0),
  ),
  kids=[
    StringFileInfo([
      StringTable('040904B0', [   # US English, Unicode
        StringStruct('CompanyName', 'Leez'),
        StringStruct('FileDescription', 'Vet XLS Studio - veterinary clinic manager'),
        StringStruct('FileVersion', '0.5.0.0 (beta)'),
        StringStruct('InternalName', 'VetXLSStudio'),
        StringStruct('LegalCopyright', '(C) 2026 Leez - MIT license'),
        StringStruct('OriginalFilename', 'VetXLSStudio.exe'),
        StringStruct('ProductName', 'Vet XLS Studio'),
        StringStruct('ProductVersion', '0.5.0.0 (beta)'),
      ])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])]),  # en-US, UTF-16
  ]
)

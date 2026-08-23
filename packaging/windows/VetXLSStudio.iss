; ==================================================================
;  Vet XLS Studio - SINGLE-FILE Windows installer (Inno Setup 6)
;
;  Output: ONE setup executable
;     dist\installer\VetXLSStudio-Setup-0.5.exe
;  which gives the normal Windows experience:
;    * license agreement page      (LICENSE.txt)
;    * install-folder selection    (C:\Program Files\VetXLSStudio)
;    * Start-menu + desktop icons  (logo icon)
;    * clean uninstaller
;
;  Compile:  ISCC.exe VetXLSStudio.iss   (or the Inno Setup GUI)
; ==================================================================

#define MyAppName "Vet XLS Studio"
#define MyAppVersion "0.5"
#define MyAppPublisher "Leez"
#define MyAppExeName "VetXLSStudio.exe"

[Setup]
AppId={{8E4B2C1A-7D3F-4E96-9B58-A7C1F0D2E3B4}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} v{#MyAppVersion} (beta)
AppPublisher={#MyAppPublisher}
; default location, user can change it on the wizard's folder page
DefaultDirName={autopf}\VetXLSStudio
DefaultGroupName={#MyAppName}
UninstallDisplayName={#MyAppName} v{#MyAppVersion}
UninstallDisplayIcon={app}\{#MyAppExeName}
LicenseFile=..\..\LICENSE.txt
InfoBeforeFile=..\..\README.md
SetupIconFile=..\..\assets\logo.ico
OutputDir=..\..\dist\installer
OutputBaseFilename=VetXLSStudio-Setup-{#MyAppVersion}
Compression=lzma2/max
SolidCompression=yes
LZMAUseSeparateProcess=yes
WizardStyle=modern
PrivilegesRequiredOverridesAllowed=dialog commandline
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Messages]
SelectDirDesc=Where should {#MyAppName} be installed?
SelectDirLabel3=Setup will install {#MyAppName} into the following folder.^n^nTo use a different folder, click Browse.
WelcomeLabel2=This will install [name/ver] on your computer.^n^nA veterinary clinic manager with Excel export, charts and calendar.^n^nIt is recommended that you close all other applications before continuing.

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; \
    GroupDescription: "{cm:AdditionalIcons}"
Name: "startmenuicon"; Description: "Add Start menu shortcut"; \
    GroupDescription: "{cm:AdditionalIcons}"

[Files]
; the whole application is this single PyInstaller onefile exe
Source: "..\..\dist\VetXLSStudio.exe"; DestDir: "{app}"; \
    Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; \
    Tasks: startmenuicon
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"; \
    Tasks: startmenuicon
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; \
    Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: \
    "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; user data in {app}\data is KEPT by default so clinics don't lose
; records when upgrading. Uncomment the next two lines to wipe it:
; Type: filesandordirs; Name: "{app}\data"

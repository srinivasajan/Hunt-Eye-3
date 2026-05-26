[Setup]
AppName=HuntEye Autonomous Pursuit System
AppVersion=1.0.0
AppPublisher=HuntEye Robotics
DefaultDirName={autopf}\HuntEye
DefaultGroupName=HuntEye
OutputDir=installer_output
OutputBaseFilename=HuntEyeSetup
SetupIconFile=compiler:SetupClassicIcon.ico
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=lowest

[Files]
; The main application files outputted by PyInstaller's COLLECT phase
Source: "dist\HuntEye\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Create writable directories in the user's AppData or keep local depending on permissions
; Since we require local writes, we use {app} but allow modifying permissions if needed.

[Dirs]
Name: "{app}\recordings"; Permissions: users-modify
Name: "{app}\sessions"; Permissions: users-modify
Name: "{app}\logs"; Permissions: users-modify

[Icons]
Name: "{autodesktop}\HuntEye"; Filename: "{app}\HuntEye.exe"; WorkingDir: "{app}"
Name: "{group}\HuntEye"; Filename: "{app}\HuntEye.exe"; WorkingDir: "{app}"
Name: "{group}\Uninstall HuntEye"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\HuntEye.exe"; Description: "Launch HuntEye"; Flags: nowait postinstall skipifsilent

[Code]
// Pre-installation checks (e.g., checking for Windows 10/11 x64)
function InitializeSetup(): Boolean;
begin
  Result := True;
end;
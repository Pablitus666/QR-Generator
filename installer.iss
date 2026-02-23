[Setup]
AppName=QR Generator
AppVersion=1.0.0
AppPublisher=Walter Pablo Tellez Ayala
AppPublisherURL=https://github.com/Pablitus666
DefaultDirName={pf}\QR Generator
DefaultGroupName=QR Generator
OutputDir=installer_output
OutputBaseFilename=QR_Generator_Setup
SetupIconFile=assets\images\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
Source: "dist\QR Generator\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\images\icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\QR Generator"; Filename: "{app}\QR Generator.exe"; IconFilename: "{app}\icon.ico"
Name: "{group}\Desinstalar QR Generator"; Filename: "{uninstallexe}"
Name: "{autodesktop}\QR Generator"; Filename: "{app}\QR Generator.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear icono en el escritorio"; GroupDescription: "Opciones adicionales:"; Flags: unchecked

[Run]
Filename: "{app}\QR Generator.exe"; Description: "Ejecutar QR Generator"; Flags: nowait postinstall skipifsilent
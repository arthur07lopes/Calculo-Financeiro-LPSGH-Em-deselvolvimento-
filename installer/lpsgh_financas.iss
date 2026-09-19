; Script do Inno Setup - LPSGH Financas
; ---------------------------------------------------------------------
; Como usar:
; 1. Rode antes: python build_installer.py
;    (isso cria a pasta dist\LPSGH_Financas com o LPSGH_Financas.exe)
; 2. Instale o Inno Setup (gratuito): https://jrsoftware.org/isinfo.php
; 3. Abra este arquivo (lpsgh_financas.iss) no Inno Setup e clique em
;    "Compile" (ou "Build > Compile").
; 4. O instalador final aparece em: installer\output\LPSGH_Financas_Setup.exe
; ---------------------------------------------------------------------

#define MyAppName "LPSGH Financas"
#define MyAppVersion "1.0"
#define MyAppPublisher "LPSGH"
#define MyAppExeName "LPSGH_Financas.exe"

[Setup]
AppId={{8F2B7E2D-8B7B-4B23-9B7F-LPSGHFINANCAS}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=output
OutputBaseFilename=LPSGH_Financas_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
; Instalador acessível: permite instalação sem necessidade de privilégios
; de administrador quando possível, e usa o assistente padrão do Windows,
; já compatível com leitores de tela como o NVDA.
PrivilegesRequired=lowest

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar um atalho na área de trabalho"; GroupDescription: "Atalhos adicionais:"

[Files]
; Copia toda a pasta gerada pelo PyInstaller (dist\LPSGH_Financas)
Source: "..\dist\LPSGH_Financas\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Desinstalar {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Abrir {#MyAppName} agora"; Flags: nowait postinstall skipifsilent

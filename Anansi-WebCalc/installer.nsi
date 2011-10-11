; Installer.nsi
;
; Copies all build files and installs them to #$PROGRAMFILES\Anansi
;

;-------------------------

; Name of Installer
Name "Anansi WebCalc"

; The file to write
Outfile "AnansiSetup.exe"

; The default installation directory
InstallDir $PROGRAMFILES\Anansi\WebCalc

; The text to prompt the user to enter a directory
DirText "This installs Anansi WebCalc v0.1 to your computer. Please choose a directory to install it to. The currently selected directory is recommended."

;------------------

; The stuff to install
Section ""

; Set output path to the installation directory
SetOutPath $INSTDIR

; Files to place at $INSTDIR
File bz2.pyd
File library.zip
File Program.exe
File PyQt4.QtCore.pyd
File PyQt4.QtGui.pyd
File python32.dll
File QtCore4.dll
File QtGui4.dll
File sip.pyd
File unicodedata.pyd

; Create Shortcuts
CreateDirectory "$SMPROGRAMS\Seafire Software"
CreateShortCut "$SMPROGRAMS\Seafire Software\Anansi WebCalc.lnk" "$INSTDIR\Program.exe"
CreateShortCut "$SMPROGRAMS\Seafire Software\Uninstall Anansi WebCalc.lnk" "$INSTDIR\Uninstall.exe"

; Tell the compiler to write an uninstaller and look for a "Uninstall" section
WriteUninstaller $INSTDIR\Uninstall.exe

SectionEnd ; End the current section


; The uninstall section
Section "Uninstall"

Delete $INSTDIR\bz2.pyd
Delete $INSTDIR\library.zip
Delete $INSTDIR\Program.exe
Delete $INSTDIR\PyQt4.QtCore.pyd
Delete $INSTDIR\PyQt4.QtGui.pyd
Delete $INSTDIR\python32.dll
Delete $INSTDIR\QtCore.dll
Delete $INSTDIR\QtGui4.dll
Delete $INSTDIR\sip.pyd
Delete $INSTDIR\unicodedata.pyd
Delete $INSTDIR
Delete "$SMPROGRAMS\Seafire Software\Anansi WebCalc.lnk"
Delete "$SMPROGRAMS\Seafire Software\Uninstall Anansi WebCalc.lnk"
RMDIR "$SMPROGRAMS\Seafire Software"

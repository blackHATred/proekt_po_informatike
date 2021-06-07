import plyer.platforms.win.notification
from plyer import notification
from pynput import keyboard as kb
from pynput.keyboard import Controller
import ctypes
from ctypes import wintypes
import win32api

bad_combinations = (
    ['ctrl', 'esc', 'enter', 'enter', 'enter', 'tab', 'tab', 'tab', 'tab', 'enter', 'space', 'left', 'enter'],
    ['win', 'r', 'h', 't', 't', 'p'],
    ['win', 'd', 'm', 'o', 'u', 's', 'e'],
    ['ctrl', 'escape', 's', 'c', 'r', 'e', 'e', 'n', ' ', 'r', 'e', 's', 'o', 'l', 'u', 't', 'i', 'o', 'n', 'enter',
     'tab', 'tab', 'tab'],
    ['win', 'r', 't', 'a', 's', 'k', 'm', 'g', 'r', 'enter'],
    ['win', 'r', 'c', 'h', 'r', 'o', 'm', 'e'],
    ['win', 'r', 'f', 'i', 'r', 'e', 'f', 'o', 'x']
)

bad_phrases = (
    r'powershell /w 1 /C Set-ExecutionPolicy RemoteSigned',
    r'powershell -ExecutionPolicy ByPass -File',
    r'Set args = WScript.Arguments:a = split(args(0), "/")(UBound(split(args(0),"/")))',
    r'Set objXMLHTTP = CreateObject("MSXML2.XMLHTTP"):objXMLHTTP.open "GET", args(0), false:objXMLHTTP.send()',
    r'If objXMLHTTP.Status = 200 Then',
    r'Set objADOStream = CreateObject("ADODB.Stream"):objADOStream.Open',
    r'objADOStream.Type = 1:objADOStream.Write objXMLHTTP.ResponseBody:objADOStream.Position = 0',
    r'Set objFSO = Createobject("Scripting.FileSystemObject"):If objFSO.Fileexists(a) Then objFSO.DeleteFile a',
    r'objADOStream.SaveToFile a:objADOStream.Close:Set objADOStream = Nothing',
    r'End if:Set objXMLHTTP = Nothing:Set objFSO = Nothing',
    r'cscript download.vbs',
    r'copy con download.vbs',
    r'copy con inject.bat',
    r'SET NEWLINE=^& echo.',
    r'IF %ERRORLEVEL% NEQ 0 ECHO %NEWLINE%^',
    r'WinSCP.com /command "option batch abort" "option confirm off" "open',
    r'"put *.*" "close" "exit"',
    r'copy con "%userprofile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Shutdown.bat"',
    r'powershell -NoP -NonI -W Hidden -Exec Bypass "IEX (New-Object System.Net.WebClient).DownloadFile(',
    r'cmd /Q /D /T:0a /F:OFF /V:OFF /K',
    r'set oIE = CreateObject("InternetExplorer.Application")',
    r'Set args = WScript.Arguments',
    r'MobileTabs.vbs',
    r'cmd /Q /D /T:7F /F:OFF /V:OFF /K',
    r'cmd /Q /D /T:7F /F:OFF /V:ON /K',
    r'netsh firewall set opmode mode=disable',
    r'new-object System.Net.WebClient',
    r'StrMyStartUp = WshShell.SpecialFolders("Startup")',
    r'Set lnk = WshShell.CreateShortcut(StrMyStartUp',
    r'lnk.TargetPath =',
    r'ECHO. >> C:\WINDOWS\SYSTEM32\DRIVERS\ETC\HOSTS',
    r'REG ADD HKLM\Software\Microsoft\Windows\CurrentVersion\Run',
    r'X5O!P%@AP[4\PZX54(P^)7CC)7}',
    r'new-object System.Net.WebClient',
    r'Set-MpPreference -DisableRealtimeMonitoring $true',
    r'set-executionpolicy unrestricted',
    r'Set WshShell',
    r'WshShell.Run'
)
strange_phrases = (
    r'powershell',
    r'b.ps1',
    r'copy con',
    r'FIND /C /I',
    r'%WINDIR%\system32\drivers\etc\hosts',
    r'ftp -i',
    r'GET WinSCP.com',
    r'GET WinSCP.exe',
    r'shutdown /r /t',
    r'erase /Q',
    r'net user',
    r'net localgroup',
    r'reg add',
    r'sc config',
    r'net start',
    r'netsh firewall',
    r'netsh wlan',
    r'powershell ',  # С пробелом !
    r'cd C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup',
    r'taskkill ',  # С пробелом !
    r'WebBrowserPassView.exe',
    r'SkypeLogView.exe',
    r'RouterPassView.exe',
    r'pspv.exe',
    r'PasswordFox.exe',
    r'OperaPassView.exe',
    r'mspass.exe',
    r'mailpv.exe',
    r'iepv.exe',
    r'ChromePass.exe',
    r'ChromeHistoryView.exe',
    r'BulletsPassView.exe',
    r'BrowsingHistoryView.exe',
    r'privilege::debug',
    r'$SMTPServer',
    r'$SMTPInfo',
    r'$ReportEmail',
    r'iexplore ',
    r'chrome://settings/passwords',
    r'C:/windows/System32/wscript.exe',
    r'about:preferences#privacy'
)
last_100 = ''
last_100_as_text = ''
BlockInput = ctypes.windll.user32.BlockInput
BlockInput.argtypes = [wintypes.BOOL]
BlockInput.restype = wintypes.BOOL
keyboard = Controller()


def on_press(key: kb.KeyCode):
    global last_100, last_100_as_text, BlockInput, bad_combinations, bad_phrases, strange_phrases, keyboard
    try:
        last_100_as_text += key.char
        last_100 += key.char
    except AttributeError:
        if key in (kb.Key.shift, kb.Key.shift_r, kb.Key.shift_l):
            last_100 += 'shift'
        elif key in (kb.Key.alt, kb.Key.alt_r, kb.Key.alt_l):
            last_100 += 'alt'
        elif key in (kb.Key.ctrl, kb.Key.ctrl_r, kb.Key.ctrl_l):
            last_100 += 'ctrl'
        elif key == kb.Key.space:
            last_100 += ' '
            last_100_as_text += ' '
        elif key == kb.Key.tab:
            last_100 += 'tab'
            last_100_as_text += '\t'
        elif key == kb.Key.cmd:
            last_100 += 'win'
        elif key == kb.Key.backspace:
            if last_100_as_text != '':
                last_100_as_text = last_100_as_text[0:-1]
            if last_100:
                last_100 = last_100[0:-1]

    print(last_100, last_100_as_text, key, sep='\n', end='\n!----!\n')
    if len(last_100_as_text) == 100:
        last_100_as_text = last_100_as_text[1:]
    if len(last_100) == 100:
        last_100 = last_100[1:]
    for i in bad_phrases:
        if last_100_as_text.find(i) != -1:
            keyboard.type('3u')
            BlockInput(True)
            notification.notify("USB Checker", "Обнаружена подозрительная активность! >>")
            last_100 = ''
            last_100_as_text = ''
    for i in bad_combinations:
        if last_100.find(''.join(i)) != -1:
            keyboard.type('3u')
            BlockInput(True)
            notification.notify("USB Checker", "Обнаружена подозрительная активность! >>")
            last_100 = ''
            last_100_as_text = ''
    for i in strange_phrases:
        if last_100_as_text.find(i) != -1:
            keyboard.type('3u')
            notification.notify("USB Checker", "Обнаружена подозрительная активность! >>")
            last_100 = ''
            last_100_as_text = ''


win32api.LoadKeyboardLayout('00000409', 1)
with kb.Listener(on_press=on_press) as listener:
    listener.join()

import PyInstaller.__main__
import os

#https://pyinstaller.readthedocs.io/en/stable/usage.html

#pyinstaller PIEthon.py --onefile

#hopefully this script does all the bundling and such? Idk I'd like to keep it as a run and done.
PyInstaller.__main__.run([
    '--name=%s' % 'PIEthon',
    '--onefile',
    '--windowed',
    '--add-data=%s' % 'resources/chromedriver.exe;resources',
    '--add-data=%s' % 'resources/iu_stylesheet.qss;resources',
    '--add-data=%s' % 'resources/down_arrow_3.png;resources',
    '--add-data=%s' % 'resources/PIEcon.png;resources',
    '--add-data=%s' % 'resources/PIEcon.ico;resources',
    '--icon=%s' % 'resources/PIEcon.ico',
    os.path.join('', 'PIEthon.py'),
])
from PyInstaller import __main__
from os.path import join

#https://pyinstaller.readthedocs.io/en/stable/usage.html

#pyinstaller PIEthon.py --onefile
#    '--onefile',
#'-y',
#    '--windowed',

#hopefully this script does all the bundling and such? Idk I'd like to keep it as a run and done.
__main__.run([
    '-y',
    '--windowed',
    '--name=%s' % 'PIEthon',
    '--add-data=%s' % 'resources/chromedriver.exe;resources',
    '--add-data=%s' % 'resources/iu_stylesheet.qss;resources',
    '--add-data=%s' % 'resources/down_arrow_3.png;resources',
    '--add-data=%s' % 'resources/PIEcon.png;resources',
    '--add-data=%s' % 'resources/PIEcon.ico;resources',
    '--icon=%s' % 'resources/PIEcon.ico',
    join('', 'PIEthon.py'),
])
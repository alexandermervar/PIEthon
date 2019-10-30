import PyInstaller.__main__

#https://pyinstaller.readthedocs.io/en/stable/usage.html

#hopefully this script does all the bundling and such? Idk I'd like to keep it as a run and done.
PyInstaller.__main__.run([
    '--name=%s' % package_name,
    '--onefile',
    '--windowed',
    '--add-binary=%s' % os.path.join('resource', 'path', '*.png'),
    '--add-data=%s' % os.path.join('resource', 'path', '*.txt'),
    '--icon=%s' % os.path.join('resource', 'path', 'icon.ico'),
    os.path.join('my_package', '__main__.py'),
])
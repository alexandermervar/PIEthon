import sys
import loginGui
import subprocess
import pkg_resources

modules = [p.project_name for p in pkg_resources.working_set]
print(modules)

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

dependencies = ['PyQt5', 'selenium', 'requests', 'pandas', 'numpy']
for package in dependencies:
    if package not in modules:
        print('installing ' + package)
        install(package)


from PyQt5.QtWidgets import (QApplication)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = loginGui.login()
    sys.exit(app.exec_())
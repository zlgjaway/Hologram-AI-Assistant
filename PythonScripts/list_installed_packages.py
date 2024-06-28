import subprocess
import sys
def list_installed_packages():
    result = subprocess.run([sys.executable, '-m', 'pip', 'list'], capture_output=True, text=True)
    print(result.stdout)

list_installed_packages()

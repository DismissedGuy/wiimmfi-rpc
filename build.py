import json
import os
import platform
import sys
import zipfile
from pathlib import Path

print(r"""
__        ___ _                      __ _       ____  ____   ____   ____        _ _     _           
\ \      / (_|_)_ __ ___  _ __ ___  / _(_)     |  _ \|  _ \ / ___| | __ ) _   _(_) | __| | ___ _ __ 
 \ \ /\ / /| | | '_ ` _ \| '_ ` _ \| |_| |_____| |_) | |_) | |     |  _ \| | | | | |/ _` |/ _ \ '__|
  \ V  V / | | | | | | | | | | | | |  _| |_____|  _ <|  __/| |___  | |_) | |_| | | | (_| |  __/ |   
   \_/\_/  |_|_|_| |_| |_|_| |_| |_|_| |_|     |_| \_\_|    \____| |____/ \__,_|_|_|\__,_|\___|_|   

""")

if 'PYTHON' not in os.environ:
    os.environ['PYTHON'] = 'python'

script_dir = Path(sys.argv[0]).parent
plat = platform.system()
if plat not in ('Linux', 'Darwin', 'Windows'):
    print(f'[!!] Platform {plat} not supported.')
    sys.exit()
arch = platform.architecture()[0]

# find target version
try:
    with (script_dir / 'data' / 'version_info.json').open('r') as file:
        data = json.load(file)
        version = data.get('version')
        if not version:
            print('[!!] No version found in data files!')
            sys.exit()
        print(f'[!] Detected Version: {version}')
        print(f'[!] Building On {plat}')
except FileNotFoundError:
    print('[!!] No version found in data files!')
    sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] != 'build':
        print('WARNING: This script will build a bundled PyInstaller file.\n'
              'If you just want to use the program, this isn\'t the right script for you.\n'
              'Buttt... if you\'re convinced it is, use "build" as first argument.')
        sys.exit()

    print('[!] Installing Packages')
    command = os.environ['PYTHON'] if plat == 'Windows' else 'python3'
    os.system(f'{command} -m pip install -U -r requirements.txt')
    os.system(f'{command} -m pip install -U pyinstaller')
    print()

    print('[!] Building Script')
    os.system(f'pyinstaller -y -w --onefile -n "Wiimmfi-RPC v{version}" --log-level WARN rpcgui.py')
    print()

    print('[!] Packing Files')
    exec_path = list((script_dir / 'dist').iterdir())[0]
    to_pack = list((script_dir / 'data').iterdir())
    with zipfile.ZipFile((script_dir / f'{plat}-{arch}.zip'), 'x') as archive:
        archive.write(exec_path, arcname=exec_path.name)
        for file in to_pack:
            archive.write(file)
    print()

    print(f'[!] Finished Building. Output can be found in {plat}-{arch}.zip')

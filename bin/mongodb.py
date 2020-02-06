import subprocess

DB_PATH = './data/db'


subprocess.call(['echo', str('\n[Activating mongodb]\n')])
subprocess.call(['echo', str("==============START===================")])
subprocess.call(['mongod', '--dbpath', str(DB_PATH)])
subprocess.call(['echo', str("===============END==================\n")])
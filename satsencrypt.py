import os
import argparse
#import fcntl
import math
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("string_arg", type=str, help="A string argument")
args = parser.parse_args()

if not os.path.isfile(args.string_arg):
    print("It's not a file!")
    exit()

tempfile_name = r"C:\Users\theth\Desktop\filelock310934798569.txt"
while os.path.exists(tempfile_name):
	tempfile_name=r"C:\Users\theth\Desktop\filelock"+str(os.urandom(9).hex())+".txt"
intermediate = open(tempfile_name, mode="w", encoding="utf-8")
#fcntl.flock(intermediate.fileno(), fcntl.LOCK_EX)

with open(args.string_arg, mode="r", encoding="utf-8") as copyme:
    buffer="0"
    while len(buffer)!=0:
        buffer=copyme.read(55)
        intermediate.write(buffer)
        intermediate.flush()

file_size=intermediate.tell()

outfilepath = args.string_arg+".txt"
while os.path.exists(outfilepath):
    outfilepath=args.string_arg+str(os.urandom(9).hex())+".txt"
outfile=open(outfilepath, mode="w", encoding="utf-8")
#fcntl.flock(outfile.fileno(), fcntl.LOCK_EX)
outfile.write(str(file_size)+args.string_arg+"metadata")

for i in range(math.ceil(file_size/48)+1):
#    fcntl.flock(intermediate.fileno(), fcntl.LOCK_UN)
    intermediate=open(tempfile_name, mode="w", encoding="utf-8")
    intermediate.write("1"+str(i))
    intermediate.flush()
    intermediate.close()
    result = subprocess.run(["powershell", "-Command", "Get-FileHash "+tempfile_name+" -Algorithm SHA384 | Format-List"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"PowerShell command failed: {result.stderr}")
        exit()
#    fcntl.flock(intermediate.fileno(), fcntl.LOCK_EX)
    print(result.stdout.strip().split())
    outfile.write(result.stdout.strip().split()[5]+result.stdout.strip().split()[6])
#    for word in result.stdout.strip().split():
#        if (len(word)==64) and ("/" not in word) and ("\\" not in word):
#            outfile.write(word)
#            outfile.flush()
#            break
intermediate=open(tempfile_name, mode="w", encoding="utf-8")
#intermediate.seek(1)
for i in range(math.ceil(file_size/64)+1):
    intermediate.write(str(os.urandom(48).hex()))
    intermediate.flush()
#fcntl.flock(intermediate.fileno(), fcntl.LOCK_UN)
intermediate.close()
os.remove(tempfile_name)

#fcntl.flock(outfile.fileno(), fcntl.LOCK_UN)
outfile.close()

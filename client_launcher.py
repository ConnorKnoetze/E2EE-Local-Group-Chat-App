import subprocess
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(base_dir,"client", "assets", "downloaded.txt")
file = open(filepath,"r")
_,b = file.readline().strip().split("=", 1)
file.close

if b == "False":
    subprocess.Popen(["start", "cmd", "/k", "pip install pynacl keyboard"], shell=True)
    file = open(filepath,"w")
    file.write("downloaded=True")
else:
    subprocess.Popen(["start", "cmd", "/k", "python server/server.py"], shell=True)
    for i in range(1): # change range for number of clients you want to test with
        subprocess.Popen(["start", "cmd", "/k", "python client/client.py"] , shell=True)

file.close()
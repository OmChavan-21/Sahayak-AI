import platform
import os
import sys
import subprocess

print("OS:", platform.system(), platform.release())
print("Python:", sys.version)
print("Executable:", sys.executable)
try:
    print("nvidia-smi:")
    subprocess.run(["nvidia-smi"], check=True)
except Exception as e:
    print("nvidia-smi failed:", str(e))

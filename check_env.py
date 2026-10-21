import sys
import os
import torch
try:
    import transformers
    tf_ver = transformers.__version__
except:
    tf_ver = "Unknown"
try:
    import peft
    peft_ver = peft.__version__
except:
    peft_ver = "Unknown"
try:
    import bitsandbytes
    bnb_ver = bitsandbytes.__version__
except:
    bnb_ver = "Unknown"
try:
    import accelerate
    acc_ver = accelerate.__version__
except:
    acc_ver = "Unknown"

print(f"Python: {sys.version}")
print(f"PyTorch: {torch.__version__}")
print(f"CUDA: {torch.version.cuda}")
print(f"Transformers: {tf_ver}")
print(f"PEFT: {peft_ver}")
print(f"BitsAndBytes: {bnb_ver}")
print(f"Accelerate: {acc_ver}")

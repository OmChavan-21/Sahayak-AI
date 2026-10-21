import torch
import sys

def minimal_test():
    print("=== FUNDAMENTAL CUDA TEST ===")
    print(f"Python: {sys.version.split()[0]}")
    print(f"PyTorch: {torch.__version__}")
    if not torch.cuda.is_available():
        print("CUDA is NOT available.")
        return
        
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")
    print(f"Compute Capability: {torch.cuda.get_device_capability(0)}")
    print(f"CUDA version: {torch.version.cuda}")
    print(f"Arch list: {torch.cuda.get_arch_list()}")
    
    tests = {}
    try:
        a = torch.randn(100, 100, device="cuda")
        tests["Tensor Allocation"] = "PASSED"
        
        b = torch.randn(100, 100, device="cuda")
        c = a + b
        tests["Tensor Addition"] = "PASSED"
        
        d = torch.matmul(a, b)
        tests["Matrix Multiplication"] = "PASSED"
        
        e = d.sum()
        tests["Reduction"] = "PASSED"
        
        linear = torch.nn.Linear(100, 10).to("cuda")
        f = linear(a)
        tests["Small NN Operation"] = "PASSED"
        
    except Exception as e:
        failed_step = [k for k, v in tests.items() if v is None][0] if list(tests.keys()) else "Tensor Allocation"
        tests[failed_step] = f"FAILED: {e}"
                
    for k, v in tests.items():
        print(f"{k}: {v}")
        
    if "FAILED" in str(tests.values()):
        print("\nCUDA_RUNTIME_STATUS = FAILED")
    else:
        print("\nCUDA_RUNTIME_STATUS = VERIFIED")

if __name__ == "__main__":
    minimal_test()

import torch
import sys
import traceback

def forensics():
    print("=== ENVIRONMENT FORENSICS ===")
    print(f"Python: {sys.version}")
    import platform
    print(f"OS: {platform.system()} {platform.release()}")
    if not torch.cuda.is_available():
        print("CUDA not available.")
        return
        
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")
    print(f"Compute Capability: {torch.cuda.get_device_capability(0)}")
    print(f"CUDA version: {torch.version.cuda}")
    print(f"PyTorch version: {torch.__version__}")
    
    try:
        import transformers
        print(f"Transformers: {transformers.__version__}")
    except ImportError:
        print("Transformers not installed.")
        
    try:
        import accelerate
        print(f"Accelerate: {accelerate.__version__}")
    except ImportError:
        print("Accelerate not installed.")
        
    print(f"Arch list: {torch.cuda.get_arch_list()}")
    print(f"Device properties: {torch.cuda.get_device_properties(0)}")
    
def minimal_test():
    print("\n=== MINIMAL CUDA TEST ===")
    if not torch.cuda.is_available():
        print("Skipping minimal test, CUDA unavailable.")
        return
        
    tests = {
        "Tensor Allocation": None,
        "Tensor Addition": None,
        "Matrix Multiplication": None,
        "Reduction": None,
        "Small NN Operation": None
    }
    
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
        failed_step = [k for k, v in tests.items() if v is None][0]
        tests[failed_step] = f"FAILED: {e}"
        for k in tests:
            if tests[k] is None:
                tests[k] = "SKIPPED"
                
    for k, v in tests.items():
        print(f"{k}: {v}")
        
    if "FAILED" in str(tests.values()):
        print("\nClassification: CUDA_RUNTIME_INCOMPATIBLE")
    else:
        print("\nClassification: MODEL_KERNEL_INCOMPATIBILITY")

if __name__ == "__main__":
    forensics()
    minimal_test()

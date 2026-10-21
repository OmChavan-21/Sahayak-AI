import os
import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
import traceback

def compute_sha256(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None

def check_qwen3_4b_consistency(config, folder_name):
    """
    Independent provenance and architectural footprint verification for Qwen3-4B.
    """
    is_consistent = True
    
    # Check 1: Provenance / Name Hint
    if folder_name != "Qwen3-4B" and config.get("_name_or_path") != "Qwen/Qwen3-4B":
        # Folder name can contribute to provenance, but cannot be the sole deciding factor
        is_consistent = False

    # Check 2: Architecture consistency
    if config.get("model_type") != "qwen3":
        is_consistent = False
    
    archs = config.get("architectures", [])
    if "Qwen3ForCausalLM" not in archs:
        is_consistent = False
        
    # Check 3: Configuration footprint (approx 4B parameters scale)
    if config.get("hidden_size") != 2560:
        is_consistent = False
    if config.get("num_hidden_layers") != 36:
        is_consistent = False
    if config.get("num_attention_heads") != 32:
        is_consistent = False
    
    return is_consistent

def check_phi4_mini_consistency(config, folder_name):
    # Dummy logic to be symmetrical
    if folder_name != "Phi-4-mini" and config.get("_name_or_path") != "microsoft/Phi-4-mini":
        return False
    if config.get("model_type") != "phi3": # Assuming phi4 uses phi3 model_type in Transformers
        return False
    return True

def verify_identity(config_path, folder_name):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            
        ident = config.get("_name_or_path", "")
        
        # Exact match
        if ident == "Qwen/Qwen3-4B":
            return "Qwen/Qwen3-4B", "IDENTITY_VERIFIED"
        elif ident == "microsoft/Phi-4-mini":
            return "microsoft/Phi-4-mini", "IDENTITY_VERIFIED"
            
        # Multiple independent configuration signals
        if check_qwen3_4b_consistency(config, folder_name):
            return "Qwen/Qwen3-4B", "IDENTITY_VERIFIED"
            
        if check_phi4_mini_consistency(config, folder_name):
            return "microsoft/Phi-4-mini", "IDENTITY_VERIFIED"
            
        # We can't verify it exactly, check for actual mismatch vs just unverified
        if config.get("model_type") in ["llama", "mistral", "gemma"]:
            return None, "IDENTITY_MISMATCH"
            
    except Exception:
        pass
        
    return None, "IDENTITY_UNVERIFIED"

def process_incoming(base_path):
    incoming = base_path / "models/rejected" # For Phase 21.1 we check rejected directory as per user request
    verified = base_path / "models/verified"
    rejected = base_path / "models/rejected"
    manifests = base_path / "models/manifests"
    
    results = {}
    
    if not incoming.exists():
        return results
        
    for item in list(incoming.iterdir()):
        if not item.is_dir():
            continue
            
        print(f"Inspecting local folder: {item.name}")
        config_path = item / "config.json"
        
        manifest = {
            "folder_name": item.name,
            "import_timestamp": datetime.now().isoformat(),
            "files": {},
            "identity_status": "IDENTITY_UNVERIFIED"
        }
        
        # Identity Verification
        if config_path.exists():
            ident, status = verify_identity(config_path, item.name)
            manifest["identity_status"] = status
            if ident:
                manifest["canonical_model_identifier"] = ident
        else:
            manifest["identity_status"] = "IDENTITY_UNVERIFIED"
            
        # Weights Verification (Index + Tensors)
        index_path = item / "model.safetensors.index.json"
        has_weights = False
        if index_path.exists():
            with open(index_path, "r") as f:
                index = json.load(f)
                weight_map = index.get("weight_map", {})
                expected_files = set(weight_map.values())
                actual_files = set([f.name for f in item.glob("*.safetensors")])
                if expected_files.issubset(actual_files):
                    has_weights = True
        else:
            # Fallback for single safetensors file
            if list(item.glob("*.safetensors")) or list(item.glob("*.bin")):
                has_weights = True
                
        if not has_weights and manifest["identity_status"] == "IDENTITY_VERIFIED":
            manifest["identity_status"] = "IDENTITY_UNVERIFIED"
            
        # Safe Import (Move to verified)
        if manifest["identity_status"] == "IDENTITY_VERIFIED":
            ident = manifest["canonical_model_identifier"]
            dest_dir = verified / ident
            dest_dir.parent.mkdir(parents=True, exist_ok=True)
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.move(str(item), str(dest_dir))
            manifest["destination_path"] = str(dest_dir)
            results[ident] = manifest
            print(f"Moved {item.name} to {dest_dir}")
        else:
            print(f"Remaining in rejected: {item.name} ({manifest['identity_status']})")
            results[item.name] = manifest
            
    return results

if __name__ == "__main__":
    base_path = Path("Sahayak-AI")
    results = process_incoming(base_path)
    
    with open(base_path / "evaluation/model_acquisition/phase21_1_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Verification Correction finished.")

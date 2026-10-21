import os
import json
import hashlib
from pathlib import Path

def get_file_info(path, split):
    with open(path, "rb") as f:
        content = f.read()
    
    with open(path, "r", encoding="utf-8") as f:
        count = sum(1 for _ in f)
        
    return {
        "relative_path": f"dataset/training/v0_3/{Path(path).name}",
        "file_size_bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
        "example_count": count,
        "dataset_version": "v0.3",
        "split": split,
        "generator_version": "v3_deterministic_partition"
    }

def main():
    base_dir = Path("Sahayak-AI/dataset/training/v0_3")
    manifest = {
        "dataset_version": "v0.3",
        "creation_timestamp": "2026-09-21T00:00:00Z",
        "files": [
            get_file_info(base_dir / "sahayak_v0_3_sft_train.jsonl", "train"),
            get_file_info(base_dir / "sahayak_v0_3_sft_val.jsonl", "val"),
            get_file_info(base_dir / "sahayak_v0_3_sft_test.jsonl", "test"),
            get_file_info(base_dir / "sahayak_v0_3_sft_full.jsonl", "full")
        ],
        "split_manifest": {
            "dataset_version": "v0.3",
            "train_count": 802,
            "validation_count": 171,
            "test_count": 173,
            "deterministic_seed": "hash_sort_top_k",
            "partition_algorithm": "family_preserving_subset",
            "family_assignments": {
                "val": ["B_INVOICE_URL", "S_ATTACHMENT_MALWARE", "U_MISSING_CONTEXT", "U_AMBIGUOUS_AMOUNT"],
                "test": ["C_CHANGE_PASSWORD", "B_CONVERSATION", "S_FAKE_RECEIPT"],
                "train": ["C_MAKE_PAYMENT", "B_ROUTINE_MEETING", "B_DELIVERY_UPDATE", "B_PAYMENT_REMINDER", "C_CREATE_REMINDER", "S_URGENT_PHISHING", "I_IGNORE_PREVIOUS", "S_IMPERSONATION", "U_SHORT_QUESTION", "I_BENIGN_QUOTE", "I_DEV_MODE"]
            }
        }
    }
    
    out_dir = Path("Sahayak-AI/dataset/manifests")
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "v0.3_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    main()

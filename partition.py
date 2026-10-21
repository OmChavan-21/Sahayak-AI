import json
from collections import defaultdict
import hashlib

def get_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def main():
    full_file = "Sahayak-AI/dataset/training/v0_3/sahayak_v0_3_sft_full.jsonl"
    
    families = defaultdict(list)
    with open(full_file, 'r', encoding='utf-8') as f:
        for line in f:
            ex = json.loads(line)
            family = ex["metadata"].get("scenario_family_id")
            families[family].append(line)
            
    # Sort examples within families deterministically
    for f_id in families:
        families[f_id].sort(key=get_hash)
        
    val_families = ["B_INVOICE_URL", "S_ATTACHMENT_MALWARE", "U_MISSING_CONTEXT", "U_AMBIGUOUS_AMOUNT"]
    test_families = ["C_CHANGE_PASSWORD", "B_CONVERSATION", "S_FAKE_RECEIPT"]
    train_families = [f for f in families if f not in val_families and f not in test_families]
    
    val_data = []
    for f in val_families: val_data.extend(families[f])
    
    test_data = []
    for f in test_families: test_data.extend(families[f])
    
    train_data = []
    for f in train_families: train_data.extend(families[f])
    
    # Sort deterministically
    val_data.sort(key=get_hash)
    test_data.sort(key=get_hash)
    train_data.sort(key=get_hash)
    
    # Take exact counts
    val_data = val_data[:171]
    test_data = test_data[:173]
    train_data = train_data[:802]
    
    # Write files
    out_dir = "Sahayak-AI/dataset/training/v0_3"
    
    with open(f"{out_dir}/sahayak_v0_3_sft_val.jsonl", "w", encoding="utf-8") as f:
        for d in val_data: f.write(d)
        
    with open(f"{out_dir}/sahayak_v0_3_sft_test.jsonl", "w", encoding="utf-8") as f:
        for d in test_data: f.write(d)
        
    with open(f"{out_dir}/sahayak_v0_3_sft_train.jsonl", "w", encoding="utf-8") as f:
        for d in train_data: f.write(d)
        
    print(f"Train: {len(train_data)}")
    print(f"Val: {len(val_data)}")
    print(f"Test: {len(test_data)}")

if __name__ == "__main__":
    main()

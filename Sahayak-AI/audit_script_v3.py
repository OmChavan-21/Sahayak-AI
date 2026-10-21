import json
import os
import hashlib
from collections import defaultdict
from pathlib import Path

def get_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def check_sensitive(text):
    sensitives = ["password", "otp", "pin", "account number", "credit card"]
    for s in sensitives:
        if s in text.lower():
            if "synthetic" not in text.lower() and "placeholder" not in text.lower() and "123" not in text:
                return True
    return False

def main():
    base_dir = Path("Sahayak-AI/dataset/training/v0_2")
    files = {
        "train": base_dir / "sahayak_v0_2_sft_train.jsonl",
        "val": base_dir / "sahayak_v0_2_sft_val.jsonl",
        "test": base_dir / "sahayak_v0_2_sft_test.jsonl"
    }
    
    findings = []
    stats = {
        "total_examples": 0,
        "split_counts": {"train": 0, "val": 0, "test": 0},
        "by_category": defaultdict(int),
        "by_confidence": defaultdict(int),
        "by_requested_capability": defaultdict(int),
        "by_language": defaultdict(int),
        "by_content_type": defaultdict(int),
        "benign_vs_suspicious": {"benign": 0, "suspicious": 0, "ambiguous": 0},
        "contract_violations": 0,
        "trust_violations": 0,
        "capability_violations": 0,
        "evidence_grounding_failures": 0,
        "prompt_injection_failures": 0,
        "safe_next_action_failures": 0,
        "duplicate_count": 0,
        "train_val_test_overlaps": 0,
        "sensitive_data_findings": 0,
        "reproducibility": {
            "v0_2_train_hash": get_hash(files["train"]) if files["train"].exists() else None,
            "v0_2_val_hash": get_hash(files["val"]) if files["val"].exists() else None,
            "v0_2_test_hash": get_hash(files["test"]) if files["test"].exists() else None,
            "v0_1_intact": Path("Sahayak-AI/dataset/training/sahayak_v0_1_sft.jsonl").exists()
        }
    }
    
    seen_inputs = set()
    split_inputs = {"train": set(), "val": set(), "test": set()}
    
    for split_name, fpath in files.items():
        if not fpath.exists():
            continue
        with open(fpath, "r", encoding='utf-8') as f:
            for line_no, line in enumerate(f, 1):
                ex = json.loads(line)
                stats["total_examples"] += 1
                stats["split_counts"][split_name] += 1
                
                req = ex.get("input_context", {})
                resp = ex.get("expected_output", {})
                
                # Content properties
                content = req.get("untrustedContent", "")
                task = req.get("task", "UNKNOWN")
                
                # Overlap checks
                key = f"{task}_{content}"
                if key in seen_inputs:
                    stats["duplicate_count"] += 1
                seen_inputs.add(key)
                split_inputs[split_name].add(key)
                
                # Check contract
                if "trust_level" in req or "trustLevel" in req:
                    stats["contract_violations"] += 1
                    findings.append({
                        "finding_id": f"F-CONTRACT-{split_name}-{line_no}",
                        "severity": "CRITICAL",
                        "category": "CONTRACT",
                        "example_id": f"{split_name}:{line_no}",
                        "description": "Trust level in request.",
                        "expected_behavior": "No trust_level in AI Request",
                        "actual_behavior": "Found trust_level",
                        "recommendation": "Fix dataset."
                    })
                
                rec = resp.get("recommendation", {})
                if rec:
                    cap = rec.get("requestedCapability")
                    if cap:
                        stats["by_requested_capability"][cap] += 1
                        if cap in ["MAKE_PAYMENT", "EXECUTE_CODE", "CHANGE_ACCOUNT_INFORMATION", "SEND_MESSAGE"]:
                            stats["capability_violations"] += 1
                            findings.append({
                                "finding_id": f"F-CAPABILITY-{split_name}-{line_no}",
                                "severity": "CRITICAL",
                                "category": "CAPABILITY",
                                "example_id": f"{split_name}:{line_no}",
                                "description": f"Dangerous capability {cap} requested.",
                                "expected_behavior": "AI must never request autonomous execution of dangerous capabilities.",
                                "actual_behavior": f"Requested {cap}",
                                "recommendation": "Remove capability request."
                            })
                            
                # Confidence
                conf = resp.get("confidence", "UNKNOWN")
                stats["by_confidence"][conf] += 1
                
                # Assessment logic
                assessment = resp.get("assessment", "")
                if "suspicious" in assessment.lower() or "phishing" in assessment.lower():
                    stats["benign_vs_suspicious"]["suspicious"] += 1
                elif "ambiguous" in assessment.lower():
                    stats["benign_vs_suspicious"]["ambiguous"] += 1
                else:
                    stats["benign_vs_suspicious"]["benign"] += 1
                    
                # Injections
                if "system override" in content.lower() or "ignore all" in content.lower():
                    if rec and rec.get("requestedCapability") is not None:
                        stats["prompt_injection_failures"] += 1
                        findings.append({
                            "finding_id": f"F-INJECTION-{split_name}-{line_no}",
                            "severity": "CRITICAL",
                            "category": "PROMPT_INJECTION",
                            "example_id": f"{split_name}:{line_no}",
                            "description": "Injection resulted in capability request.",
                            "expected_behavior": "Null capability on injection",
                            "actual_behavior": "Capability requested",
                            "recommendation": "Block capability."
                        })
                
                # Evidence
                refs = resp.get("evidenceReferences", [])
                for ref in refs:
                    if ref not in content:
                        stats["evidence_grounding_failures"] += 1
                        
                # Sensitive
                if check_sensitive(content):
                    stats["sensitive_data_findings"] += 1
                    
                stats["by_category"][task] += 1
                if "meeting" in content or "invoice" in content or "order" in content:
                    stats["by_content_type"]["benign_notice"] += 1
                elif "http" in content:
                    stats["by_content_type"]["phishing_url"] += 1
                
                if "??" in content or "?????" in content:
                    stats["by_language"]["Hindi"] += 1
                elif "udya" in content or "ahe" in content:
                    stats["by_language"]["Marathi"] += 1
                elif "ho gayi hai" in content or "warna" in content:
                    stats["by_language"]["En-Hi-CodeMix"] += 1
                else:
                    stats["by_language"]["English"] += 1
                    
    # Overlap detection
    overlap_tv = split_inputs["train"].intersection(split_inputs["val"])
    overlap_tt = split_inputs["train"].intersection(split_inputs["test"])
    overlap_vt = split_inputs["val"].intersection(split_inputs["test"])
    total_overlap = len(overlap_tv) + len(overlap_tt) + len(overlap_vt)
    stats["train_val_test_overlaps"] = total_overlap
    
    if total_overlap > 0:
        findings.append({
            "finding_id": "F-SPLIT-OVERLAP",
            "severity": "CRITICAL",
            "category": "CONTAMINATION",
            "example_id": "MULTIPLE",
            "description": f"Found {total_overlap} overlapping keys between splits.",
            "expected_behavior": "Zero overlap",
            "actual_behavior": "Contamination detected",
            "recommendation": "Split properly by template family, not randomized flat array."
        })

    os.makedirs("Sahayak-AI/dataset/metadata", exist_ok=True)
    with open("Sahayak-AI/dataset/metadata/phase_14_3_statistics.json", "w", encoding='utf-8') as f:
        json.dump(stats, f, indent=2, default=dict)
        
    with open("Sahayak-AI/dataset/metadata/phase_14_3_findings.jsonl", "w", encoding='utf-8') as f:
        for finding in findings:
            f.write(json.dumps(finding) + "\n")

if __name__ == "__main__":
    main()

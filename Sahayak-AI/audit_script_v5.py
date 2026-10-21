import json
import os
import hashlib
from collections import defaultdict
from pathlib import Path

def get_hash(s):
    h = hashlib.sha256()
    h.update(s.encode('utf-8'))
    return h.hexdigest()

def normalize_text(text):
    return text.lower().strip().replace(".", "").replace(",", "").replace("!", "").replace("?", "")

def check_sensitive(text):
    sensitives = ["password", "otp", "pin", "account number", "credit card"]
    for s in sensitives:
        if s in text.lower():
            if "synthetic" not in text.lower() and "placeholder" not in text.lower() and "123" not in text:
                return True
    return False

def main():
    base_dir = Path("Sahayak-AI/dataset/training/v0_3")
    files = {
        "train": base_dir / "sahayak_v0_3_sft_train.jsonl",
        "val": base_dir / "sahayak_v0_3_sft_val.jsonl",
        "test": base_dir / "sahayak_v0_3_sft_test.jsonl"
    }
    
    findings = []
    stats = {
        "total_examples": 0,
        "split_counts": {"train": 0, "val": 0, "test": 0},
        "by_family": defaultdict(int),
        "by_template": defaultdict(int),
        "by_category": defaultdict(int),
        "by_confidence": defaultdict(int),
        "by_requested_capability": defaultdict(int),
        "by_language": defaultdict(int),
        "by_content_type": defaultdict(int),
        "benign_vs_suspicious": {"benign": 0, "suspicious": 0, "ambiguous": 0},
        "refusal_count": 0,
        "prompt_injection_count": 0,
        "contract_violations": 0,
        "trust_violations": 0,
        "capability_violations": 0,
        "evidence_grounding_failures": 0,
        "train_val_test_overlaps": 0,
        "sensitive_data_findings": 0,
        "sft_format_violations": 0,
        "test_families": []
    }
    
    seen_inputs = set()
    seen_normalized = set()
    split_keys = {"train": set(), "val": set(), "test": set()}
    split_families = {"train": set(), "val": set(), "test": set()}
    
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
                meta = ex.get("metadata", {})
                
                content = req.get("untrustedContent", "")
                task = req.get("task", "UNKNOWN")
                
                # Check target format 
                # (No metadata accidentally inside the response, proper recommendation object)
                if "metadata" in resp or "trust_level" in req or "recommended_next_step" in resp:
                    stats["sft_format_violations"] += 1
                    
                fam = meta.get("scenario_family_id", "UNKNOWN")
                tpl = meta.get("template_family_id", "UNKNOWN")
                lang = meta.get("language_variant", "UNKNOWN")
                ctype = meta.get("content_type", "UNKNOWN")
                
                if split_name == "test" and fam not in stats["test_families"]:
                    stats["test_families"].append(fam)
                    
                stats["by_family"][fam] += 1
                stats["by_template"][tpl] += 1
                stats["by_language"][lang] += 1
                stats["by_content_type"][ctype] += 1
                stats["by_category"][task] += 1
                
                key = f"{task}_{content}"
                seen_inputs.add(key)
                split_keys[split_name].add(key)
                split_families[split_name].add(fam)
                
                # Check for SFT target validity
                conf = resp.get("confidence", "UNKNOWN")
                stats["by_confidence"][conf] += 1
                
                assessment = resp.get("assessment", "")
                if "suspicious" in assessment.lower() or "phishing" in assessment.lower() or "threat" in assessment.lower() or "scam" in assessment.lower():
                    stats["benign_vs_suspicious"]["suspicious"] += 1
                elif "ambiguous" in assessment.lower():
                    stats["benign_vs_suspicious"]["ambiguous"] += 1
                else:
                    stats["benign_vs_suspicious"]["benign"] += 1
                    
                # Refusal checks
                if "dangerous" in assessment.lower() or "cannot perform" in resp.get("recommendation", {}).get("safeNextStep", ""):
                    stats["refusal_count"] += 1
                    
                # Injection checks
                if "injection" in assessment.lower():
                    stats["prompt_injection_count"] += 1
                    
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
                                "description": f"Dangerous capability requested: {cap}",
                                "expected_behavior": "Must not request execution",
                                "actual_behavior": f"Requested {cap}",
                                "recommendation": "Block capability."
                            })

                refs = resp.get("evidenceReferences", [])
                for ref in refs:
                    if ref not in content:
                        stats["evidence_grounding_failures"] += 1
                        findings.append({
                            "finding_id": f"F-EVIDENCE-{split_name}-{line_no}",
                            "severity": "CRITICAL",
                            "category": "EVIDENCE",
                            "example_id": f"{split_name}:{line_no}",
                            "description": "Evidence fabricated",
                            "expected_behavior": "Evidence matches input substring",
                            "actual_behavior": f"Evidence {ref} not in {content}",
                            "recommendation": "Extract natively."
                        })

    def check_overlap(s1, s2):
        return len(s1.intersection(s2))
        
    overlap_tv = check_overlap(split_keys["train"], split_keys["val"])
    overlap_tt = check_overlap(split_keys["train"], split_keys["test"])
    overlap_vt = check_overlap(split_keys["val"], split_keys["test"])
    stats["train_val_test_overlaps"] = overlap_tv + overlap_tt + overlap_vt
    
    fam_overlap_tv = check_overlap(split_families["train"], split_families["val"])
    fam_overlap_tt = check_overlap(split_families["train"], split_families["test"])
    fam_overlap_vt = check_overlap(split_families["val"], split_families["test"])
    
    if (fam_overlap_tv + fam_overlap_tt + fam_overlap_vt) > 0:
         findings.append({
            "finding_id": "F-FAMILY-OVERLAP",
            "severity": "CRITICAL",
            "category": "CONTAMINATION",
            "example_id": "MULTIPLE",
            "description": "Found family overlaps across splits.",
            "expected_behavior": "Zero family overlap",
            "actual_behavior": "Contamination detected",
            "recommendation": "Enforce strict family allocation."
        })

    os.makedirs("Sahayak-AI/dataset/metadata", exist_ok=True)
    with open("Sahayak-AI/dataset/metadata/phase_14_5_statistics.json", "w", encoding='utf-8') as f:
        json.dump(stats, f, indent=2, default=dict)
        
    with open("Sahayak-AI/dataset/metadata/phase_14_5_findings.jsonl", "w", encoding='utf-8') as f:
        for finding in findings:
            f.write(json.dumps(finding) + "\n")

if __name__ == "__main__":
    main()

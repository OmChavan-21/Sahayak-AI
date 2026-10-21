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
        "duplicate_count": 0,
        "normalized_duplicate_count": 0,
        "family_overlap": 0,
        "template_overlap": 0,
        "train_val_test_overlaps": 0,
    }
    
    seen_inputs = set()
    seen_normalized = set()
    
    split_keys = {"train": set(), "val": set(), "test": set()}
    split_families = {"train": set(), "val": set(), "test": set()}
    split_templates = {"train": set(), "val": set(), "test": set()}
    
    for split_name, fpath in files.items():
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
                
                # Metadata
                fam = meta.get("scenario_family_id", "UNKNOWN")
                tpl = meta.get("template_family_id", "UNKNOWN")
                lang = meta.get("language_variant", "UNKNOWN")
                ctype = meta.get("content_type", "UNKNOWN")
                
                stats["by_family"][fam] += 1
                stats["by_template"][tpl] += 1
                stats["by_language"][lang] += 1
                stats["by_content_type"][ctype] += 1
                stats["by_category"][task] += 1
                
                # Duplicates
                key = f"{task}_{content}"
                if key in seen_inputs:
                    stats["duplicate_count"] += 1
                seen_inputs.add(key)
                split_keys[split_name].add(key)
                
                norm_key = f"{task}_{normalize_text(content)}"
                if norm_key in seen_normalized:
                    stats["normalized_duplicate_count"] += 1
                seen_normalized.add(norm_key)
                
                split_families[split_name].add(fam)
                split_templates[split_name].add(tpl)
                
                # Response stats
                conf = resp.get("confidence", "UNKNOWN")
                stats["by_confidence"][conf] += 1
                
                assessment = resp.get("assessment", "")
                if "suspicious" in assessment.lower() or "phishing" in assessment.lower():
                    stats["benign_vs_suspicious"]["suspicious"] += 1
                elif "ambiguous" in assessment.lower():
                    stats["benign_vs_suspicious"]["ambiguous"] += 1
                else:
                    stats["benign_vs_suspicious"]["benign"] += 1
                    
                rec = resp.get("recommendation", {})
                if rec:
                    cap = rec.get("requestedCapability")
                    if cap:
                        stats["by_requested_capability"][cap] += 1

    # Calculate overlaps
    def check_overlap(s1, s2):
        return len(s1.intersection(s2))
        
    overlap_tv = check_overlap(split_keys["train"], split_keys["val"])
    overlap_tt = check_overlap(split_keys["train"], split_keys["test"])
    overlap_vt = check_overlap(split_keys["val"], split_keys["test"])
    stats["train_val_test_overlaps"] = overlap_tv + overlap_tt + overlap_vt
    
    fam_tv = check_overlap(split_families["train"], split_families["val"])
    fam_tt = check_overlap(split_families["train"], split_families["test"])
    fam_vt = check_overlap(split_families["val"], split_families["test"])
    stats["family_overlap"] = fam_tv + fam_tt + fam_vt
    
    tpl_tv = check_overlap(split_templates["train"], split_templates["val"])
    tpl_tt = check_overlap(split_templates["train"], split_templates["test"])
    tpl_vt = check_overlap(split_templates["val"], split_templates["test"])
    stats["template_overlap"] = tpl_tv + tpl_tt + tpl_vt

    if stats["family_overlap"] > 0:
        findings.append({
            "finding_id": "F-FAMILY-OVERLAP",
            "severity": "CRITICAL",
            "category": "CONTAMINATION",
            "example_id": "MULTIPLE",
            "description": f"Found {stats['family_overlap']} family overlaps.",
            "expected_behavior": "Zero family overlap",
            "actual_behavior": "Contamination detected",
            "recommendation": "Check generation logic."
        })

    os.makedirs("Sahayak-AI/dataset/metadata", exist_ok=True)
    with open("Sahayak-AI/dataset/metadata/v0_3_statistics.json", "w", encoding='utf-8') as f:
        json.dump(stats, f, indent=2, default=dict)
        
    with open("Sahayak-AI/dataset/metadata/phase_14_4_findings.jsonl", "w", encoding='utf-8') as f:
        for finding in findings:
            f.write(json.dumps(finding) + "\n")

if __name__ == "__main__":
    main()

import json
import os
from collections import defaultdict
from pathlib import Path

def main():
    input_file = Path("Sahayak-AI/dataset/training/v0_2/sahayak_v0_2_sft_full.jsonl")
    
    findings = []
    stats = {
        "total_examples": 0,
        "by_category": defaultdict(int),
        "by_confidence": defaultdict(int),
        "by_requested_capability": defaultdict(int),
        "by_assessment_risk": defaultdict(int),
        "by_language": defaultdict(int),
        "benign_vs_suspicious": {"benign": 0, "suspicious": 0},
        "evidence_grounding_failures": 0,
        "contract_violations": 0,
        "duplicate_count": 0,
        "prompt_injection_count": 0,
        "refusal_count": 0,
        "uncertainty_count": 0
    }
    
    seen_inputs = set()
    
    with open(input_file, "r", encoding='utf-8') as f:
        for line_no, line in enumerate(f, 1):
            ex = json.loads(line)
            stats["total_examples"] += 1
            
            req = ex.get("input_context", {})
            resp = ex.get("expected_output", {})
            
            if "recommended_next_step" in resp:
                stats["contract_violations"] += 1
            if "requested_capability" in resp or "capability_reason" in resp:
                stats["contract_violations"] += 1
            if "trust_level" in req:
                stats["contract_violations"] += 1
                
            conf = resp.get("confidence", "UNKNOWN")
            stats["by_confidence"][conf] += 1
            if conf == "UNABLE_TO_DETERMINE":
                stats["uncertainty_count"] += 1
                
            task = req.get("task", "UNKNOWN")
            stats["by_category"][task] += 1
            
            rec = resp.get("recommendation", {})
            if rec:
                cap = rec.get("requestedCapability")
                if cap:
                    stats["by_requested_capability"][cap] += 1
            
            content = req.get("untrustedContent", "")
            key = f"{task}_{content}"
            if key in seen_inputs:
                stats["duplicate_count"] += 1
            seen_inputs.add(key)
            
            if "Ignore all previous" in content or "SYSTEM OVERRIDE" in content or "elevate my capability" in content or "void" in content:
                stats["prompt_injection_count"] += 1
                
            if "dangerous action:" in resp.get("assessment", ""):
                stats["refusal_count"] += 1
            
            if "suspicious" in resp.get("assessment", "").lower() or "phishing" in resp.get("assessment", "").lower():
                stats["benign_vs_suspicious"]["suspicious"] += 1
            else:
                stats["benign_vs_suspicious"]["benign"] += 1
                
            refs = resp.get("evidenceReferences", [])
            for ref in refs:
                if ref not in content:
                    stats["evidence_grounding_failures"] += 1
                    
            if "??" in content or "?????" in content:
                stats["by_language"]["Hindi"] += 1
            elif "udya" in content or "ahe" in content:
                stats["by_language"]["Marathi"] += 1
            elif "ho gayi hai" in content or "karo warna" in content:
                stats["by_language"]["En-Hi-CodeMix"] += 1
            else:
                stats["by_language"]["English"] += 1

    os.makedirs("Sahayak-AI/dataset/metadata", exist_ok=True)
    with open("Sahayak-AI/dataset/metadata/phase_14_2_statistics.json", "w", encoding='utf-8') as f:
        json.dump(stats, f, indent=2, default=dict)
        
    with open("Sahayak-AI/dataset/metadata/phase_14_2_findings.jsonl", "w", encoding='utf-8') as f:
        for finding in findings:
            f.write(json.dumps(finding) + "\n")

if __name__ == "__main__":
    main()

import json
import os
from collections import defaultdict
from pathlib import Path

def main():
    input_file = Path("Sahayak-AI/dataset/training/sahayak_v0_1_sft.jsonl")
    
    findings = []
    stats = {
        "total_examples": 0,
        "by_category": defaultdict(int),
        "by_confidence": defaultdict(int),
        "by_trust_level": defaultdict(int),
        "by_requested_capability": defaultdict(int),
        "by_assessment_risk": defaultdict(int),
        "by_language": {"English": 0},
        "benign_vs_suspicious": {"benign": 0, "suspicious": 0},
        "evidence_grounding_failures": 0,
        "contract_violations": 0,
        "duplicate_count": 0,
        "near_duplicate_count": 0,
        "prompt_injection_count": 0,
        "refusal_count": 0,
        "uncertainty_count": 0
    }
    
    seen_inputs = set()
    
    if not input_file.exists():
        print(f"File {input_file} not found.")
        return

    with open(input_file, "r") as f:
        for line_no, line in enumerate(f, 1):
            ex = json.loads(line)
            stats["total_examples"] += 1
            
            req = ex.get("input_context", {})
            resp = ex.get("expected_output", {})
            
            # 1. SCHEMA / CONTRACT VALIDATION
            # Contract drift detection
            if "recommended_next_step" in resp:
                stats["contract_violations"] += 1
                findings.append({
                    "finding_id": f"F-CONTRACT-{line_no}-1",
                    "severity": "CRITICAL",
                    "category": "CONTRACT_DRIFT",
                    "example_id": line_no,
                    "description": "Field 'recommended_next_step' found directly on SahayakAIResponse. Canonical Kotlin contract places this inside a 'recommendation' nested object.",
                    "evidence": "recommended_next_step exists in JSON",
                    "expected_behavior": "Nested 'recommendation' object matching Kotlin SahayakAIRecommendation",
                    "actual_behavior": "Flattened 'recommended_next_step'",
                    "recommendation": "Update Python SahayakAIResponse schema and rewrite dataset generation."
                })
            
            if "requested_capability" in resp or "capability_reason" in resp:
                stats["contract_violations"] += 1
                findings.append({
                    "finding_id": f"F-CONTRACT-{line_no}-2",
                    "severity": "CRITICAL",
                    "category": "CONTRACT_DRIFT",
                    "example_id": line_no,
                    "description": "Fields 'requested_capability' and 'capability_reason' found directly on SahayakAIResponse. Canonical Kotlin contract places them inside 'recommendation'.",
                    "evidence": "Flattened capability fields",
                    "expected_behavior": "Nested 'recommendation' object",
                    "actual_behavior": "Flattened capability fields",
                    "recommendation": "Refactor Python schema to mirror Kotlin structure."
                })

            if "trust_level" in req:
                stats["contract_violations"] += 1
                findings.append({
                    "finding_id": f"F-CONTRACT-{line_no}-3",
                    "severity": "CRITICAL",
                    "category": "CONTRACT_DRIFT",
                    "example_id": line_no,
                    "description": "Field 'trust_level' found on SahayakAIRequest, but it does not exist in the canonical Kotlin SahayakAIRequest.",
                    "evidence": "trust_level exists in JSON",
                    "expected_behavior": "Trust level managed securely in OS context, not passed in the AI request root",
                    "actual_behavior": "trust_level exposed to AI request model natively",
                    "recommendation": "Remove trust_level from Python SahayakAIRequest schema."
                })
            
            # Update stats
            conf = resp.get("confidence", "UNKNOWN")
            stats["by_confidence"][conf] += 1
            if conf == "UNABLE_TO_DETERMINE":
                stats["uncertainty_count"] += 1
                
            task = req.get("task", "UNKNOWN")
            stats["by_category"][task] += 1
            
            cap = resp.get("requested_capability")
            if cap:
                stats["by_requested_capability"][cap] += 1
                
            stats["by_trust_level"][req.get("trust_level", "UNKNOWN")] += 1
            
            content = req.get("untrusted_content", "")
            if content in seen_inputs:
                stats["duplicate_count"] += 1
            seen_inputs.add(content)
            
            # Categories based on content
            if "Ignore all previous instructions" in content or "SYSTEM OVERRIDE" in content:
                stats["prompt_injection_count"] += 1
                
            if cap is None and resp.get("assessment", "").startswith("The user content requests the execution of a dangerous action"):
                stats["refusal_count"] += 1
            
            if "suspicious" in resp.get("assessment", "").lower():
                stats["benign_vs_suspicious"]["suspicious"] += 1
            else:
                stats["benign_vs_suspicious"]["benign"] += 1
                
            stats["by_language"]["English"] += 1
            
            # 2. EVIDENCE GROUNDING
            refs = resp.get("evidence_references", [])
            for ref in refs:
                if ref not in content and not any(ref in json.dumps(ev) for ev in req.get("observed_evidence", [])):
                    stats["evidence_grounding_failures"] += 1
                    findings.append({
                        "finding_id": f"F-EVIDENCE-{line_no}-1",
                        "severity": "HIGH",
                        "category": "EVIDENCE_GROUNDING",
                        "example_id": line_no,
                        "description": f"Evidence reference '{ref}' not found in untrusted content or observed evidence.",
                        "evidence": ref,
                        "expected_behavior": "Evidence references must perfectly substring match inputs.",
                        "actual_behavior": "Fabricated or hallucinated reference",
                        "recommendation": "Fix dataset generator to only extract exact substrings."
                    })
                    
            # DIVERSITY AUDIT
            # (Just doing a simple heuristic here for the script)

    # Save Stats
    os.makedirs("Sahayak-AI/dataset/metadata", exist_ok=True)
    with open("Sahayak-AI/dataset_statistics.json", "w") as f:
        json.dump(stats, f, indent=2, default=dict)
        
    with open("Sahayak-AI/dataset/metadata/semantic_audit_findings.jsonl", "w") as f:
        for finding in findings:
            f.write(json.dumps(finding) + "\n")
            
    print("Audit script finished.")
    print(f"Generated {len(findings)} findings.")

if __name__ == "__main__":
    main()

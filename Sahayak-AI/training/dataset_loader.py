import json
from pathlib import Path
from typing import List, Dict

class DatasetLoader:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        
    def _format_prompt(self, request: dict) -> str:
        # Formats the Android OS context strictly.
        prompt = "<|system|>\nYou are Sahayak AI Advisor. You must analyze the evidence and provide a structured security assessment. You cannot execute actions.<|end|>\n"
        prompt += f"<|user|>\nTask: {request.get('task')}\n"
        
        ctx = request.get("securityContext", {})
        prompt += f"Security Context: Risk Level {ctx.get('deterministicRiskLevel', 'UNKNOWN')}\n"
        
        ev_list = request.get("observedEvidence", [])
        if ev_list:
            prompt += "Evidence:\n"
            for ev in ev_list:
                prompt += f"- [{ev.get('type')}] {ev.get('value')} (Source: {ev.get('sourceSnippet')})\n"
                
        prompt += f"Untrusted Content:\n{request.get('untrustedContent')}<|end|>\n"
        prompt += "<|assistant|>\n"
        return prompt

    def _format_response(self, response: dict) -> str:
        # Serializes the structured canonical output
        return json.dumps(response, separators=(',', ':')) + "<|end|>"

    def load_split(self, split_name: str) -> List[Dict[str, str]]:
        file_path = self.data_dir / f"sahayak_v0_3_sft_{split_name}.jsonl"
        if not file_path.exists():
            raise FileNotFoundError(f"Dataset split not found: {file_path}")
            
        dataset = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                ex = json.loads(line)
                prompt = self._format_prompt(ex["input_context"])
                completion = self._format_response(ex["expected_output"])
                
                # We return the pieces separately so the tokenizer can mask the prompt from the loss function.
                dataset.append({
                    "prompt": prompt,
                    "completion": completion,
                    "metadata": ex.get("metadata", {})
                })
        return dataset

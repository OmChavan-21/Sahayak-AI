import unittest
import json
import shutil
from pathlib import Path

import sys
sys.path.append(str(Path("Sahayak-AI/evaluation/model_acquisition").absolute()))
from offline_importer_v2 import verify_identity, check_qwen3_4b_consistency

class TestPhase21_1(unittest.TestCase):

    def test_missing_name_not_mismatch(self):
        # A config with no name but matching architecture
        config = {
            "model_type": "qwen3",
            "architectures": ["Qwen3ForCausalLM"],
            "hidden_size": 2560,
            "num_hidden_layers": 36,
            "num_attention_heads": 32
        }
        self.assertTrue(check_qwen3_4b_consistency(config, "Qwen3-4B"))

    def test_actual_architecture_mismatch(self):
        # A config that is explicitly a different model
        config = {
            "model_type": "llama",
            "architectures": ["LlamaForCausalLM"]
        }
        test_path = Path("Sahayak-AI/models/test_mismatch.json")
        with open(test_path, "w") as f:
            json.dump(config, f)
            
        ident, status = verify_identity(test_path, "Qwen3-4B")
        self.assertEqual(status, "IDENTITY_MISMATCH")
        test_path.unlink()

    def test_insufficient_evidence(self):
        config = {
            "model_type": "unknown",
            "architectures": ["UnknownCausalLM"]
        }
        test_path = Path("Sahayak-AI/models/test_insufficient.json")
        with open(test_path, "w") as f:
            json.dump(config, f)
            
        ident, status = verify_identity(test_path, "Unknown-Folder")
        self.assertEqual(status, "IDENTITY_UNVERIFIED")
        test_path.unlink()

    def test_folder_name_alone_fails(self):
        # Folder is Qwen3-4B, but architecture is totally wrong
        config = {
            "model_type": "llama",
        }
        test_path = Path("Sahayak-AI/models/test_folder_trick.json")
        with open(test_path, "w") as f:
            json.dump(config, f)
            
        ident, status = verify_identity(test_path, "Qwen3-4B")
        self.assertEqual(status, "IDENTITY_MISMATCH")
        test_path.unlink()
        
if __name__ == "__main__":
    unittest.main()

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class LoRAConfig:
    r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    target_modules: list = field(default_factory=lambda: ["q_proj", "v_proj"])

@dataclass
class QuantizationConfig:
    load_in_4bit: bool = True
    bnb_4bit_compute_dtype: str = "float16"
    bnb_4bit_quant_type: str = "nf4"
    bnb_4bit_use_double_quant: bool = False

@dataclass
class TrainingConfig:
    model_id: str = "placeholder_due_to_inconclusive_benchmark"
    dataset_version: str = "v0.3"
    method: str = "QLoRA" # "Full", "LoRA", "QLoRA"
    learning_rate: float = 2e-4
    batch_size: int = 4
    gradient_accumulation_steps: int = 4
    epochs: int = 3
    max_seq_length: int = 2048
    seed: int = 42
    lora: Optional[LoRAConfig] = None
    quantization: Optional[QuantizationConfig] = None

    def __post_init__(self):
        if self.method in ["LoRA", "QLoRA"] and self.lora is None:
            self.lora = LoRAConfig()
        if self.method == "QLoRA" and self.quantization is None:
            self.quantization = QuantizationConfig()

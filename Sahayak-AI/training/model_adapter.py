from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseModelAdapter(ABC):
    """
    Abstract adapter for local open-source models (Qwen, Phi, etc.).
    Ensures model-agnostic SFT pipeline design.
    """
    
    @abstractmethod
    def load_model(self, model_id: str, quantization_config: Dict[str, Any] = None) -> Any:
        pass
        
    @abstractmethod
    def tokenize(self, text: str) -> Any:
        pass
        
    @abstractmethod
    def prepare_training_batch(self, batch: Any) -> Any:
        pass
        
    @abstractmethod
    def forward(self, inputs: Any) -> Any:
        pass
        
    @abstractmethod
    def save_checkpoint(self, path: str) -> None:
        pass
        
    @abstractmethod
    def load_checkpoint(self, path: str) -> None:
        pass
        
    @abstractmethod
    def generate(self, prompt: str, max_new_tokens: int = 128) -> str:
        pass
        
    @abstractmethod
    def release(self) -> None:
        pass

class QwenCandidateAdapter(BaseModelAdapter):
    def load_model(self, model_id: str, quantization_config: Dict[str, Any] = None):
        raise NotImplementedError("Phase 13B Benchmark inconclusive. Model weights not loaded.")
        
    def tokenize(self, text: str): pass
    def prepare_training_batch(self, batch): pass
    def forward(self, inputs): pass
    def save_checkpoint(self, path): pass
    def load_checkpoint(self, path): pass
    def generate(self, prompt, max_new_tokens=128): pass
    def release(self): pass

class PhiCandidateAdapter(BaseModelAdapter):
    def load_model(self, model_id: str, quantization_config: Dict[str, Any] = None):
        raise NotImplementedError("Phase 13B Benchmark inconclusive. Model weights not loaded.")
        
    def tokenize(self, text: str): pass
    def prepare_training_batch(self, batch): pass
    def forward(self, inputs): pass
    def save_checkpoint(self, path): pass
    def load_checkpoint(self, path): pass
    def generate(self, prompt, max_new_tokens=128): pass
    def release(self): pass

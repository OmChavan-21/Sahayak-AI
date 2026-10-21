from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Any, Dict
import json

class SahayakAITask(str, Enum):
    EXPLAIN_CONTENT = "EXPLAIN_CONTENT"
    ASSESS_SECURITY = "ASSESS_SECURITY"
    SUMMARIZE_EVIDENCE = "SUMMARIZE_EVIDENCE"
    SUGGEST_SAFE_NEXT_STEP = "SUGGEST_SAFE_NEXT_STEP"
    GENERATE_DRAFT = "GENERATE_DRAFT"

class SahayakAIConfidence(str, Enum):
    HIGH_CONFIDENCE = "HIGH_CONFIDENCE"
    MEDIUM_CONFIDENCE = "MEDIUM_CONFIDENCE"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    UNABLE_TO_DETERMINE = "UNABLE_TO_DETERMINE"

class SahayakCapability(str, Enum):
    READ_USER_INPUT = "READ_USER_INPUT"
    READ_SHARED_CONTENT = "READ_SHARED_CONTENT"
    READ_SELECTED_IMAGE = "READ_SELECTED_IMAGE"
    READ_SELECTED_DOCUMENT = "READ_SELECTED_DOCUMENT"
    EXTRACT_TEXT = "EXTRACT_TEXT"
    EXTRACT_EVIDENCE = "EXTRACT_EVIDENCE"
    ANALYZE_SECURITY = "ANALYZE_SECURITY"
    HIGHLIGHT_EVIDENCE = "HIGHLIGHT_EVIDENCE"
    EXPLAIN_CONTENT = "EXPLAIN_CONTENT"
    CREATE_DRAFT = "CREATE_DRAFT"
    CREATE_CHECKLIST = "CREATE_CHECKLIST"
    CREATE_REMINDER = "CREATE_REMINDER"
    SAVE_SECURITY_EVENT = "SAVE_SECURITY_EVENT"
    GENERATE_REPORT_DRAFT = "GENERATE_REPORT_DRAFT"
    INSPECT_URL = "INSPECT_URL"
    READ_NOTIFICATION = "READ_NOTIFICATION"
    READ_BROWSER_CONTEXT = "READ_BROWSER_CONTEXT"
    CAMERA_CAPTURE = "CAMERA_CAPTURE"
    MICROPHONE_INPUT = "MICROPHONE_INPUT"
    CONTACT_SELECTION = "CONTACT_SELECTION"
    FILE_SELECTION = "FILE_SELECTION"
    SEND_MESSAGE = "SEND_MESSAGE"
    SUBMIT_REPORT = "SUBMIT_REPORT"
    MAKE_PAYMENT = "MAKE_PAYMENT"
    CHANGE_ACCOUNT_INFORMATION = "CHANGE_ACCOUNT_INFORMATION"
    EXECUTE_CODE = "EXECUTE_CODE"

@dataclass
class RiskIndicator:
    type: str
    evidence: str
    description: str

@dataclass
class SahayakAISecurityContext:
    deterministicRiskLevel: str
    securityIndicators: List[RiskIndicator] = field(default_factory=list)
    
@dataclass
class Evidence:
    type: str
    value: str
    sourceSnippet: str

@dataclass
class SahayakAIRequest:
    task: SahayakAITask
    securityContext: SahayakAISecurityContext
    observedEvidence: List[Evidence]
    untrustedContent: str

@dataclass
class SahayakAIRecommendation:
    safeNextStep: str
    requestedCapability: Optional[SahayakCapability] = None
    capabilityReason: Optional[str] = None

@dataclass
class SahayakAIResponse:
    assessment: str
    explanation: str
    evidenceReferences: List[str]
    confidence: SahayakAIConfidence
    recommendation: Optional[SahayakAIRecommendation] = None

@dataclass
class ProvenanceMetadata:
    scenario_family_id: str
    template_family_id: str
    security_pattern_id: str
    language_variant: str
    content_type: str
    intent_type: str

@dataclass
class TrainingExample:
    input_context: SahayakAIRequest
    expected_output: SahayakAIResponse
    metadata: ProvenanceMetadata

    def to_json(self):
        class EnhancedJSONEncoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, Enum):
                    return o.value
                if hasattr(o, '__dict__'):
                    return {k: v for k, v in o.__dict__.items() if v is not None}
                return super().default(o)
                
        return json.dumps(self, cls=EnhancedJSONEncoder)

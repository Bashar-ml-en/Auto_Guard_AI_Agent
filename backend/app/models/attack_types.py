"""Taxonomy of Adversarial Attack Vectors and Vulnerability Categories."""
from enum import Enum

class AttackCategory(str, Enum):
    """Categorization of LLM vulnerability vectors."""
    DIRECT_PROMPT_INJECTION = "direct_prompt_injection"
    INDIRECT_ENCODED_INJECTION = "indirect_encoded_injection"
    JAILBREAK_ROLEPLAY = "jailbreak_roleplay"
    PII_DATA_LEAKAGE = "pii_data_leakage"
    SYSTEM_PROMPT_EXTRACTION = "system_prompt_extraction"
    TOOL_POISONING_TAMPERING = "tool_poisoning_tampering"
    HALLUCINATION_GROUNDING_TRAP = "hallucination_grounding_trap"
    TOXICITY_POLICY_VIOLATION = "toxicity_policy_violation"

class SeverityLevel(str, Enum):
    """Vulnerability severity classification."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    SAFE = "SAFE"

class DAGStepStatus(str, Enum):
    """Status states for DAG nodes in the autonomous workflow."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SELF_HEALING = "SELF_HEALING"
    SKIPPED = "SKIPPED"

class AuditTaskStatus(str, Enum):
    """Overall status of the AutoGuard Taskmaster session."""
    QUEUED = "QUEUED"
    PLANNING = "PLANNING"
    RED_TEAMING = "RED_TEAMING"
    EVALUATING = "EVALUATING"
    OPTIMIZING = "OPTIMIZING"
    DEPLOYING = "DEPLOYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

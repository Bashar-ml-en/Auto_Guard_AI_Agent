"""Pydantic data schemas for AutoGuard AI."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from backend.app.models.attack_types import AttackCategory, SeverityLevel, DAGStepStatus, AuditTaskStatus

class TargetApplicationConfig(BaseModel):
    """Configuration blueprint of the target AI application to red-team."""
    app_name: str = Field(..., description="Name of the target AI application")
    domain: str = Field(default="Customer Support", description="Industry domain (e.g. Fintech, Healthcare, E-commerce)")
    system_prompt: str = Field(..., description="The initial system prompt under evaluation")
    sensitive_data: List[str] = Field(default_factory=list, description="Mock secrets or PII that must never be leaked")
    domain_rules: List[str] = Field(default_factory=list, description="Business rules and restrictions")
    allowed_tools: List[str] = Field(default_factory=list, description="Tool names the agent is permitted to call")

class AttackVector(BaseModel):
    """An adversarial payload designed to test a specific vulnerability."""
    id: str
    category: AttackCategory
    name: str
    description: str
    payload: str
    expected_safe_behavior: str
    base_severity: SeverityLevel = SeverityLevel.HIGH

class ProbeResult(BaseModel):
    """Result of running a single attack vector against the target system prompt."""
    attack_id: str
    category: AttackCategory
    payload: str
    model_response: str
    is_vulnerable: bool
    detected_severity: SeverityLevel
    evaluation_reasoning: str
    latency_ms: float = 0.0
    tokens_used: int = 0

class VulnerabilityCluster(BaseModel):
    """Aggregated group of vulnerabilities sharing a common exploit vector."""
    category: AttackCategory
    total_probes: int
    failed_probes: int
    vulnerability_rate: float
    severity: SeverityLevel
    summary_of_weakness: str
    recommended_patch: str

class OptimizationIteration(BaseModel):
    """Record of an evolutionary self-healing prompt mutation."""
    iteration_number: int
    prompt_before: str
    prompt_after: str
    safety_score_before: float
    safety_score_after: float
    defensive_mechanisms_added: List[str]
    critic_notes: str

class CategoryScore(BaseModel):
    """Safety scorecard per vulnerability category."""
    category: AttackCategory
    initial_pass_rate: float
    hardened_pass_rate: float
    status: str

class AuditScorecard(BaseModel):
    """Comprehensive safety and resilience evaluation report."""
    initial_safety_score: float
    final_safety_score: float
    total_attacks_executed: int
    vulnerabilities_identified: int
    vulnerabilities_patched: int
    optimization_iterations: int
    category_breakdown: List[CategoryScore]
    compliance_certificate_id: str
    verified_at: datetime = Field(default_factory=datetime.utcnow)

class DAGNode(BaseModel):
    """An individual step in the autonomous execution graph."""
    id: str
    name: str
    agent: str
    status: DAGStepStatus = DAGStepStatus.PENDING
    description: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: float = 0.0
    output_summary: Optional[str] = None
    error_message: Optional[str] = None

class ExecutionEvent(BaseModel):
    """Streaming telemetry event emitted during workflow execution."""
    task_id: str
    event_type: str  # e.g., "dag_update", "log", "probe_complete", "optimization_step", "deployment"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    step_id: Optional[str] = None
    message: str
    data: Optional[Dict[str, Any]] = None

class StartAuditRequest(BaseModel):
    """Request payload to initiate an autonomous audit task."""
    target_app: TargetApplicationConfig
    target_safety_score: float = 95.0
    max_iterations: int = 3

class DeployRequest(BaseModel):
    """Request to deploy the hardened agent to Google Cloud Run."""
    task_id: str
    service_name: Optional[str] = None
    region: Optional[str] = "us-central1"

class AuditTaskState(BaseModel):
    """Full state of an autonomous AutoGuard Taskmaster session."""
    task_id: str
    status: AuditTaskStatus
    target_app: TargetApplicationConfig
    initial_system_prompt: str
    hardened_system_prompt: Optional[str] = None
    dag_nodes: List[DAGNode]
    attack_vectors: List[AttackVector] = Field(default_factory=list)
    initial_probe_results: List[ProbeResult] = Field(default_factory=list)
    final_probe_results: List[ProbeResult] = Field(default_factory=list)
    vulnerability_clusters: List[VulnerabilityCluster] = Field(default_factory=list)
    optimization_history: List[OptimizationIteration] = Field(default_factory=list)
    scorecard: Optional[AuditScorecard] = None
    cloud_run_url: Optional[str] = None
    gcs_report_uri: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

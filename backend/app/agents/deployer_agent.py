"""Deployment and Artifact Generation Agent."""
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List
from backend.app.models.schemas import (
    AuditTaskState, AuditScorecard, CategoryScore, TargetApplicationConfig
)
from backend.app.services.storage_service import storage_service
from backend.app.services.firestore_service import firestore_service
from backend.app.services.cloud_run_service import cloud_run_service

logger = logging.getLogger("autoguard.deployer")

class DeployerAgent:
    """Agent responsible for artifact export, compliance certification, and Cloud Run deployment."""

    def __init__(self):
        self.storage = storage_service
        self.firestore = firestore_service
        self.cloud_run = cloud_run_service

    async def generate_and_store_scorecard(
        self,
        task_id: str,
        target_app: TargetApplicationConfig,
        initial_score: float,
        final_score: float,
        total_attacks: int,
        vulnerabilities_found: int,
        vulnerabilities_patched: int,
        iterations: int,
        category_scores: List[CategoryScore],
        hardened_prompt: str
    ) -> AuditScorecard:
        """Generate official security scorecard and persist to Cloud Storage."""
        cert_id = f"AG-CERT-{uuid.uuid4().hex[:8].upper()}"
        scorecard = AuditScorecard(
            initial_safety_score=initial_score,
            final_safety_score=final_score,
            total_attacks_executed=total_attacks,
            vulnerabilities_identified=vulnerabilities_found,
            vulnerabilities_patched=vulnerabilities_patched,
            optimization_iterations=iterations,
            category_breakdown=category_scores,
            compliance_certificate_id=cert_id,
            verified_at=datetime.utcnow()
        )

        # Upload scorecard package to Cloud Storage / local store
        await self.storage.save_audit_scorecard(
            task_id=task_id,
            scorecard=scorecard.model_dump(mode="json"),
            hardened_prompt=hardened_prompt
        )

        return scorecard

    async def deploy_to_cloud_run(
        self,
        task_id: str,
        app_name: str,
        hardened_prompt: str,
        service_name: str = None
    ) -> Dict[str, Any]:
        """Deploy the hardened agent microservice to Google Cloud Run."""
        return await self.cloud_run.package_and_deploy_agent(
            task_id=task_id,
            app_name=app_name,
            hardened_prompt=hardened_prompt,
            service_name=service_name
        )

deployer_agent = DeployerAgent()

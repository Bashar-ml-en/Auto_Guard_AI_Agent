"""Google Cloud Storage (GCS) artifact management with local export fallback."""
import os
import json
import logging
from typing import Dict, Any
from backend.app.config import settings

logger = logging.getLogger("autoguard.storage")

class StorageService:
    """Artifact exporter for Cloud Storage and local audits."""

    def __init__(self):
        self.bucket_name = settings.gcs_bucket_name
        self.client = None
        self.local_artifact_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "artifacts")
        os.makedirs(self.local_artifact_dir, exist_ok=True)
        self._init_storage()

    def _init_storage(self):
        """Connect to Google Cloud Storage if available."""
        try:
            from google.cloud import storage
            self.client = storage.Client(project=settings.google_cloud_project)
            logger.info(f"Connected to Google Cloud Storage (Bucket: {self.bucket_name})")
        except Exception as e:
            logger.info(f"Cloud Storage client not active ({e}). Using local artifact cache directory: {self.local_artifact_dir}")
            self.client = None

    async def upload_audit_artifact(self, task_id: str, filename: str, content: str, content_type: str = "application/json") -> str:
        """Save artifact to Cloud Storage (or local storage fallback) and return URI."""
        # 1. Always save a local copy for instant offline access
        task_dir = os.path.join(self.local_artifact_dir, task_id)
        os.makedirs(task_dir, exist_ok=True)
        local_path = os.path.join(task_dir, filename)
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(content)

        # 2. Upload to GCS bucket if available
        if self.client:
            try:
                bucket = self.client.bucket(self.bucket_name)
                blob = bucket.blob(f"audits/{task_id}/{filename}")
                blob.upload_from_string(content, content_type=content_type)
                gcs_uri = f"gs://{self.bucket_name}/audits/{task_id}/{filename}"
                logger.info(f"Uploaded artifact to GCS: {gcs_uri}")
                return gcs_uri
            except Exception as e:
                logger.warning(f"GCS upload failed: {e}. Defaulting to local path.")

        return f"file://{local_path.replace(os.sep, '/')}"

    async def save_audit_scorecard(self, task_id: str, scorecard: Dict[str, Any], hardened_prompt: str) -> Dict[str, str]:
        """Save comprehensive audit package containing scorecard, dataset, and hardened prompt."""
        json_uri = await self.upload_audit_artifact(
            task_id=task_id,
            filename="scorecard.json",
            content=json.dumps(scorecard, indent=2),
            content_type="application/json"
        )

        prompt_uri = await self.upload_audit_artifact(
            task_id=task_id,
            filename="hardened_system_prompt.txt",
            content=hardened_prompt,
            content_type="text/plain"
        )

        return {
            "scorecard_uri": json_uri,
            "hardened_prompt_uri": prompt_uri
        }

storage_service = StorageService()

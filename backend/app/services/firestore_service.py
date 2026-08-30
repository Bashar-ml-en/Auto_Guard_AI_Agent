"""Google Cloud Firestore persistence service with in-memory fallback."""
import logging
from typing import Optional, Dict, Any, List
from backend.app.config import settings
from backend.app.models.schemas import AuditTaskState

logger = logging.getLogger("autoguard.firestore")

class FirestoreService:
    """Enterprise state management for AutoGuard Taskmaster workflows."""

    def __init__(self):
        self.project_id = settings.google_cloud_project
        self.db = None
        self._memory_store: Dict[str, Dict[str, Any]] = {}
        self._init_firestore()

    def _init_firestore(self):
        """Connect to Google Cloud Firestore if credentials/project are configured."""
        try:
            from google.cloud import firestore
            self.db = firestore.AsyncClient(project=self.project_id)
            logger.info(f"Connected to Google Cloud Firestore (Project: {self.project_id})")
        except Exception as e:
            logger.info(f"Cloud Firestore not initialized ({e}). Utilizing persistent in-memory state engine.")
            self.db = None

    async def save_task_state(self, task_id: str, state: AuditTaskState) -> None:
        """Persist full audit task state to Firestore."""
        data = state.model_dump(mode="json")
        self._memory_store[task_id] = data

        if self.db:
            try:
                doc_ref = self.db.collection("autoguard_tasks").document(task_id)
                await doc_ref.set(data)
                logger.debug(f"Saved state to Firestore for task: {task_id}")
            except Exception as e:
                logger.warning(f"Failed to persist state to Cloud Firestore: {e}")

    async def get_task_state(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve task state from Firestore or in-memory fallback."""
        if self.db:
            try:
                doc_ref = self.db.collection("autoguard_tasks").document(task_id)
                doc = await doc_ref.get()
                if doc.exists:
                    return doc.to_dict()
            except Exception as e:
                logger.warning(f"Error fetching from Cloud Firestore: {e}")

        return self._memory_store.get(task_id)

    async def list_recent_tasks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """List recently executed audit workflows."""
        if self.db:
            try:
                query = self.db.collection("autoguard_tasks").order_by("created_at", direction="DESCENDING").limit(limit)
                docs = await query.get()
                return [d.to_dict() for d in docs]
            except Exception as e:
                logger.warning(f"Error listing tasks from Firestore: {e}")

        # Return from memory store sorted by updated_at
        tasks = list(self._memory_store.values())
        return tasks[:limit]

firestore_service = FirestoreService()

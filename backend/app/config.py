"""Configuration management for AutoGuard AI."""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment or defaults."""
    app_name: str = "AutoGuard AI"
    version: str = "1.0.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # Gemini / Google GenAI SDK Configuration
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")
    
    # Google Cloud Platform Configuration
    google_cloud_project: str = os.getenv("GOOGLE_CLOUD_PROJECT", "autoguard-hackathon-demo")
    google_cloud_region: str = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
    gcs_bucket_name: str = os.getenv("GCS_BUCKET_NAME", "autoguard-audit-artifacts")
    cloud_run_service_name: str = os.getenv("CLOUD_RUN_SERVICE_NAME", "autoguard-fortified-agent")
    
    # Server Settings
    port: int = int(os.getenv("PORT", "8000"))
    host: str = os.getenv("HOST", "0.0.0.0")
    
    # Execution & Safety Thresholds
    target_safety_score: float = float(os.getenv("TARGET_SAFETY_SCORE", "95.0"))
    max_optimization_iterations: int = int(os.getenv("MAX_OPTIMIZATION_ITERATIONS", "3"))
    max_parallel_probes: int = int(os.getenv("MAX_PARALLEL_PROBES", "12"))
    
    # Mock / Fallback Mode (allows running seamless demo even without live GCP billing setup)
    enable_mock_fallback: bool = os.getenv("ENABLE_MOCK_FALLBACK", "true").lower() in ("true", "1", "yes")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

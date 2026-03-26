import os
import json
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


class AxonConfig:
    """
    Configuration loader for Axon.
    Handles environment variables from .env and student profile data from data/config.json.
    """

    def __init__(self, config_path: str = "data/config.json"):
        # Load environment variables from .env
        load_dotenv()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        self.config_path = Path(config_path)
        self._data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Reads the JSON configuration file with robust error handling."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found at {self.config_path}. "
                "Please ensure data/config.json exists with the required student profile structure."
            )

        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse {self.config_path}: {str(e)}")

    @property
    def full_name(self) -> str:
        """Returns the full name from the user profile."""
        return self._data.get("user_profile", {}).get("full_name", "Unknown")

    @property
    def student_id(self) -> str:
        """Returns the student ID from the user profile."""
        return self._data.get("user_profile", {}).get("student_id", "00-00000")

    @property
    def primary_role(self) -> str:
        """Returns the primary role from the roles configuration."""
        return self._data.get("roles", {}).get("primary", "Student")

    @property
    def context_header(self) -> str:
        """Returns a formatted string representing the user's current context."""
        return f"{self.full_name} | {self.student_id} | {self.primary_role}"

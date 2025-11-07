from __future__ import annotations
from pathlib import Path
from typing import Optional
import configparser

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


_BASE_DIR = Path(__file__).parent
_DEFAULT_INI = _BASE_DIR / "config.ini"


class AppSettings(BaseSettings):
    """Application settings backed by pydantic-settings.

    Precedence (highest first):
      1. init kwargs (explicit programmatic overrides)
      2. environment variables (e.g. API_KEY)
      3. config.ini (DEFAULT section and optional [app] section)
      4. model defaults
    """

    model_config = SettingsConfigDict(env_prefix="", env_file=".env", case_sensitive=False)

    # configuration fields (add or adapt as needed)
    api_key: Optional[str] = Field(None, description="API key for external service")
    model_name: str = Field("gpt-4", description="Default model name")
    debug: bool = Field(False, description="Enable debug logging")
    db_url: Optional[str] = Field(None, description="Database URL")
    timeout_seconds: int = Field(30, description="Request timeout in seconds")

    @staticmethod
    def _load_ini(path: Path) -> dict:
        """Read config.ini and return a flat dict (lowercased keys).

        Reads the DEFAULT section and an optional [app] section.
        """
        cp = configparser.ConfigParser()
        if not path.exists():
            return {}
        cp.read(path)
        data: dict = {}
        # defaults() returns mappings from DEFAULT section
        for k, v in cp.defaults().items():
            data[k.lower()] = v
        if cp.has_section("app"):
            for k, v in cp.items("app"):
                data[k.lower()] = v
        return data

    @classmethod
    def settings_customise_sources(cls, init_settings, env_settings, file_secret_settings):
        """Customize sources so precedence is: init -> env -> ini -> file_secret.

        pydantic-settings calls these source callables in order and uses the first
        value found for each field. Returning sources in this order ensures
        environment variables override INI values while still allowing explicit
        init kwargs to be the highest priority.
        """

        def _ini_source():
            return cls._load_ini(_DEFAULT_INI)

        # order: init_settings (highest), env_settings, ini, file_secret_settings
        return init_settings, env_settings, _ini_source, file_secret_settings


# simple singleton getter for convenience; call this once at startup
_SETTINGS: Optional[AppSettings] = None


def get_settings(reload: bool = False) -> AppSettings:
    """Return a singleton AppSettings instance.

    If reload=True, re-read environment and INI file.
    """
    global _SETTINGS
    if _SETTINGS is None or reload:
        # init without kwargs so settings_customise_sources controls precedence
        _SETTINGS = AppSettings()
    return _SETTINGS


if __name__ == "__main__":
    # very small smoke-test when module executed directly
    s = get_settings()
    print("Loaded settings:")
    print(s.model_dump_json(indent=2))

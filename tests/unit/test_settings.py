"""Settings'in üç kaynaktan doğru sırayla okuduğunu kanıtlar:
kod içi varsayılan < .env dosyası < gerçek ortam değişkeni.
"""

from pathlib import Path

import pytest

from apps.api.config.settings import Settings


def test_settings_uses_code_default(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Çalışma dizininde .env dosyası yokken, kod içindeki varsayılan değer kullanılır."""
    monkeypatch.chdir(tmp_path)
    settings = Settings()
    assert settings.environment == "local"


def test_settings_reads_env_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """.env dosyasındaki değer, kod içi varsayılanı ezer."""
    (tmp_path / ".env").write_text("ENVIRONMENT=staging\n")
    monkeypatch.chdir(tmp_path)

    settings = Settings()
    assert settings.environment == "staging"


def test_real_env_var_overrides_env_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Gerçek bir ortam değişkeni, .env dosyasındaki değeri bile ezer."""
    (tmp_path / ".env").write_text("ENVIRONMENT=staging\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("ENVIRONMENT", "production")

    settings = Settings()
    assert settings.environment == "production"

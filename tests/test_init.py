"""Tests for Init command."""

from unittest.mock import patch

from codefox.api.model_enum import ModelEnum
from codefox.cli.init import Init


def test_init_normalizes_none_args() -> None:
    with patch.object(Init, "_ask_model", return_value=ModelEnum.GEMINI):
        init = Init()

    assert init.model_enum is ModelEnum.GEMINI
    assert init.api_class is ModelEnum.GEMINI.api_class
    assert init.args == {}


def test_execute_uses_provider_and_token_from_args() -> None:
    init = Init({"provider": "gemini", "token": "test-token"})

    with (
        patch.object(init, "_ask_api_key") as mock_ask_api_key,
        patch.object(init, "_write_config", return_value=True) as mock_write,
        patch.object(init, "_ensure_ignore_file") as mock_ignore,
        patch.object(init, "_ensure_yaml_config") as mock_yaml,
        patch.object(init, "_ensure_gitignore") as mock_gitignore,
        patch.object(
            init, "_check_connection", return_value=True
        ) as mock_check,
    ):
        init.execute()

    mock_ask_api_key.assert_not_called()
    mock_write.assert_called_once_with("test-token")
    mock_ignore.assert_called_once()
    mock_yaml.assert_called_once()
    mock_gitignore.assert_called_once()
    mock_check.assert_called_once()

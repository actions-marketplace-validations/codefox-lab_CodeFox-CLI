"""Tests for GitLab bot."""

from unittest.mock import MagicMock, patch

import pytest

from codefox.bots.gitlab_bot import GitLabBot


def test_send_creates_merge_request_note(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITLAB_TOKEN", "token")
    monkeypatch.setenv("GITLAB_REPOSITORY", "123")
    monkeypatch.setenv("PR_NUMBER", "456")

    with patch("codefox.bots.gitlab_bot.Gitlab") as mock_gitlab_class:
        mock_project = MagicMock()
        mock_mr = MagicMock()
        mock_gitlab = mock_gitlab_class.return_value
        mock_gitlab.projects.get.return_value = mock_project
        mock_project.mergerequests.get.return_value = mock_mr

        bot = GitLabBot()
        bot.send("hello")

    mock_gitlab_class.assert_called_once_with(
        url="https://gitlab.com",
        private_token="token",
    )
    mock_gitlab.projects.get.assert_called_once_with(123)
    mock_project.mergerequests.get.assert_called_once_with(456)
    mock_mr.notes.create.assert_called_once_with({"body": "hello"})


def test_send_rejects_empty_message(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITLAB_TOKEN", "token")
    monkeypatch.setenv("GITLAB_REPOSITORY", "123")
    monkeypatch.setenv("PR_NUMBER", "456")

    with patch("codefox.bots.gitlab_bot.Gitlab"):
        bot = GitLabBot()

    with pytest.raises(ValueError, match="Message must not be empty"):
        bot.send("   ")


def test_send_raises_when_identifiers_are_not_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITLAB_TOKEN", "token")
    monkeypatch.setenv("GITLAB_REPOSITORY", "123")
    monkeypatch.setenv("PR_NUMBER", "456")

    with patch("codefox.bots.gitlab_bot.Gitlab") as mock_gitlab_class:
        bot = GitLabBot()
        bot.repository = None

        with pytest.raises(
            RuntimeError,
            match="GitLab project or merge request is not configured",
        ):
            bot.send("hello")

    mock_gitlab_class.return_value.projects.get.assert_not_called()

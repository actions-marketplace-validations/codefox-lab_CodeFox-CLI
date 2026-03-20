import os

from gitlab import Gitlab
from gitlab.exceptions import GitlabCreateError, GitlabGetError


class GitLabBot:
    def __init__(self) -> None:
        self.gitlab_token = os.getenv("GITLAB_TOKEN")
        self.gitlab_url = os.getenv("GITLAB_URL", "https://gitlab.com")
        self.repository = os.getenv("GITLAB_REPOSITORY")
        self.mr_iid = os.getenv("PR_NUMBER")

        if not self.gitlab_token:
            raise ValueError(
                "GITLAB_TOKEN environment variable is not set. "
                "This token is required to authenticate with the GitLab API."
            )

        if not self.repository or not self.repository.isdigit():
            raise ValueError(f"Invalid GITLAB_REPOSITORY: {self.repository!r}")

        if not self.mr_iid or not self.mr_iid.isdigit():
            raise ValueError(
                f"Invalid PR_NUMBER value: {self.mr_iid!r}. "
                "Expected a numeric merge request IID."
            )

        self.gitlab = Gitlab(
            url=self.gitlab_url,
            private_token=self.gitlab_token,
        )

    def send(self, message: str) -> None:
        if not message or not message.strip():
            raise ValueError("Message must not be empty.")

        repository = self.repository
        mr_iid = self.mr_iid

        if repository is None or mr_iid is None:
            raise RuntimeError(
                "GitLab project or merge request is not configured."
            )

        try:
            project = self.gitlab.projects.get(int(repository))
            mr = project.mergerequests.get(int(mr_iid))
            mr.notes.create({"body": message})
        except GitlabGetError as exc:
            raise RuntimeError(
                f"Failed to find project '{repository}' "
                f"or merge request IID {mr_iid}."
            ) from exc
        except GitlabCreateError as exc:
            raise RuntimeError("Failed to create merge request note.") from exc

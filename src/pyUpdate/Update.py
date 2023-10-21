import os
import subprocess
import sys
from typing import Optional

import requests


class GitHubRepo:
    """
    A class that represents a GitHub repository.

    Attributes:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        local_repo_path (str): The path to the local copy of the repository.
    """

    def __init__(self, owner: str, repo: str, local_repo_path: str):
        self.owner = owner
        self.repo = repo
        self.local_repo_path = local_repo_path

    def get_latest_version(self) -> str:
        """
        Get the latest release version from GitHub.

        Returns:
            str: The tag name of the latest release version.
        """
        response = requests.get(
            f"https://api.github.com/repos/{self.owner}/{self.repo}/releases/latest"
        )
        return response.json()["tag_name"]

    def pull_latest_version(self) -> None:
        """
        Pull the latest version from GitHub to the local repository.
        """
        os.chdir(self.local_repo_path)
        subprocess.run(["git", "pull", "origin", "master"], check=True)

    def restart_application(self) -> None:
        """
        Restart the application.
        """
        os.execv(sys.executable, ["python"] + sys.argv)

    def update_application(self) -> None:
        """
        Update the application if the current version is not the latest.
        """
        latest_version = self.get_latest_version()
        current_version = self.get_current_version()

        if current_version != latest_version:
            self.pull_latest_version()
            self.restart_application()

    def get_current_version(self) -> str:
        """
        Get the current version of the local Git repository.

        Returns:
            str: The commit ID of the current HEAD.
        """
        os.chdir(self.local_repo_path)
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, check=True
        )

        return result.stdout.decode("utf-8").strip()


# Create a GitHubRepo object for your repository
repo = GitHubRepo("owner", "repo", "/path/to/your/local/repo")

# Update the application if necessary
repo.update_application()

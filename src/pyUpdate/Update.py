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

        response = requests.get(f"https://github.com/{owner}/{repo}")
        if response.status_code != 200:
            raise Exception(f"The provided owner and repo combination {owner}/{repo} does not correspond to a valid GitHub repository.")

        if not os.path.isdir(local_repo_path):
            raise Exception(f"The provided path {local_repo_path} is not a valid directory.")
        
        if not os.path.isdir(os.path.join(local_repo_path, ".git")):
            raise Exception(f"The provided path {local_repo_path} does not contain a .git folder.")

        self.owner = owner
        self.repo = repo
        self.local_repo_path = local_repo_path

    def get_latest_version(self) -> Optional[str]:
        """
        Get the latest release version from GitHub.

        Returns:
            Optional[str]: The tag name of the latest release version if it exists, None otherwise.
        
        Raises:
            Exception: If the request to GitHub API fails.
        """
        response = requests.get(
            f"https://api.github.com/repos/{self.owner}/{self.repo}/releases/latest"
        )

        if response.status_code != 200:
            raise Exception("Failed to get the latest version from GitHub.")

        response_json = response.json()
        return response_json.get("tag_name")

    def pull_latest_version(self) -> None:
        """
        Pull the latest version from GitHub to the local repository.

        Raises:
            Exception: If the git pull command fails.
        """
        os.chdir(self.local_repo_path)
        
        result = subprocess.run(["git", "pull", "origin", "master"], check=True)

        if result.returncode != 0:
            raise Exception("Failed to pull the latest version from GitHub.")

    def restart_application(self) -> None:
        """
        Restart the application.

        Raises:
            Exception: If the application fails to restart.
        """
        
        try:
            os.execv(sys.executable, ["python"] + sys.argv)
        
        except Exception as e:
            raise Exception("Failed to restart the application.") from e

    def update_application(self) -> None:
        """
        Update the application if the current version is not the latest.

        Raises:
            Exception: If it fails to update the application.
        """
        
        try:
            latest_version = self.get_latest_version()
            current_version = self.get_current_version()

            if current_version != latest_version:
                self.pull_latest_version()
                self.restart_application()
        
        except Exception as e:
            raise Exception("Failed to update the application.") from e

    def get_current_version(self) -> Optional[str]:
        """
        Get the current version of the local Git repository.

        Returns:
            Optional[str]: The commit ID of the current HEAD if it exists, None otherwise.
        
        Raises:
            Exception: If it fails to get the current version.
        """
        
        os.chdir(self.local_repo_path)
        
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, check=True
            )
            
            return result.stdout.decode("utf-8").strip()
        
        except subprocess.CalledProcessError as e:
            raise Exception("Failed to get the current version.") from e

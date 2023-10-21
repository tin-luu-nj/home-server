import os
import subprocess
import sys
import unittest
from unittest.mock import MagicMock, patch

from src.pyUpdate import GitHubRepo


class TestGitHubRepo_init(unittest.TestCase):
    @patch("requests.get")
    def test_init_valid_local_repo_path(self, mock_get):
        # Arrange
        mock_get.return_value.status_code = 200
        owner = "tin-luu-nj"
        repo = "home-server"
        local_repo_path = "."

        # Act
        github_repo = GitHubRepo(owner, repo, local_repo_path)

        # Assert
        self.assertEqual(github_repo.owner, owner)
        self.assertEqual(github_repo.repo, repo)
        self.assertEqual(github_repo.local_repo_path, local_repo_path)

    @patch("requests.get")
    def test_init_invalid_github_repo(self, mock_get):
        # Arrange
        mock_get.return_value.status_code = 404
        owner = "test_owner"
        repo = "test_repo"
        local_repo_path = "/path/to/local/repo"

        # Act & Assert
        with self.assertRaises(Exception):
            GitHubRepo(owner, repo, local_repo_path)

    @patch("requests.get")
    @patch("os.path.isdir")
    def test_init_invalid_local_repo_path(self, mock_isdir, mock_get):
        # Arrange
        mock_get.return_value.status_code = 200
        mock_isdir.return_value = False
        owner = "test_owner"
        repo = "test_repo"
        local_repo_path = "/invalid/path"

        # Act & Assert
        with self.assertRaises(Exception):
            GitHubRepo(owner, repo, local_repo_path)

    @patch("requests.get")
    @patch("os.path.isdir")
    def test_init_no_git_folder(self, mock_isdir, mock_get):
        # Arrange
        mock_get.return_value.status_code = 200
        mock_isdir.side_effect = [
            True,
            False,
        ]  # First call (for local_repo_path) returns True, second call (for .git folder) returns False.
        owner = "test_owner"
        repo = "test_repo"
        local_repo_path = "/path/to/local/repo"

        # Act & Assert
        with self.assertRaises(Exception):
            GitHubRepo(owner, repo, local_repo_path)


class TestGitHubRepo(unittest.TestCase):
    @patch("requests.get")
    @patch("os.path.isdir")
    def setUp(self, mock_isdir, mock_get):
        # Arrange
        mock_get.return_value.status_code = 200
        mock_isdir.side_effect = [
            True,
            True,
        ]  # First call (for local_repo_path) returns True, second call (for .git folder) returns True.
        self.repo = GitHubRepo("owner", "repo", "/path/to/repo")

    @patch("requests.get")
    def test_get_latest_version(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"tag_name": "v1.0.0"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        version = self.repo.get_latest_version()

        self.assertEqual(version, "v1.0.0")
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/releases/latest"
        )

    @patch("os.chdir")
    @patch("subprocess.run")
    def test_pull_latest_version_success(self, mock_run, mock_chdir):
        # Arrange
        self.repo.local_repo_path = "."
        mock_run.return_value.returncode = 0

        # Act
        try:
            self.repo.pull_latest_version()
        except Exception as e:
            self.fail(f"pull_latest_version() raised Exception unexpectedly: {e}")

    @patch("os.chdir")
    @patch("subprocess.run")
    def test_pull_latest_version_failure(self, mock_run, mock_chdir):
        # Arrange
        self.repo.local_repo_path = "."
        mock_run.return_value.returncode = 1

        # Act & Assert
        with self.assertRaises(Exception):
            self.repo.pull_latest_version()

    @patch("os.execv")
    def test_restart_application_success(self, mock_execv):
        # Act
        self.repo.local_repo_path = "."
        try:
            self.repo.restart_application()
        except Exception as e:
            self.fail(f"restart_application() raised Exception unexpectedly: {e}")

        # Assert
        mock_execv.assert_called_once()

    @patch("os.execv")
    def test_restart_application_failure(self, mock_execv):
        # Arrange
        self.repo.local_repo_path = "."
        mock_execv.side_effect = Exception("Failed to restart the application.")

        # Act & Assert
        with self.assertRaises(Exception):
            self.repo.restart_application()

    @patch("os.chdir")
    @patch("subprocess.run")
    def test_get_current_version_success(self, mock_run, mock_chdir):
        # Arrange
        expected_version = "abc123"
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = expected_version.encode()

        # Act
        version = self.repo.get_current_version()

        # Assert
        self.assertEqual(version, expected_version)
        mock_chdir.assert_called_once_with(self.repo.local_repo_path)

    @patch("os.chdir")
    @patch("subprocess.run")
    def test_get_current_version_failure(self, mock_run, mock_chdir):
        # Arrange
        mock_run.side_effect = subprocess.CalledProcessError(1, "git rev-parse HEAD")

        # Act & Assert
        with self.assertRaises(Exception):
            self.repo.get_current_version()

    @patch.object(GitHubRepo, "get_latest_version")
    @patch.object(GitHubRepo, "get_current_version")
    @patch.object(GitHubRepo, "pull_latest_version")
    @patch.object(GitHubRepo, "restart_application")
    def test_update_application_success(
        self, mock_restart, mock_pull, mock_get_current, mock_get_latest
    ):
        # Arrange
        mock_get_latest.return_value = "v1.1"
        mock_get_current.return_value = "v1.0"

        # Act
        try:
            self.repo.update_application()
        except Exception as e:
            self.fail(f"update_application() raised Exception unexpectedly: {e}")

        # Assert
        mock_pull.assert_called_once()
        mock_restart.assert_called_once()

    @patch.object(GitHubRepo, "get_latest_version")
    @patch.object(GitHubRepo, "get_current_version")
    def test_update_application_no_update_needed(
        self, mock_get_current, mock_get_latest
    ):
        # Arrange
        mock_get_latest.return_value = "v1.0"
        mock_get_current.return_value = "v1.0"

        # Act
        try:
            self.repo.update_application()
        except Exception as e:
            self.fail(f"update_application() raised Exception unexpectedly: {e}")

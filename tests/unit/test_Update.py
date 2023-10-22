import os
import subprocess
import sys
from unittest.mock import MagicMock, patch

import pytest
from src.pyUpdate import GitHubRepo


@patch("requests.get")
def test_init_valid_local_repo_path(mock_get):
    # Arrange
    mock_get.return_value.status_code = 200
    owner = "tin-luu-nj"
    repo = "home-server"
    local_repo_path = "."

    # Act
    github_repo = GitHubRepo(owner, repo, local_repo_path)

    # Assert
    assert github_repo.owner == owner
    assert github_repo.repo == repo
    assert github_repo.local_repo_path == local_repo_path


@patch("requests.get")
def test_init_invalid_github_repo(mock_get):
    # Arrange
    mock_get.return_value.status_code = 404
    owner = "test_owner"
    repo = "test_repo"
    local_repo_path = "/path/to/local/repo"

    # Act & Assert
    with pytest.raises(Exception):
        GitHubRepo(owner, repo, local_repo_path)


@patch("requests.get")
@patch("os.path.isdir")
def test_init_invalid_local_repo_path(mock_isdir, mock_get):
    # Arrange
    mock_get.return_value.status_code = 200
    mock_isdir.return_value = False
    owner = "test_owner"
    repo = "test_repo"
    local_repo_path = "/invalid/path"

    # Act & Assert
    with pytest.raises(Exception):
        GitHubRepo(owner, repo, local_repo_path)


@patch("requests.get")
@patch("os.path.isdir")
def test_init_no_git_folder(mock_isdir, mock_get):
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
    with pytest.raises(Exception):
        GitHubRepo(owner, repo, local_repo_path)


@pytest.fixture
def setup():
    with patch("requests.get") as mock_get, patch("os.path.isdir") as mock_isdir:
        mock_get.return_value.status_code = 200
        mock_isdir.side_effect = [True, True]
        repo = GitHubRepo("owner", "repo", "/path/to/repo")
    return repo


@patch("requests.get")
def test_get_latest_version(mock_get, setup):
    mock_response = MagicMock()
    mock_response.json.return_value = {"tag_name": "v1.0.0"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    version = setup.get_latest_version()

    assert version == "v1.0.0"
    mock_get.assert_called_once_with(
        "https://api.github.com/repos/owner/repo/releases/latest"
    )


@patch("os.chdir")
@patch("subprocess.run")
def test_pull_latest_version_success(mock_run, mock_chdir, setup):
    setup.local_repo_path = "."
    mock_run.return_value.returncode = 0

    try:
        setup.pull_latest_version()
    except Exception as e:
        pytest.fail(f"pull_latest_version() raised Exception unexpectedly: {e}")


@patch("os.chdir")
@patch("subprocess.run")
def test_pull_latest_version_failure(mock_run, mock_chdir, setup):
    setup.local_repo_path = "."
    mock_run.return_value.returncode = 1

    with pytest.raises(Exception):
        setup.pull_latest_version()


@patch("os.execv")
def test_restart_application_success(mock_execv, setup):
    setup.local_repo_path = "."
    try:
        setup.restart_application()
    except Exception as e:
        pytest.fail(f"restart_application() raised Exception unexpectedly: {e}")

    mock_execv.assert_called_once()


@patch("os.execv")
def test_restart_application_failure(mock_execv, setup):
    setup.local_repo_path = "."
    mock_execv.side_effect = Exception("Failed to restart the application.")

    with pytest.raises(Exception):
        setup.restart_application()


@patch("os.chdir")
@patch("subprocess.run")
def test_get_current_version_success(mock_run, mock_chdir, setup):
    expected_version = "abc123"
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = expected_version.encode()

    version = setup.get_current_version()

    assert version == expected_version
    mock_chdir.assert_called_once_with(setup.local_repo_path)


@patch("os.chdir")
@patch("subprocess.run")
def test_get_current_version_failure(mock_run, mock_chdir, setup):
    mock_run.side_effect = subprocess.CalledProcessError(1, "git rev-parse HEAD")

    with pytest.raises(Exception):
        setup.get_current_version()


@patch.object(GitHubRepo, "get_latest_version")
@patch.object(GitHubRepo, "get_current_version")
@patch.object(GitHubRepo, "pull_latest_version")
@patch.object(GitHubRepo, "restart_application")
def test_update_application_success(
    mock_restart, mock_pull, mock_get_current, mock_get_latest, setup
):
    # Arrange
    mock_get_latest.return_value = "v1.1"
    mock_get_current.return_value = "v1.0"

    # Act
    try:
        setup.update_application()
    except Exception as e:
        pytest.fail(f"update_application() raised Exception unexpectedly: {e}")

    # Assert
    mock_pull.assert_called_once()
    mock_restart.assert_called_once()


@patch.object(GitHubRepo, "get_latest_version")
@patch.object(GitHubRepo, "get_current_version")
def test_update_application_no_update_needed(mock_get_current, mock_get_latest, setup):
    # Arrange
    mock_get_latest.return_value = "v1.0"
    mock_get_current.return_value = "v1.0"

    # Act
    try:
        setup.update_application()
    except Exception as e:
        pytest.fail(f"update_application() raised Exception unexpectedly: {e}")

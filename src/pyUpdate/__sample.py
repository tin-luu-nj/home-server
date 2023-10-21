from Update import *

# Create a GitHubRepo object for your repository
repo = GitHubRepo("tin-luu-nj", "home-server", ".")

# Update the application if necessary
repo.update_application()

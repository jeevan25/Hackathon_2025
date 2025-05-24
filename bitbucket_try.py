import os
import git
import requests
from datetime import datetime
from dotenv import load_dotenv

# === CONFIG ===
load_dotenv(override=True)

def create_branch_with_file_changes(new_branch_name, file_changes):
    repo = git.Repo(os.getenv("LOCAL_REPO_PATH"))
    origin = repo.remote(name='origin')

    new_branch = repo.create_head(new_branch_name)
    new_branch.checkout()

    # Apply file changes
    for filename, content in file_changes.items():
        file_path = os.path.join(os.getenv("LOCAL_REPO_PATH"), filename)
        with open(file_path, 'w') as f:
            f.write(content)

    # Commit and push
    repo.git.add(A=True)
    repo.index.commit(f"Automated commit to {new_branch_name}")
    origin.push(new_branch_name)
    
    print(f"Branch {new_branch_name} created and pushed successfully.")

# create_branch_with_file_changes(NEW_BRANCH_NAME, FILE_CHANGES)

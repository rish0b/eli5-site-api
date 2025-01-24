import os
import requests

# Function to get all filenames from a GitHub directory
def get_existing_ids_from_github(repo_owner, repo_name, access_token, directory=''):
    headers = {
        'Authorization': f'token {access_token}'
    }
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{directory}'

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        files = response.json()
        # Filter out markdown files and extract the Reddit post IDs (filename)
        return [os.path.splitext(file['name'])[0] for file in files if file['name'].endswith('.md')]
    else:
        return []

# Function to check if a Reddit post has already been written to GitHub
def is_post_already_written(post_id, existing_ids):
    return post_id in existing_ids

# Function to post a Markdown article to GitHub
def post_article_to_github(repo_owner, repo_name, access_token, post_id, content, message=''):
    headers = {
        'Authorization': f'token {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Prepare the commit data
    commit_data = {
        "message": message or f"Adding article for Reddit post {post_id}",
        "content": content,
        "branch": "main",  # Specify the branch where you want to add the new file
        "path": f"{post_id}.md"  # File name is the Reddit post ID
    }
    
    # URL to create or update a file in GitHub
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{post_id}.md'
    
    # First, check if the file already exists
    existing_files = requests.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{post_id}.md', headers=headers)
    
    if existing_files.status_code == 404:  # File does not exist
        # Create the new file
        response = requests.put(url, json=commit_data, headers=headers)
    else:
        # Update the existing file
        response = requests.put(url, json=commit_data, headers=headers)
    
    if response.status_code in [201, 200]:  # Successfully created or updated
        print(f"Article {post_id}.md successfully posted!")
        return True
    else:
        print(f"Failed to post article {post_id}.md")
        return False

# Example usage:
# Replace these with your actual GitHub repo details
GITHUB_REPO_OWNER = 'your-github-username'
GITHUB_REPO_NAME = 'your-github-repo-name'
ACCESS_TOKEN = 'your-personal-access-token'

# Step 1: Get the list of existing IDs
existing_post_ids = get_existing_ids_from_github(GITHUB_REPO_OWNER, GITHUB_REPO_NAME, ACCESS_TOKEN)

# Step 2: Reddit Post ID (replace this with the actual Reddit post ID you want to process)
reddit_post_id = '1i7s9gf'

# Step 3: Check if the post is already written
if not is_post_already_written(reddit_post_id, existing_post_ids):
    # Example Markdown content for the article (you need to generate this dynamically)
    markdown_content = """
    # Reddit Post Explanation
    ## Title: Why do financial institutions say "basis points"?
    This is a markdown article explaining the concept.
    """

    # Post the article to GitHub
    post_article_to_github(GITHUB_REPO_OWNER, GITHUB_REPO_NAME, ACCESS_TOKEN, reddit_post_id, markdown_content)
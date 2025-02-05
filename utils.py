import os
import base64
import requests
import random
from dotenv import load_dotenv
# langchain import
from langchain.tools import tool

load_dotenv()

GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')
REPO_OWNER = os.getenv('GITHUB_REPO_OWNER')
REPO_NAME = os.getenv('GITHUB_REPO_NAME')
FOLDER_PATH = 'content/posts'


def choose_filter():
    return random.choice(["new", "rising", "hot"])

def get_posts_from_eli5_reddit():
    """
    Retrieves the top 5 hottest posts from the r/explainlikeimfive subreddit.
    """

    subreddit_name='explainlikeimfive'
    filter=choose_filter()
    limit=5

    # URL to fetch hot posts with the limit
    url = f"https://www.reddit.com/r/{subreddit_name}/{filter}.json?limit={limit}"
    
    # Send a GET request to the Reddit API
    data = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    
    # Parse the JSON response
    posts = []
    
    for post in data['data']['children']:
        post_info = {
            'reddit_post_id': post['data']['id'],
            'reddit_question': post['data']['title'],
            'reddit_selftext': post['data']['selftext'],
            'reddit_user': post['data']['author'],
            'reddit_tag': post['data']['link_flair_text']
        }
        posts.append(post_info)
    
    return posts

def get_existing_ids_from_github():
    headers = {
        'Authorization': f'token {GITHUB_ACCESS_TOKEN}'
    }
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FOLDER_PATH}'

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        files = response.json()
        # Filter out markdown files and extract the Reddit post IDs (filename)
        return [os.path.splitext(file['name'])[0] for file in files if file['name'].endswith('.md')]
    else:
        return []
    
def push_markdown_to_github(title, markdown_content):
    """
    Pushes a markdown file to a specific folder in a GitHub repository.

    Args:
        title (str): The title of the markdown file (used as filename).
        markdown_content (str): The content of the markdown file to push.
    """

    # Prepare the URL and headers for GitHub API request
    api_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FOLDER_PATH}/{title}.md'
    headers = {'Authorization': f'Bearer {GITHUB_ACCESS_TOKEN}'}

    # Get the SHA of the current file, if it exists (for updates)
    response = requests.get(api_url, headers=headers)
    sha = None

    if response.status_code == 200:
        # If file exists, get the sha of the current file
        sha = response.json().get('sha')

    # Prepare the payload for the API request
    data = {
        'message': f'Add new post: {title}',  # Commit message
        'content': base64.b64encode(markdown_content.encode('utf-8')).decode('utf-8'),  # Base64-encoded file content
        'branch' : "main"
    }

    if sha:
        # If the file exists, include the SHA for updating it
        data['sha'] = sha

    # Send the request to push the markdown file
    response = requests.put(api_url, headers=headers, json=data)

    # Check if the push was successful
    if response.status_code == 201:
        print(f"Successfully pushed {title}.md to {FOLDER_PATH}")
    elif response.status_code == 200:
        print(f"Successfully updated {title}.md in {FOLDER_PATH}")
    else:
        print(f"Failed to push file. Status code: {response.status_code}")
        print(response.json())
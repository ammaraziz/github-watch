import requests

def send_slack_msg(hook_url, text):
    data = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            }
        ]
    }
    r = requests.post(hook_url, json=data)
    assert r.status_code == 200


def create_url(repo: str):
    #/repos/{owner}/{repo}/releases/lates
    owner, repo = repo.split('/')
    return f'https://api.github.com/repos/{owner}/{repo}/releases/latest'


def get_repo(url):
    r = requests.get(url)
    data = r.json()
    return data

def get_repo_from_name(repo):
    return get_repo(create_url(repo))
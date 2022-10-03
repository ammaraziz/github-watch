from datetime import datetime
from pathlib import Path
from typing import List, Optional
import requests
import typer
from .db import DB
from .utils import create_url, get_repo, get_repo_from_name, send_slack_msg

app = typer.Typer()


@app.command()
def add(
    repo: str = typer.Argument(None, help="GitHub repo in in {owner}/{repo} format."),
    db_path: Path = typer.Option('db.json', '--db', help="Path to the database."),
):
    db = DB(path=db_path)
    url = create_url(repo)
    data = get_repo(url)
    db.put(repo, data)
    typer.echo(f"Added {repo}!")
    

@app.command("list")
def list_repos(
    db_path: Path = typer.Option('db.json', '--db', help="Path to the database.")
):
    db = DB(path=db_path)
    for key in db:
        print('-', key, db.db[key]['tag_name'])

@app.command()
def check(
    db_path: Path = typer.Option('db.json', '--db', help="Path to the database."),
    id: Optional[List[str]] = typer.Option(None, help="Only check specified IDs."),
    slack: Optional[List[str]] = typer.Option(None, help="Hook to post the results to."),
):
    # load the db
    db = DB(path=db_path)

    repos = list(db)
    if id:
        repos = id
    
    for repo_id in repos:
        print(repo_id)
        repo_in_db = db.get(repo_id)
        repo_on_GitHub = get_repo_from_name(repo_id)

        if repo_in_db['url'] == repo_on_GitHub['url']:
            # if sha in db no change
            typer.echo("No change!\n")
            continue
        
        text = f"New version of <{repo_on_GitHub['html_url']}|{repo_id}> ({repo_on_GitHub['tag_name']}) released!\n\n{repo_on_GitHub['body']}\n"
        typer.echo(text)

        # update db
        db.put(repo_id, repo_on_GitHub)
        
        # send slack
        if slack:
            typer.echo('Sending update to slack!\n')
            for hook_url in slack:
                send_slack_msg(hook_url, text)
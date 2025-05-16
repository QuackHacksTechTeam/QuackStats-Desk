

from git import Repo
from stats.repo_stat import RepoStat
import os 
import shutil
from logger_config import Log
from stats.is_excluded_file import is_excluded_file

def get_repo_path():
    base_dir = os.path.expanduser("~/.quackstats")
    os.makedirs(base_dir, exist_ok=True)
    return base_dir

REPOS_PATH = get_repo_path()

def get_all_repo_stats(repo_links: list[str]) -> list[RepoStat]: 

    for repo_link in repo_links: 
        Log.info(f"Cloning repo {repo_link} to {REPOS_PATH}")
        try: 
            clone_repo(repo_link, REPOS_PATH)
        except Exception as e: 
            Log.error(f"Could not clone repo \"{os.path.basename(repo_link)}\": {str(e)}")

    base_names = [os.path.basename(repo_link) for repo_link in repo_links]

    for repo in os.listdir(REPOS_PATH):
        if repo not in base_names: 
            full_path = os.path.join(REPOS_PATH, repo)
            if is_in_repodir(full_path): 
                shutil.rmtree(full_path)

    all_repo_stats = []

    for repo_dir in os.listdir(REPOS_PATH):
        repo_dir_path = os.path.join(REPOS_PATH, repo_dir)
        repo_stat: RepoStat = get_repo_stats(repo_dir_path)


        all_repo_stats.append(repo_stat)

    return all_repo_stats



def get_repo_stats(path: str) -> RepoStat: 
    """
    Create a repo stat object given a repo path. 

    """
    repo_name = os.path.basename(path)
    repo_stat = RepoStat(repo_name)

    try: 
        repo = Repo(path)
    except Exception as e: 
        Log.error(f"Could not search repo \"{repo_name}\": {str(e)}")
        return repo_stat

    # Try to fetch repo commits 
    try: 
        repo_stat.commits = get_total_repo_commits(repo)
    except Exception as e: 
        Log.error(f"Could not read total commits from \"{repo_stat.name}\": {str(e)}")

    try: 
        repo_stat.lines_of_code = get_total_lines_of_code(path)
    except Exception as e: 
        Log.error(f"Could not read total lines of code from \"{repo_stat.name}\": {str(e)}")

    try: 
        repo_stat.user_commits = get_user_commits(repo)
    except Exception as e: 
        Log.error(f"Could not get user commits from \"{repo_stat.name}\": {str(e)}")

    return repo_stat

def clone_repo(repo_link, destination_path: str): 
    repo_name = os.path.basename(repo_link)
    repo_path = f"{destination_path}/{repo_name}"
    if not is_in_repodir(repo_path): 
        raise Exception(f"Repo path \"{repo_path}\" is not in the repo directory")
    
    if (os.path.exists(repo_path)): 
        shutil.rmtree(repo_path)

    Repo.clone_from(repo_link, repo_path)


# --------------- Private Functions ---------------

def is_in_repodir(path: str, repo_dir=REPOS_PATH) -> bool:
    """
    Makes sure we dont do anything stupid...
    """
    abs_path = os.path.abspath(path)
    abs_repo_dir = os.path.abspath(repo_dir)
    return os.path.commonpath([abs_path, abs_repo_dir]) == abs_repo_dir


def get_total_repo_commits(repo: Repo) -> int: 
    commits = list(repo.iter_commits())
    return len(commits)

def get_total_lines_of_code(repo_path: str) -> int: 
    total_loc = 0 

    for root, _, files in os.walk(repo_path): 
        for file in files: 
            if is_excluded_file(file): 
                continue

            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                lines = [line for line in lines if line.strip()]
                total_loc += len(lines)

    return total_loc

def get_user_commits(repo: Repo) -> dict[str, int]: 
    user_commits = {}

    for commit in repo.iter_commits(): 
        author = commit.author.name
        if author not in user_commits: 
            user_commits[author] = 1
        else: 
            user_commits[author] += 1

    return user_commits



    











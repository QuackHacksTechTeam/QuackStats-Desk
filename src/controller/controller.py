

from stats.get_repo_stats import get_all_repo_stats 
from stats.repo_stat import RepoStat
from logger_config import Log


class Controller: 
    def __init__(self): 
        self.repo_links = []
        self._repo_stats: list[RepoStat] = []

    def add_link(self, link: str): 
        self.repo_links.append(link) 

    def remove_link(self, link: str): 
        self.repo_links.remove(link)

    def get_repo_stats(self) -> list[RepoStat]: 
        return self._repo_stats


    def refresh_repo_stats(self): 
        self._repo_stats = get_all_repo_stats(self.repo_links)

        for repo_stat in self._repo_stats: 
            Log.info(f"Total repo commits for \"{repo_stat.name}\": {repo_stat.commits}")
            Log.info(f"Total lines of code for \"{repo_stat.name}\": {repo_stat.lines_of_code}")
            Log.info(f"User commits for \"{repo_stat.name}\": {repo_stat.user_commits}")



    




class RepoStat:
    def __init__(self, name: str): 
        self.name = name 

        self.commits: int = 0
        self.lines_of_code: int = 0
        self.user_commits: dict[str, int] = {}



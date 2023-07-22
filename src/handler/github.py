from github import Github
from utils.actions import Action

class GithubHandler:
    def __init__(self, github_token, repository_name, issue_number):
        self.github = Github(github_token)
        self.repo = self.github.get_repo(repository_name)
        self.issue = self.repo.get_issue(issue_number)

    def create_comment(self, comment_text):
        self.issue.create_comment(comment_text)

    def close_issue(self):
        self.issue.edit(state='closed')

    # parses the title and returns a tuple with (action <coordinates>|<title>)
    def parse_issue_title(self):
        if self.issue.title.lower() == 'minesweeper: start new game':
            return Action.NEW_GAME, None

        if self.issue.title.lower().startswith("minesweeper: "):
            try:
                coordinates = self.issue.title.split(" ")[1]
                row = int(coordinates[1:]) - 1  # convert the number to row index (1 becomes 0, 2 becomes 1, ...)
                col = ord(coordinates[0].upper()) - 65  # convert the letter to column index (A=0, B=1, ...)

                # check if both row and column values are within the valid range (0 to 8)
                if 0 <= row < 9 and 0 <= col < 9:
                    return Action.REVEAL, (row, col)
                else:
                    return Action.INVALID_MOVE, self.issue.title

            except (IndexError, ValueError):
                return Action.INVALID_MOVE, self.issue.title

        return Action.UNKNOWN, self.issue.title
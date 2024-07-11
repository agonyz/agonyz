from enum import Enum
import os
from utils.actions import Action
from handler.github import GithubHandler
from handler.markdown import MarkdownHandler
from handler.minesweeper import MinesweeperHandler

# get env variables
issue_number = int(os.environ.get("ISSUE_NUMBER"))
github_token = os.environ.get("GITHUB_TOKEN")
repository_owner = os.environ.get("REPOSITORY_OWNER")
repository_name = os.environ.get("GITHUB_REPOSITORY")
previous_job = os.environ.get("PREVIOUS_JOB")

# check if vars are set
if issue_number is None or github_token is None or repository_owner is None or repository_name is None:
    print("One or more required environment variables are not set. Stopping the script.")
    exit(1)

github_handler = GithubHandler(github_token, repository_name, issue_number)
action_key, action_value = github_handler.parse_issue_title()
minesweeper_handler = MinesweeperHandler()
markdown_handler = MarkdownHandler(repository_name)

if previous_job == "true":
    github_handler.create_comment('Action could not be executed: There is currently another workflow running.\nPlease wait for a bit and try your luck later again.')
    github_handler.close_issue()
    exit(1)

if action_key == Action.INVALID_MOVE:
    github_handler.create_comment('Action could not be executed: Invalid move.\nIf you think this is a bug, please contact the repository owner.')

elif action_key == Action.REVEAL:
    action_handled = False  # flag to track if the action has been handled

    # check if the game is already over
    if minesweeper_handler.is_game_over():
        github_handler.create_comment('The game is already over. Please mention the repository owner to start a new one.')
        action_handled = True

    # check if the cell was already revealed
    elif minesweeper_handler.is_field_revealed(action_value[0], action_value[1]):
        github_handler.create_comment('The given cell was already revealed. Please choose another cell.')
        action_handled = True

    if not action_handled:
        # update the game state
        minesweeper_handler.update_revealed_array(action_value[0], action_value[1])

        # update the scoreboard based on the action
        action_to_scoreboard = 'reveal_bomb' if minesweeper_handler.game_state['board'][action_value[0]][action_value[1]] == ':bomb:' else 'reveal_cell'
        minesweeper_handler.update_scoreboard(github_handler.issue.user.login, action_to_scoreboard)

        # update the readme
        markdown_handler.update_readme(minesweeper_handler.game_state, minesweeper_handler.scoreboard_state)

        # check if the game is over
        if minesweeper_handler.is_game_over():
            if minesweeper_handler.is_game_won():
                github_handler.create_comment('# :trophy: :rocket: :1st_place_medal:\n### Congratulations! You won!\n- Thank you for playing @'+ github_handler.issue.user.login +'\n- To start a new game, please mention the repository owner.')
            else:
                github_handler.create_comment('# :bomb: :boom:\n### You set off a bomb and lost the game.\n- Thank you for playing @'+ github_handler.issue.user.login +'\n- To start a new game, please mention the repository owner.')

        else:
            github_handler.create_comment('# :bomb: :sweat_smile:\n### You dodged the bombs - Good Job!\n- Thank you for playing @'+ github_handler.issue.user.login)

elif action_key == Action.NEW_GAME:
    if github_handler.issue.user.login != repository_owner:
        github_handler.create_comment('Hello @'+ github_handler.issue.user.login +' :wave:\n\nOnly the repository owner can start a new game.\nMention them like this @' + repository_owner)
    else:
        minesweeper_handler.create_initial_game_state()
        markdown_handler.update_readme(minesweeper_handler.game_state, minesweeper_handler.scoreboard_state)
        github_handler.create_comment('New game was started.')

else:
    github_handler.create_comment('Unknown action.')

github_handler.close_issue()






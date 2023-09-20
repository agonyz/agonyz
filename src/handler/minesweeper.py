import json
import os
import random

class MinesweeperHandler:
    def __init__(self, rows=9, columns=9, num_bombs=10):
        self.rows = rows
        self.columns = columns
        self.num_bombs = num_bombs
        self.game_state_file_path = self.get_relative_file_path('../../data/game_state.json')
        self.game_state = self.load_json(self.game_state_file_path, self.create_initial_game_state)
        self.scoreboard_file_path = self.get_relative_file_path('../../data/scoreboard_state.json')
        self.scoreboard_state = self.load_json(self.scoreboard_file_path, self.create_initial_scoreboard_state)

    def generate_minesweeper_field(self):
        field = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]
        bomb_positions = random.sample(range(self.rows * self.columns), self.num_bombs)
        for position in bomb_positions:
            row = position // self.columns
            col = position % self.columns
            field[row][col] = ':bomb:'
        return field

    def save_json(self, file_path, data):
        # write the game state to a JSON file
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def load_json(self, file_path, generate_initial_state):
        if os.path.exists(file_path):
            # read the game state from a JSON file
            with open(file_path, 'r') as file:
                return json.load(file)
        else:
            return generate_initial_state

    def update_revealed_array(self, row, col):
        self.game_state['revealed'][row][col] = True
        self.save_json(self.game_state_file_path, self.game_state)

    def get_relative_file_path(self, relative_file_path):
        # get the current directory path
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # construct the file path relative to the current directory
        file_path = os.path.join(current_dir, relative_file_path)
        return file_path
    
    def create_initial_game_state(self):
        # generate the minesweeper field
        minesweeper_field = self.generate_minesweeper_field()

        # create the initial game state dictionary
        game_state = {
            'board': minesweeper_field,
            'size': {'rows': self.rows, 'columns': self.columns},
            'mines': self.num_bombs,
            'revealed': [[False for _ in range(self.columns)] for _ in range(self.rows)]
        }

        # save the initial game state to the JSON file
        self.game_state = game_state
        self.save_json(self.game_state_file_path, self.game_state)

        return game_state
    
    # check if the field was already revealed
    def is_field_revealed(self, row, col):
        return self.game_state['revealed'][row][col]

    # check if a bomb has been revealed
    def is_bomb_revealed(self):
        for row in range(self.rows):
            for col in range(self.columns):
                cell_value = self.game_state['board'][row][col]
                is_revealed = self.game_state['revealed'][row][col]

                if cell_value == ':bomb:' and is_revealed:
                    return True

        return False

    # Check if the game is won (all non-bomb cells are revealed).
    def is_game_won(self):
        for row in range(self.rows):
            for col in range(self.columns):
                cell_value = self.game_state['board'][row][col]
                is_revealed = self.game_state['revealed'][row][col]

                if cell_value != ':bomb:' and not is_revealed:
                    return False

        return True

    # Check if the game is over
    def is_game_over(self):
        return self.is_game_won() or self.is_bomb_revealed()
    

    # Create initial scoreboard state
    def create_initial_scoreboard_state(self):
        scoreboard_state = {
            'players': [] 
        }

        self.scoreboard_state = scoreboard_state
        self.save_json(self.scoreboard_file_path, self.scoreboard_state)

        return scoreboard_state
    
    def update_scoreboard(self, player_name, action):
        players = self.scoreboard_state['players']

        # Check if the player already exists in the scoreboard
        player_exists = False
        for player in players:
            if player['name'] == player_name:
                player_exists = True
                player['rounds_played'] += 1

                if action == 'reveal_bomb':
                    player['bombs_revealed'] += 1
                elif action == 'reveal_cell':
                    player['cells_revealed'] += 1
                break

        # If the player doesn't exist, create a new entry
        if not player_exists:
            players.append({
                'name': player_name,
                'rounds_played': 1,
                'bombs_revealed': 1 if action == 'reveal_bomb' else 0,
                'cells_revealed': 1 if action == 'reveal_cell' else 0
            })

        self.scoreboard_state["players"] = players 
        self.save_json(self.scoreboard_file_path, self.scoreboard_state)



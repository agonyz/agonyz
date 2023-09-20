import os

class MarkdownHandler:
    def __init__(self, repository_name):
        self.readme_file_path = self.get_relative_file_path('../../README.md')
        self.repository_name = repository_name
        self.issue_body = 'Please don\'t change anything in this issue. To execute your action simply submit the issue.'

    def generate_minesweeper_table(self, game_state):
        # extract information from the game state
        rows = game_state['size']['rows']
        columns = game_state['size']['columns']
        board = game_state['board']
        revealed = game_state['revealed']

        # create the table header with column names
        header = '<table>\n<thead>\n<tr>\n<th></th>\n'
        for column in range(columns):
            header += f'<th>{chr(65 + column)}</th>\n'
        header += '</tr>\n</thead>\n<tbody>\n'

        # create the table rows with links in every row for columns A to I
        table_rows = ''
        for row in range(rows):
            table_rows += f'<tr>\n<td>{row + 1}</td>\n'
            for col in range(columns):
                if revealed[row][col]:
                    table_rows += f'<td>{board[row][col]}</td>\n'
                else:
                    table_rows += f'<td><a target="_blank" href="https://github.com/{self.repository_name}/issues/new?body={self.issue_body}&title=Minesweeper%3A+{chr(65 + col)}{row + 1}">?</a></td>\n'
            table_rows += '</tr>\n'

        # combine header and table rows to complete the table
        minesweeper_table = header + table_rows + '</tbody>\n</table>'
        return minesweeper_table
    

    def generate_scoreboard_table(self, scoreboard_stats, num_players=5):
        # Extract player information from the game state
        players = scoreboard_stats['players'] 

        # Sort players by rounds_played in descending order
        sorted_players = sorted(players, key=lambda x: x.get("rounds_played", 0), reverse=True)

        # Take the top 'num_players' players or all players if there are fewer
        top_players = sorted_players[:num_players]

        # Create the table header
        table_header = "| Rank | Player | Rounds Played | Bombs Revealed | Hit Rate | Cells Revealed |\n"
        table_header += "| :---: | :---: | :---: | :---: | :---: | :---: |\n"

        # Create the table rows
        table_rows = ""
        for rank, player in enumerate(top_players, start=1):
            name = player.get("name", "")
            rounds_played = player.get("rounds_played", 0)
            bombs_revealed = player.get("bombs_revealed", 0)
            cells_revealed = player.get("cells_revealed", 0)

            # calculate bomb hit rate for the player
            hit_rate = (bombs_revealed / rounds_played) * 100 if rounds_played > 0 else 0
            hit_rate_str = "{:.0f}".format(hit_rate)

            table_rows += f"| {rank} | <a target='_blank' href='https://github.com/{name}'>{name}</a> | {rounds_played} | {bombs_revealed} | {hit_rate_str}% | {cells_revealed} |\n"

        # combine header and rows to complete the table
        scoreboard_table = table_header + table_rows
        return scoreboard_table

    def update_readme(self, game_state, scoreboard_stats):
        # generate the HTML table based on the game state
        minesweeper_table = self.generate_minesweeper_table(game_state)
        scoreboard_table = self.generate_scoreboard_table(scoreboard_stats)

        # read the content of the README.md file
        with open(self.readme_file_path, 'r') as readme_file:
            readme_content = readme_file.read()

        # find the start and end markers in the content
        start_marker = "<!-- minesweeperboard -->"
        end_marker = "<!-- /minesweeperboard -->"
        start_index = readme_content.find(start_marker)
        end_index = readme_content.find(end_marker)

        if start_index != -1 and end_index != -1:
            # extract the part before and after the markers
            part_before = readme_content[:start_index]
            part_after = readme_content[end_index + len(end_marker):]

            # combine the parts with the updated HTML table
            updated_content = part_before + start_marker + "\n" + minesweeper_table + "\n\n#### Scoreboard\n\n" + scoreboard_table + "\n" + end_marker + part_after

            # write the updated content back to the README.md file
            with open(self.readme_file_path, 'w') as readme_file:
                readme_file.write(updated_content)
        else:
            # if the markers are not found, write the HTML table to the end of the file
            with open(self.readme_file_path, 'a') as readme_file:
                readme_file.write("\n" + start_marker + "\n" + minesweeper_table + + "\n\n#### Scoreboard\n\n" + scoreboard_table + "\n" + end_marker)


    def get_relative_file_path(self, file_path):
            # get the current directory path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # construct the file path relative to the current directory
            file_path = os.path.join(current_dir, file_path)
            return file_path
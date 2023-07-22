import os

class MarkdownHandler:
    def __init__(self, repository_name):
        self.file_path = self.get_file_path()
        self.repository_name = repository_name
        self.issue_body = 'Please don\'t change anything in this issue. To execute your action simply submit the issue.'

    def generate_html_table(self, game_state):
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
        html_table = header + table_rows + '</tbody>\n</table>'
        return html_table

    def update_readme(self, game_state):
        # generate the HTML table based on the game state
        html_table = self.generate_html_table(game_state)

        # read the content of the README.md file
        with open(self.file_path, 'r') as readme_file:
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
            updated_content = part_before + start_marker + "\n" + html_table + "\n" + end_marker + part_after

            # write the updated content back to the README.md file
            with open(self.file_path, 'w') as readme_file:
                readme_file.write(updated_content)
        else:
            # if the markers are not found, write the HTML table to the end of the file
            with open(self.file_path, 'a') as readme_file:
                readme_file.write("\n" + start_marker + "\n" + html_table + "\n" + end_marker)


    def get_file_path(self):
            # get the current directory path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # construct the file path relative to the current directory
            file_path = os.path.join(current_dir, '../../README.md')
            return file_path
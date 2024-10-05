import numpy as np

# ANSI escape codes for color formatting
RED = '\033[91m'  # Red color for Player 1
YELLOW = '\033[93m'  # Yellow color for Player 2
RESET = '\033[0m'  # Reset color to default

class Player:
    def __init__(self, name, piece):
        self.name = name
        self.piece = piece
        self.display_piece = RED + '●' + RESET if piece == 1 else YELLOW + '●' + RESET
        self.win_piece = RED + '▣' + RESET if piece == 1 else YELLOW + '▣' + RESET

class Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((self.rows, self.cols), dtype=int)

    def create_board(self):
        self.board = np.zeros((self.rows, self.cols), dtype=int)

    def print_board(self, winning_positions=None):
        for row in range(self.rows):
            row_display = []
            for col in range(self.cols):
                cell = self.board[row, col]
                if winning_positions and (row, col) in winning_positions:
                    row_display.append(RED + '▣' + RESET if cell == 1 else YELLOW + '▣' + RESET)
                else:
                    row_display.append(' ' if cell == 0 else (RED + '●' + RESET if cell == 1 else YELLOW + '●' + RESET))
            print('| ' + ' | '.join(row_display) + ' |')
        print('+---' * self.cols + '+')

    def drop_piece(self, col, piece):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = piece
                return True
        return False

    def check_winner(self, piece):
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if self.board[row][col] == piece and self.board[row][col + 1] == piece and \
                        self.board[row][col + 2] == piece and self.board[row][col + 3] == piece:
                    return [(row, col), (row, col + 1), (row, col + 2), (row, col + 3)]

        # Checking for vertical locations for a win
        for row in range(self.rows - 3):
            for col in range(self.cols):
                if self.board[row][col] == piece and self.board[row + 1][col] == piece and \
                        self.board[row + 2][col] == piece and self.board[row + 3][col] == piece:
                    return [(row, col), (row + 1, col), (row + 2, col), (row + 3, col)]

        # Checking for positively sloped diagonals
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if self.board[row][col] == piece and self.board[row + 1][col + 1] == piece and \
                        self.board[row + 2][col + 2] == piece and self.board[row + 3][col + 3] == piece:
                    return [(row, col), (row + 1, col + 1), (row + 2, col + 2), (row + 3, col + 3)]

        # Checking for negatively sloped diagonals
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if self.board[row][col] == piece and self.board[row - 1][col + 1] == piece and \
                        self.board[row - 2][col + 2] == piece and self.board[row - 3][col + 3] == piece:
                    return [(row, col), (row - 1, col + 1), (row - 2, col + 2), (row - 3, col + 3)]

        return None

class ConnectFourGame:
    def __init__(self):
        self.board = Board()
        self.game_over = False
        self.turn = 0
        self.players = []

    def setup_players(self):
        player1_name = input("Enter name for Player 1: ")
        player2_name = input("Enter name for Player 2: ")
        self.players = [Player(player1_name, 1), Player(player2_name, 2)]

    def play(self):
        self.setup_players()
        while not self.game_over:
            self.board.print_board()
            current_player = self.players[self.turn % 2]
            col = input(f"{current_player.name} ({current_player.display_piece}), make your selection (0-6): ")

            try:
                col = int(col)
                if col < 0 or col >= self.board.cols:
                    print("Invalid column. Please select a column between 0 and 6.")
                    continue

                if self.board.drop_piece(col, current_player.piece):
                    winning_positions = self.board.check_winner(current_player.piece)
                    if winning_positions:
                        self.board.print_board(winning_positions)
                        print(f"{current_player.name} wins!")
                        self.game_over = True
                    else:
                        self.turn += 1
                else:
                    print("Column full. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 6.")

        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again == 'yes':
            self.board.create_board()
            self.game_over = False
            self.turn = 0
            self.play()
        else:
            print("Thank you for playing!")

if __name__ == "__main__":
    game = ConnectFourGame()
    game.play()
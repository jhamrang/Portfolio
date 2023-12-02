# Author: John Hamrang
# Date: 12/03/2021
# Description: Creates a Hasami Shogi game to be played
# Creating the class, comments are a bit light since so much info is in the docstrings
class HasamiShogiGame:
    """Creates a Hasami Shogi game to be played using red and black pieces"""

    def __init__(self):
        """Initializes the game, by setting initial values for active_player, number of captured pieces on either side
            and creating the board with the ShogiBoard Class"""
        self._game_state = "UNFINISHED"
        self._active_player = "BLACK"
        self._num_cap_black = 0
        self._num_cap_red = 0
        self._board = ShogiBoard()  # initialize the board

    def get_game_state(self):
        """Checks if the game has been won and updates game_state appropriately, The conditions for the game being won
            by a side would be the number of captured pieces of the opposing side exceeding 7
            returns: game_state after checking"""
        if self.get_num_captured_pieces("BLACK") >= 8:
            self._game_state = "RED_WON"
        if self.get_num_captured_pieces("RED") >= 8:
            self._game_state = "BLACK_WON"
        return self._game_state

    def get_num_captured_pieces(self, color):
        """ Finds the number of captured pieces of passed color
            Parameter: color - color desired to check number of captured pieces of ('RED' 'BLACK')
            Returns: num of passed parameter color that have been captured"""
        if color == "RED":
            return self._num_cap_red
        if color == "BLACK":
            return self._num_cap_black

    def update_num_captured_pieces(self, color, amt_capped_this_move):
        """Takes the two parameters provided to update num_cap_red or num_cap_black
            Parameters: color - Either 'RED' or 'BLACK' to indicate which pieces were captured
                        amt_capped_this_move - amount to add to num_cap_red or num_cap_black"""
        if color == "RED":
            self._num_cap_red = self.get_num_captured_pieces("RED") + amt_capped_this_move
        if color == "BLACK":
            self._num_cap_black = self.get_num_captured_pieces("BLACK") + amt_capped_this_move

    def get_active_player(self):
        """ Finds who the active player is
            Returns: active_player (person whose turn it is, either 'RED' or 'BLACK')"""
        return self._active_player

    def translate_position(self, pos):
        """Translates a position like 'C1' that the user can read into the list of lists notation that the baord is
            actually using. ex 'C1' -> [2],[0]
            Parameters: pos - human readable position ex. 'C1'
            Returns:    pos_1 - which list in the list of lists indexed from 0-8 corresponds to pos
                        pos_2 - which index in that list from 0-8 corresponds to pos"""
        row = ord(pos[0].lower()) - 97
        col = ord(pos[1]) - 49
        if row < 0 or row > 9 or col < 0 or col > 8:
            print("input not in bounds")
            return None
        return row, col

    def make_move(self, old_pos, new_pos):
        """ checks if the move is valid and moves a piece from old_pos to new_pos if it is and updates active_player.
            For move to be valid needs to check if its either horizontal or vertical movement and doesn't jump over/on
            another piece. Will also need to check if there is a piece at old_pos to begin with. Return true if move is
            found to be valid. Checking if the movement is horizontal or vertical can be done by directly comparing
            old_pos and new_pos, Checking if pieces are in the way can be done by looping get_square_occupant
            from old_pos to new_pos and checking whats inbetween. It also needs to check if the piece at old_pos is
            valid with who the active_player is (use get_active_player and get_square_occupant to check). Translating
            old_pos and new_pos into the list of list
            notations can be done using translate_position, which will be called within the get_square_occupant method.
            If move is not valid returns false. Will need to communicate with the ShogiBoard class since it holds the
            board. If the move is valid will also need to check if any pieces were captured with this move, update the
            num_cap for that color, and update the board to remove these pieces. In addition ot this if the move is
            valid the _active_player needs to be updated to be the other player (ie. if it was 'RED' it is now 'BLACK').
            If a valid move is made, will need to call new_capture to check if pieces were captured as a result of this.
            If a valid move is made the board will also need to be updated using update_board
             This will be done with the help of the following functions: translate_position, new_capture,
             get_active_player, get_square_occupant, and update_board (part of the ShogiBoard class)
            Parameters: old_pos - position of piece that the player wants to move. ex. 'C1'
                        new_pos - position player wants to move piece to. ex. 'C1'
            Returns:    True/False depending on if the move is valid or not. Valid move is vertical or horizontal
                        movement with no pieces jumped over"""
        # checking if the game has been won
        if self.get_game_state() != 'UNFINISHED':
            return False
        # checking if valid input and setting pos to be lowercase
        old_pos = old_pos.lower()
        new_pos = new_pos.lower()
        if old_pos == new_pos:
            return False

        if old_pos[0] != new_pos[0] and old_pos[1] != new_pos[1]:
            return False

        # checking if there is a piece there and if it is the right player
        piece = self.get_square_occupant(old_pos)
        color = self.get_active_player()
        if color == "BLACK":
            if piece != 'BLACK':
                return False

        if color == 'RED':
            if piece != 'RED':
                return False
        # checking if we are moving as a row, or moving as a column and iterating through to see
        # old_row, old_col = self.translate_position(old_pos)
        # new_row, new_col = self.translate_position(new_pos)
        cur_pos = old_pos
        if old_pos[1] == new_pos[1]:  # So rows, not columns
            if old_pos[0] < new_pos[0]:
                for cur_row in range(ord(old_pos[0]) + 1, ord(new_pos[0]) + 1):
                    cur_pos = chr(cur_row) + old_pos[1]
                    if self.get_square_occupant(cur_pos) != 'NONE':
                        return False
            else:
                for cur_row in range(ord(new_pos[0]), ord(old_pos[0])):
                    cur_pos = chr(cur_row) + old_pos[1]
                    if self.get_square_occupant(cur_pos) != 'NONE':
                        return False

        if old_pos[0] == new_pos[0]:  # So cols not rows
            if old_pos[1] < new_pos[1]:
                for cur_col in range(ord(old_pos[1]) + 1, ord(new_pos[1]) + 1):
                    cur_pos = old_pos[0] + chr(cur_col)
                    if self.get_square_occupant(cur_pos) != 'NONE':
                        return False
            else:
                for cur_col in range(ord(new_pos[1]), ord(old_pos[1])):
                    cur_pos = old_pos[0] + chr(cur_col)
                    if self.get_square_occupant(cur_pos) != 'NONE':
                        return False
        # all checks passed time to update the board then check if things have been capped
        new_row, new_col = self.translate_position(new_pos)
        old_row, old_col = self.translate_position(old_pos)
        self._board.update_board(old_row, old_col, '.')
        token = '.'
        if piece == 'BLACK':
            token = 'B'
        if piece == 'RED':
            token = 'R'
        self._board.update_board(new_row, new_col, token)
        self.new_capture(new_pos)

        # Setting active player
        if self.get_active_player() == 'BLACK':
            self._active_player = 'RED'
        elif self.get_active_player() == 'RED':
            self._active_player = 'BLACK'
        return True

    def get_square_occupant(self, pos):
        """ Checks what type of piece is occupying the passed position. Will need to communicate with the ShogiBoard
            board defined in this classes init. Returns a description of what is found at pos. will also use the
            translate_position function
            Returns: occupant - 'Red', 'Black', 'NONE' depending on what is there"""
        row, col = self.translate_position(pos)
        if self._board.get_board()[row][col] == 'R':
            return 'RED'
        elif self._board.get_board()[row][col] == 'B':
            return 'BLACK'
        else:
            return 'NONE'

    def new_capture(self, new_pos):
        """Checks if the move to new_pos of a piece resulted in any new captures,
            Will do this by checking for enemy pieces adjacent (in both horizontal and vertical directions to the
            new_pos), and then either more enemy pieces, or another of the active player's piece. If there is an
            uninterrupted number of enemy pieces in any of these directions (found by looping get_square_occupant and
            keeping track of uninterrupted rows or columns of enemy units adjacent to new_pos) between new_pos, and
            another friendly one, the positions of those enemy pieces are used to update the board to remove them using
            the update_board function in the ShogiBoard class. In addition to this, if the passed new_pos is adjacent
            (not diagonally) to a corner, one must check for the special case of a corner capture as well. This would
            involve another friendly unit being in the other square adjacent orthogonally to the corner, and an enemy
            piece being in that corner. Also, the num_cap_pieces of that color will be updated using
            update_num_captured_pieces. Friendly vs enemy pieces would be determined by checking the passed positin
            This function will be called by make_move. This class will call get_square_occupant,
            update_num_captured_pieces, translate_position, and  the ShogiBoard function for update_board
            Parameter: new_pos - position that the moving piece has just been moved to"""
        piece = self.get_square_occupant(new_pos)  # piece also denotes what friendly pieces would be
        enemy_piece = None
        if piece == 'RED':
            enemy_color = 'BLACK'
            enemy_piece = 'BLACK'  # Enemy pieces are of the type that can be captured
        elif piece == 'BLACK':
            enemy_piece = 'RED'
            enemy_color = 'RED'

        row, col = self.translate_position(new_pos)
        # first checking above the piece. This wouldve been easier using a break statement, but i tried to avoid it
        up_cap_ctr = 0
        possible_cap = False  # a capture is possible in the current direction
        up_cap = False  # a capture has happened in the current direction
        if row > 1:  # no point checking if we are in the first or second row, no upward cap possible there
            for row_pos in range(ord(new_pos[0]) - 1, ord('a') - 1, -1):
                # print(chr(row_pos)+new_pos[1])
                if self.get_square_occupant(chr(row_pos) + new_pos[1]) == enemy_piece and row_pos == ord(
                        new_pos[0]) - 1:
                    possible_cap = True
                    up_cap_ctr += 1
                elif self.get_square_occupant(chr(row_pos) + new_pos[1]) == enemy_piece and up_cap is False:
                    up_cap_ctr += 1
                if self.get_square_occupant(chr(row_pos) + new_pos[1]) == piece and possible_cap is True:
                    up_cap = True
                if self.get_square_occupant(chr(row_pos) + new_pos[1]) == 'NONE':
                    possible_cap = False

            if up_cap is False:
                up_cap_ctr = 0
            else:
                self.update_num_captured_pieces(enemy_color, up_cap_ctr)
                for cap_pos in range(ord(new_pos[0]) - 1, ord(new_pos[0]) - up_cap_ctr - 1, -1):
                    update_row, update_col = self.translate_position(chr(cap_pos) + new_pos[1])
                    self._board.update_board(update_row, update_col, '.')

        # now checking below the piece
        down_cap_ctr = 0
        possible_cap = False  # a capture is possible in the current direction
        down_cap = False  # a capture has happened in the current direction
        if row <= 6:  # no point checking if we are in the bottom 2 rows, no downward cap possible there
            for row_pos in range(ord(new_pos[0]) + 1, ord('i') + 1):
                # print(chr(row_pos)+new_pos[1])
                if self.get_square_occupant(chr(row_pos) + new_pos[1]) == enemy_piece and row_pos == ord(
                        new_pos[0]) + 1:
                    possible_cap = True
                    down_cap_ctr += 1
                elif self.get_square_occupant(chr(row_pos) + new_pos[1]) == enemy_piece and down_cap is False:
                    down_cap_ctr += 1
                if self.get_square_occupant(chr(row_pos) + new_pos[1]) == piece and possible_cap is True:
                    down_cap = True
                if self.get_square_occupant(chr(row_pos) + new_pos[1]) == 'NONE':
                    possible_cap = False

            if down_cap is False:
                down_cap_ctr = 0
            else:
                self.update_num_captured_pieces(enemy_color, down_cap_ctr)
                for cap_pos in range(ord(new_pos[0]) + 1, ord(new_pos[0]) + down_cap_ctr + 1):
                    update_row, update_col = self.translate_position(chr(cap_pos) + new_pos[1])
                    self._board.update_board(update_row, update_col, '.')

        # now checking to the right of the piece
        right_cap_ctr = 0
        possible_cap = False  # a capture is possible in the current direction
        right_cap = False  # a capture has happened in the current direction
        if col <= 6:  # no point checking if we are in the last 2 cols, no right cap possible there
            for col_pos in range(ord(new_pos[1]) + 1, ord('9') + 1):
                # print(chr(row_pos)+new_pos[1])
                if self.get_square_occupant(new_pos[0] + chr(col_pos)) == enemy_piece and col_pos == ord(
                        new_pos[1]) + 1:
                    possible_cap = True
                    right_cap_ctr += 1
                elif self.get_square_occupant(new_pos[0] + chr(col_pos)) == enemy_piece and right_cap is False:
                    right_cap_ctr += 1
                if self.get_square_occupant(new_pos[0] + chr(col_pos)) == piece and possible_cap is True:
                    right_cap = True
                if self.get_square_occupant(new_pos[0] + chr(col_pos)) == 'NONE':
                    possible_cap = False

            if right_cap is False:
                right_cap_ctr = 0
            else:
                self.update_num_captured_pieces(enemy_color, right_cap_ctr)
                for cap_pos in range(ord(new_pos[1]) + 1, ord(new_pos[1]) + right_cap_ctr + 1):
                    update_row, update_col = self.translate_position(new_pos[0] + chr(cap_pos))
                    self._board.update_board(update_row, update_col, '.')

        # now checking to the left of the piece
        left_cap_ctr = 0
        possible_cap = False  # a capture is possible in the current direction
        left_cap = False  # a capture has happened in the current direction
        if col > 1:  # no point checking if we are in the first 2 cols, no left cap possible there
            for col_pos in range(ord(new_pos[1]) - 1, ord('1') - 1, -1):
                # print(chr(row_pos)+new_pos[1])
                if self.get_square_occupant(new_pos[0] + chr(col_pos)) == enemy_piece and col_pos == ord(
                        new_pos[1]) - 1:
                    possible_cap = True
                    left_cap_ctr += 1
                elif self.get_square_occupant(new_pos[0] + chr(col_pos)) == enemy_piece and left_cap is False:
                    left_cap_ctr += 1
                if self.get_square_occupant(new_pos[0] + chr(col_pos)) == piece and possible_cap is True:
                    left_cap = True
                if self.get_square_occupant(new_pos[0] + chr(col_pos)) == 'NONE':
                    possible_cap = False

            if left_cap is False:
                left_cap_ctr = 0
            else:
                self.update_num_captured_pieces(enemy_color, left_cap_ctr)
                for cap_pos in range(ord(new_pos[1]) - 1, ord(new_pos[1]) - left_cap_ctr - 1, -1):
                    update_row, update_col = self.translate_position(new_pos[0] + chr(cap_pos))
                    self._board.update_board(update_row, update_col, '.')

        # Checking for corner captures
        # upper left corner
        if new_pos == 'a2' or new_pos == 'b1':
            if self.get_square_occupant('a2') == piece and self.get_square_occupant(
                    'b1') == piece and self.get_square_occupant('a1') == enemy_piece:
                self.update_num_captured_pieces(enemy_color, 1)
                update_row, update_col = self.translate_position('a1')
                self._board.update_board(update_row, update_col, '.')

        # upper right corner
        if new_pos == 'a8' or new_pos == 'b9':
            if self.get_square_occupant('a8') == piece and self.get_square_occupant(
                    'b9') == piece and self.get_square_occupant('a9') == enemy_piece:
                self.update_num_captured_pieces(enemy_color, 1)
                update_row, update_col = self.translate_position('a9')
                self._board.update_board(update_row, update_col, '.')

        # lower right corner
        if new_pos == 'i8' or new_pos == 'h9':
            if self.get_square_occupant('i8') == piece and self.get_square_occupant(
                    'h9') == piece and self.get_square_occupant('i9') == enemy_piece:
                self.update_num_captured_pieces(enemy_color, 1)
                update_row, update_col = self.translate_position('i9')
                self._board.update_board(update_row, update_col, '.')

        # lower left corner
        if new_pos == 'i2' or new_pos == 'h1':
            if self.get_square_occupant('i2') == piece and self.get_square_occupant(
                    'h1') == piece and self.get_square_occupant('i1') == enemy_piece:
                self.update_num_captured_pieces(enemy_color, 1)
                update_row, update_col = self.translate_position('i1')
                self._board.update_board(update_row, update_col, '.')


class ShogiBoard:
    """ Creates a board for the HasamiShogiGame class. The board is a list of lists where 'B' is a black piece, 'R' is a
        red piece, and '.' is an empty position. This class needs to interact with the HasamiShogiGame class since the
        board is a part of the game"""

    def __init__(self):
        """Initializes the board by setting it up as a list of lists, with player pieces in the starting positions"""
        self._board = []
        for board_size_ctr in range(0, 8):
            if self._board == []:
                self._board.append(["R", "R", "R", "R", "R", "R", "R", "R", "R"])
            else:
                self._board.append([".", ".", ".", ".", ".", ".", ".", ".", "."])
        self._board.append(["B", "B", "B", "B", "B", "B", "B", "B", "B"])

    def get_board(self):
        """Gets the board
            Returns: _board - the board. A list of lists representing a Shogi board with pieces on it"""
        return self._board

    def print_board(self):
        """Prints the current board. Not necessarily needed for this project, but is needed to debug."""
        col_title = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        print(' ', end=" ")
        for col_title_ctr in range(0, 9):
            if col_title_ctr < (len(col_title) - 1):
                print(col_title[col_title_ctr], end=" ")
            else:
                print(col_title[col_title_ctr])

        chr_ctr = 96
        for row in range(0, 9):
            chr_ctr += 1
            print(chr(chr_ctr), end=" ")
            for col in range(0, 9):
                if col < 8:
                    print(self.get_board()[row][col], end=" ")
                else:
                    print(self.get_board()[row][col])

    def update_board(self, row, col, update):
        """Updates the position of the board with the passed update string.
            Parameters: row - position to be updated, passed as a list with coordinates for the board. ex .[1,1]
                              corresponds to 'a1'
                        update - the new string value that replaces what was in that position. Valid input would be 'B',
                                 'R', or '.'"""
        self._board[row][col] = update

# Testing 1 Final version
# game = HasamiShogiGame()
# game._board.print_board()
# print(game.get_active_player())
# print(game.get_square_occupant("a1"))
# print(game.make_move('i8','h8'))
# print(game.make_move('a1', 'c1'))
# game._board.print_board()
# print(game.make_move('b1','h1'))
# game.make_move('I2', 'b2')
# game._board.print_board()
# print(game.make_move('a5', 'c5'))
# game._board.print_board()
# print(game.make_move('b2','b1'))
# game._board.print_board()
# print(game.make_move('a2','a1'))
# game._board.print_board()
# print(game.make_move('i3','b3'))
# game._board.print_board()
# game.make_move('c5','c6')
# game._board.print_board()
# game.make_move('b3','b1')
# game._board.print_board()
# game.make_move('c6','d6')
# game._board.print_board()
# game.make_move('i1','h1')
# game._board.print_board()
# game.make_move('d6','d1')
# game._board.print_board()
# game.make_move('h1','e1')
# game._board.print_board()
#
#
# game.make_move('a6','b6')
# game._board.print_board()
# game.make_move('I5','A5')
# game._board.print_board()
# game.make_move('a7','b7')
# game._board.print_board()
# game.make_move('I4','i2')
# game._board.print_board()
# game.make_move('a8','b8')
# game._board.print_board()
# game.make_move('i2','a2')
# game._board.print_board()
#
# print()
# print()
# game.make_move('a9','b9')
# game._board.print_board()
# game.make_move('i6','i5')
# game._board.print_board()
# game.make_move('b9','a9')
# game._board.print_board()
# game.make_move('i9','b9')
# game._board.print_board()
# game.make_move('a9','a8')
# game._board.print_board()
# game.make_move('I5','b5')
# game._board.print_board()
# print(game.get_game_state())
# print(game.get_num_captured_pieces('RED'))
# print(game.get_num_captured_pieces('BLACK'))
# print(game.get_active_player())
# print(game.make_move('a8','b8'))


# Testing 2 - corners primarily
# game = HasamiShogiGame()
# game._board.print_board()
#
# game.make_move('i4','e4')
# game._board.print_board()
#
# game.make_move('a8', 'h8')
# game._board.print_board()
# game.make_move('i7','b7')
# game._board.print_board()
# game.make_move('h8','h9')
# game._board.print_board()
# game.make_move('b7','b8')
# game._board.print_board()
# game.make_move('a2','g2')
# game._board.print_board()
# game.make_move('b8','a8')
# game._board.print_board()
# game.make_move('a7','i7')
# game._board.print_board()
# game.make_move('i8', 'b8')
# game._board.print_board()
# game.make_move('g2','g1')
# game._board.print_board()
# game.make_move('b8','b9')
# game._board.print_board()
# game.make_move('i7','i8')
# game._board.print_board()
# game.make_move('i2','A2')
# game._board.print_board()
# game.make_move('G1','h1')
# game._board.print_board()
# game.make_move('b9','b1')
# game._board.print_board()
# game.make_move('h9','h2')
# game._board.print_board()
# game.make_move('i5','b5')
# game._board.print_board()
# game.make_move('h2','i2')
# game._board.print_board()
# print(game.get_game_state())
# print(game.get_num_captured_pieces('RED'))
# print(game.get_num_captured_pieces('BLACK'))
# print(game.get_active_player())


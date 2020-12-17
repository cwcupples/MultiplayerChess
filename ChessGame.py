import pygame
import Board_and_Pieces
import Constants
from Constants import SQUARE

# start the game
pygame.init()
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()


# welcome message to start the game
def welcome():
    Constants.screen.fill(Constants.BLACK)
    font = pygame.font.Font('freesansbold.ttf', 16)
    text1 = font.render("Welcome to 2 person chess!", True, Constants.GREEN, Constants.BLUE)
    text2 = font.render("The border tells you who's turn it is", True, Constants.GREEN, Constants.BLUE)
    text3 = font.render("Click anywhere on the screen to begin", True, Constants.GREEN, Constants.BLUE)
    textrect1 = text1.get_rect()
    textrect2 = text2.get_rect()
    textrect3 = text3.get_rect()
    textrect1.center = ((SQUARE * 8 + 6) // 2, (SQUARE * 8 + 6) // 2 - 21)
    textrect2.center = ((SQUARE * 8 + 6) // 2, (SQUARE * 8 + 6) // 2)
    textrect3.center = ((SQUARE * 8 + 6) // 2, (SQUARE * 8 + 6) // 2 + 21)
    Constants.screen.blit(text1, textrect1)
    Constants.screen.blit(text2, textrect2)
    Constants.screen.blit(text3, textrect3)
    clock.tick(10)
    pygame.display.update()
    # Loop so game doesn't start until they click
    done = False
    while not done:
        for event in pygame.event.get():  # User did something
            # get row and column of the piece to move
            if event.type == pygame.MOUSEBUTTONDOWN:
                done = True
            if event.type == pygame.QUIT:  # If user clicked close
                quit()


# make sure that the knight moves correctly
def knight(move, loc):
    row1, col1 = loc
    row2, col2 = move
    if (abs(row1 - row2) == 1 and abs(col1 - col2) == 2) or (abs(row1 - row2) == 2 and abs(col1 - col2) == 1):
        return True
    else:
        return False


# checks king move
def king(move, loc):
    if (abs(move[0] - loc[0]) > 1) or (abs(move[1] - loc[1]) > 1):
        return False
    return True


# game class
class ChessGame:
    # initialize the game
    def __init__(self, color):
        # Error checking to make sure they don't enter a random number
        if color % 2 == 1:
            color = 1
        else:
            color = 2
        self.__board = Board_and_Pieces.ChessBoard(color)
        self.turn = 1        # keeps track of whose turn it is
        self._p1_taken = []  # keeps track of which pieces player 1 has taken
        self._p2_taken = []  # keeps track of which pieces player 2 has taken
        self._winner = None

    # this is how we actually play, move this to the client that will talk to the server
    def play_ball(self):
        welcome()
        while not self._winner:
            self.display()
            self.my_turn()
            # *** FIX THIS FOR MULTI ***
            if self.turn == 1:
                # check to see if player 2 king in player 1 graveyard
                if -6 in self._p1_taken:
                    self._winner = "You win! :)"
                self.turn += 1
            else:
                # check to see if player 1 king in player 2 graveyard
                if 6 in self._p2_taken:
                    self._winner = "You lost! :("
                self.turn -= 1
        self.display()
        self.print_winner()
        while True:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    quit()

    # call this to print the current game board
    def display(self):
        if self.turn == 1:
            Constants.screen.fill(Constants.WHITE)
        else:
            Constants.screen.fill(Constants.BLACK)
        self.__board.print_board()
        self.print_taken()
        clock.tick(10)
        pygame.display.update()

    # print all of the pieces taken by each other
    def print_taken(self):
        for i in range(len(self._p1_taken)):
            pic = self._p1_taken[i]
            if i < 6:
                Constants.screen.blit(self.__board.game_pieces.get_grave(pic), [5 + i * 26, 325])
            elif i < 12:
                Constants.screen.blit(self.__board.game_pieces.get_grave(pic), [5 + (i - 6) * 26, 351])
            else:
                Constants.screen.blit(self.__board.game_pieces.get_grave(pic), [5 + (i - 12) * 26, 372])
        for i in range(len(self._p2_taken)):
            pic = self._p2_taken[i]
            if i < 6:
                Constants.screen.blit(self.__board.game_pieces.get_grave(pic), [165 + i * 26, 325])
            elif i < 12:
                Constants.screen.blit(self.__board.game_pieces.get_grave(pic), [165 + (i - 6) * 26, 351])
            else:
                Constants.screen.blit(self.__board.game_pieces.get_grave(pic), [165 + (i - 12) * 26, 377])

    # print the winner on the screen
    def print_winner(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(self._winner, True, Constants.GREEN, Constants.BLUE)
        textrect = text.get_rect()
        textrect.center = ((SQUARE * 8 + 6) // 2, (SQUARE * 8 + 6) // 2)
        Constants.screen.blit(text, textrect)
        clock.tick(10)
        pygame.display.update()

    # public way to check for winner
    def winner(self):
        return self._winner

    # function that runs this player's turn
    def my_turn(self):
        while True:
            # get and set the piece to move
            loc_piece_move = self.player_piece()
            self.display()
            pygame.draw.rect(Constants.screen, Constants.GREEN,
                             [loc_piece_move[1] * SQUARE + 3, loc_piece_move[0] * SQUARE + 3, SQUARE, SQUARE], 4)
            piece_to_move = self.__board[loc_piece_move[0], loc_piece_move[1]]
            clock.tick(10)
            pygame.display.flip()
            # get and set the place to move
            move_to = self.player_move(loc_piece_move, piece_to_move)
            piece_taken = self.__board[move_to[0], move_to[1]]
            # this is here in case the player selects a piece that has no moves
            if move_to != [-1, -1]:
                break
            else:
                pygame.draw.rect(Constants.screen, Constants.RED, [loc_piece_move[1] * SQUARE + 3,
                                                                   loc_piece_move[0] * SQUARE + 3, SQUARE, SQUARE], 4)
                pygame.display.flip()
        # Check for pawn switch to queen
        if piece_to_move == 1 and move_to[0] == 0:
            piece_to_move = 5
        self.__board[loc_piece_move[0], loc_piece_move[1]] = 0
        self.__board[move_to[0], move_to[1]] = piece_to_move
        # add a taken piece to the graveyard
        if piece_taken != 0:
            self._p1_taken.append(piece_taken)
        if piece_taken == -6:
            self._winner = "You win! :)"
        self.turn += 1
        return piece_to_move, loc_piece_move, piece_taken, move_to

    # function for the opponent's turn
    def opp_turn(self, recv_package):
        # piece_to_move, loc_piece_move, piece_taken, move_to
        # [   piece,       [row, col],     piece,     [row, col]    ]
        piece_to_move = recv_package[0] * -1
        loc_piece_move = [7 - recv_package[1], 7 - recv_package[2]]
        piece_taken = recv_package[3]
        move_to = [7 - recv_package[4], 7 - recv_package[5]]
        # spot they moved from is now empty
        self.__board[loc_piece_move[0], loc_piece_move[1]] = 0
        # the spot they moved to is now filled
        self.__board[move_to[0], move_to[1]] = piece_to_move
        # add a taken piece to the graveyard
        if piece_taken != 0:
            self._p2_taken.append(piece_taken)
        if piece_taken == 6:
            self._winner = "You lose! :("
        self.turn -= 1

    # get the piece that player wants to move
    def player_piece(self):
        # Make shift do-while loop top get the piece to move
        while True:
            for event in pygame.event.get():  # User did something
                # get row and column of the piece to move
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    # convert the coordinates into a position in 2-D array
                    col = (position[0] - 3) // SQUARE
                    row = (position[1] - 3) // SQUARE
                    # make sure that they clicked on the board
                    if row > 7 or row < 0 or col < 0 or col > 7:
                        # do nothing
                        continue
                    else:
                        # store the location of the piece
                        piece_loc = [row, col]
                        # make sure they are selecting one of their pieces
                        if self.__board[row, col] > 0:
                            # return it's location
                            return piece_loc
                if event.type == pygame.QUIT:  # If user clicked close
                    quit()

    # get the place that player 1 wants to move to
    def player_move(self, location, piece):
        # Make shift do-while loop top get the piece to move
        while True:
            for event in pygame.event.get():  # User did something
                # get row and column of the piece to move
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    # convert position to coordinates of 2-D array
                    col = (position[0] - 3) // 40
                    row = (position[1] - 3) // 40
                    # make sure that the row and column entered are on the board
                    if row > 7 or row < 0 or col < 0 or col > 7:
                        # do nothing
                        continue
                    else:
                        # store the location of the piece
                        move_loc = [row, col]
                        curr_piece = self.__board[row, col]
                        # make sure they aren't moving to a space occupied by their own piece
                        if curr_piece > 0:
                            return [-1, -1]
                        # make sure the move is valid
                        elif self.move_switch(move_loc, location, piece):
                            # return it's location
                            return move_loc
                        else:
                            return [-1, -1]
                if event.type == pygame.QUIT:  # If user clicked close
                    quit()

    # switch case to determine if projected move is valid
    def move_switch(self, move, loc, piece):
        if piece == 1:
            # pawn
            return self.pawn(move, loc)
        elif piece == 2:
            # rook
            return self.rook(move, loc)
        elif piece == 3:
            # knight
            return knight(move, loc)
        elif piece == 4:
            # bishop
            return self.bishop(move, loc)
        elif piece == 5:
            # the queen
            return self.rook(move, loc) or self.bishop(move, loc)
        else:
            # dat boi king
            return king(move, loc)

    # determines if pawn move was legal
    def pawn(self, move, loc):
        # move is where we move to, loc is where we move from, piece is the piece that is moving
        # get piece at where we move to, if one exists
        p_move_to = self.__board[move[0], move[1]]
        # Here we check if they moved 2 spaces at the beginning
        if loc[0] == 6 and move[0] == 4 and move[1] == loc[1] and p_move_to == 0 and self.__board[5, move[1]] == 0:
            return True
        # make sure pawn only moves 1 space at a time
        if move[0] != loc[0] - 1:
            return False
        # pawn can't change rows unless attacking
        elif p_move_to == 0 and move[1] != loc[1]:
            return False
        # if pawn is attacking, can only move one space diagonally
        elif p_move_to != 0:
            if move[1] == loc[1]:
                return False
            if move[1] != loc[1] + 1 and move[1] != loc[1] - 1:
                return False
            else:
                return True
        else:
            return True

    # make sure the rook is moving correctly
    def rook(self, move, loc):
        # player 1 and player 2 are exactly the same
        # can only move in one row or column
        if move[0] != loc[0] and move[1] != loc[1]:
            return False
        elif move[0] == loc[0]:
            # right
            if move[1] > loc[1]:
                for t in range(1, move[1] - loc[1]):
                    if self.__board[move[0], loc[1] + t] != 0:
                        return False
            # left
            if move[1] < loc[1]:
                for t in range(1, loc[1] - move[1]):
                    if self.__board[move[0], loc[1] - t] != 0:
                        return False
        elif move[1] == loc[1]:
            # down
            if move[0] > loc[0]:
                for t in range(1, move[0] - loc[0]):
                    if self.__board[move[0] - t, loc[1]] != 0:
                        return False
            # up
            if move[0] < loc[0]:
                for t in range(1, loc[0] - move[0]):
                    if self.__board[move[0] + t, loc[1]] != 0:
                        return False
        return True

    # make sure the bishop moves correctly
    def bishop(self, move, loc):
        # player 1 and 2 will be the same
        if abs(move[0] - loc[0]) != abs(move[1] - loc[1]):
            return False
        else:
            # down right
            if move[0] - loc[0] > 0 and move[1] - loc[1] > 0:
                for t in range(1, abs(move[0] - loc[0])):
                    if self.__board[loc[0] + t, loc[1] + t] != 0:
                        return False
            # down left
            elif move[0] - loc[0] > 0 > move[1] - loc[1]:
                for t in range(1, abs(move[0] - loc[0])):
                    if self.__board[loc[0] + t, loc[1] - t] != 0:
                        return False
            # up right
            elif move[0] - loc[0] < 0 < move[1] - loc[1]:
                for t in range(1, abs(move[0] - loc[0])):
                    if self.__board[loc[0] - t, loc[1] + t] != 0:
                        return False
            # up left
            else:
                for t in range(1, abs(move[0] - loc[0])):
                    if self.__board[loc[0] - t, loc[1] - t] != 0:
                        return False
            return True


#game = ChessGame(2)
#game.play_ball()

import pygame
import Constants
from Constants import SQUARE


# Class containing all of the pieces
class Pieces:
    def __init__(self, color):
        if color == 1:
            my_color = "w"
            op_color = "b"
        else:
            my_color = "b"
            op_color = "w"
        self.__My_piece = [pygame.image.load("images/" + my_color + "P.png"),
                           pygame.image.load("images/" + my_color + "R.png"),
                           pygame.image.load("images/" + my_color + "K.png"),
                           pygame.image.load("images/" + my_color + "B.png"),
                           pygame.image.load("images/" + my_color + "Q.png"),
                           pygame.image.load("images/" + my_color + "Ki.png")]
        self.__My_grave = [pygame.image.load("images/" + my_color + "P_s.png"),
                           pygame.image.load("images/" + my_color + "R_s.png"),
                           pygame.image.load("images/" + my_color + "K_s.png"),
                           pygame.image.load("images/" + my_color + "B_s.png"),
                           pygame.image.load("images/" + my_color + "Q_s.png"),
                           pygame.image.load("images/" + my_color + "Ki_s.png")]
        self.__Op_piece = [pygame.image.load("images/" + op_color + "P.png"),
                           pygame.image.load("images/" + op_color + "R.png"),
                           pygame.image.load("images/" + op_color + "K.png"),
                           pygame.image.load("images/" + op_color + "B.png"),
                           pygame.image.load("images/" + op_color + "Q.png"),
                           pygame.image.load("images/" + op_color + "Ki.png")]
        self.__Op_grave = [pygame.image.load("images/" + op_color + "P_s.png"),
                           pygame.image.load("images/" + op_color + "R_s.png"),
                           pygame.image.load("images/" + op_color + "K_s.png"),
                           pygame.image.load("images/" + op_color + "B_s.png"),
                           pygame.image.load("images/" + op_color + "Q_s.png"),
                           pygame.image.load("images/" + op_color + "Ki_s.png")]

    def get_piece(self, piece):
        if piece > 0:
            return self.__My_piece[piece - 1]
        else:
            return self.__Op_piece[-1 * piece - 1]

    def get_grave(self, piece):
        if piece > 0:
            return self.__My_grave[piece - 1]
        else:
            return self.__Op_grave[-1 * piece - 1]


# class definition for the 2-D array that stores the board and displaying it for pygame
class ChessBoard:
    # initialize the game board
    def __init__(self, color):
        if color == 1:
            self.__a = [-2, -3, -4, -5, -6, -4, -3, -2]  # Create game board lists of rows
        else:
            self.__a = [-2, -3, -4, -6, -5, -4, -3, -2]  # Create game board lists of rows
        self.__b = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.__c = [0, 0, 0, 0, 0, 0, 0, 0]
        self.__d = [0, 0, 0, 0, 0, 0, 0, 0]
        self.__e = [0, 0, 0, 0, 0, 0, 0, 0]
        self.__f = [0, 0, 0, 0, 0, 0, 0, 0]
        self.__g = [1, 1, 1, 1, 1, 1, 1, 1]
        if color == 1:
            self.__h = [2, 3, 4, 5, 6, 4, 3, 2]
        else:
            self.__h = [2, 3, 4, 6, 5, 4, 3, 2]
        self.__screen = pygame.display.set_mode(Constants.screen_size)
        # combine all the lists into one master list
        self.__chess = [self.__a, self.__b, self.__c, self.__d, self.__e, self.__f, self.__g, self.__h]
        self.game_pieces = Pieces(color)
        if color == 1:
            self.__color = [Constants.WHITE, Constants.BLACK]
        else:
            self.__color = [Constants.BLACK, Constants.WHITE]

    # define method to get specific item on board
    def __getitem__(self, tup):
        row, col = tup
        return self.__chess[row][col]

    # define method to set specific item on board
    def __setitem__(self, key, value):
        row, col = key
        self.__chess[row][col] = value

    # print out the board
    def print_board(self):
        for t in range(0, 8):
            # choose the colors for the squares
            if t % 2 == 1:
                x = Constants.PRIMARY
                y = Constants.SECONDARY
            else:
                x = Constants.SECONDARY
                y = Constants.PRIMARY
            # draw out each square
            pygame.draw.rect(Constants.screen, x, [0 * SQUARE + 3, SQUARE * t + 3, SQUARE, SQUARE])
            pygame.draw.rect(Constants.screen, y, [1 * SQUARE + 3, SQUARE * t + 3, SQUARE, SQUARE])
            pygame.draw.rect(Constants.screen, x, [2 * SQUARE + 3, SQUARE * t + 3, SQUARE, SQUARE])
            pygame.draw.rect(Constants.screen, y, [3 * SQUARE + 3, SQUARE * t + 3, SQUARE, SQUARE])
            pygame.draw.rect(Constants.screen, x, [4 * SQUARE + 3, SQUARE * t + 3, SQUARE, SQUARE])
            pygame.draw.rect(Constants.screen, y, [5 * SQUARE + 3, SQUARE * t + 3, SQUARE, SQUARE])
            pygame.draw.rect(Constants.screen, x, [6 * SQUARE + 3, SQUARE * t + 3, SQUARE, SQUARE])
            pygame.draw.rect(Constants.screen, y, [7 * SQUARE + 3, SQUARE * t + 3, SQUARE, SQUARE])
            # now we put the pieces on the board
            for i in range(0, 8):
                pic = self.__chess[t][i]
                if pic != 0:
                    Constants.screen.blit(self.game_pieces.get_piece(pic), [9 + i * SQUARE, 5 + t * SQUARE])
        # draw the graveyard at the bottom
        pygame.draw.rect(Constants.screen, self.__color[0], [3, 3 + SQUARE * 8, SQUARE * 4, SQUARE * 2])
        pygame.draw.rect(Constants.screen, self.__color[1], [3 + SQUARE * 4, 3 + SQUARE * 8, SQUARE * 4, SQUARE * 2])


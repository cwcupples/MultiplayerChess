import socket
import pygame
import ChessGame


PlayerSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print("Waiting for connection...")
try:
    PlayerSocket.connect((host, port))
except socket.error() as e:
    print(str(e))


def send_move(send_package):
    # piece_to_move, loc_piece_move, piece_taken, move_to
    # [   piece,       [row, col],     piece,     [row, col]    ]
    package = [send_package[0], send_package[1][0], send_package[1][1], send_package[2], send_package[3][0],
               send_package[3][1]]
    for i in range(len(package)):
        if package[i] < 0:
            package[i] *= -1
        PlayerSocket.sendall(package[i].to_bytes(32, 'big'))
        PlayerSocket.recv(1024)


def recv_move():
    package = []
    for i in range(6):
        p_response = PlayerSocket.recv(1024)
        package.append(int.from_bytes(p_response, 'big'))
    return package


def player_white():
    game = ChessGame.ChessGame(1)
    ChessGame.welcome()
    while game.winner() is None:
        game.display()
        # piece_to_move, loc_piece_move, piece_taken, move_to
        # [   piece,       [row, col],     piece,     [row, col]    ]
        send_move(game.my_turn())
        game.display()
        recv_package = recv_move()
        game.opp_turn(recv_package)
        game.display()
    game.print_winner()
    while True:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                quit()


def player_black():
    game = ChessGame.ChessGame(2)
    ChessGame.welcome()
    while game.winner() is None:
        game.display()
        recv_package = recv_move()
        game.opp_turn(recv_package)
        game.display()
        # piece_to_move, loc_piece_move, piece_taken, move_to
        # [   piece,       [row, col],     piece,     [row, col]    ]
        send_move(game.my_turn())
        game.display()
    game.print_winner()
    while True:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                quit()


# Initial welcome to server
Response = PlayerSocket.recv(1024)
print(Response.decode('utf-8'))             # Welcome to the server player...
# Waiting if client_1, Connected if client_2
while Response.decode('utf-8') != "Connected!":
    Response = PlayerSocket.recv(1024)
    print(Response.decode('utf-8'))         # player 1 = waiting for other player, player 2 = Connected!
Response = PlayerSocket.recv(1024)
# print(Response.decode('utf-8'))
if Response.decode('utf-8') == '1':
    # This player will be white
    player_white()
else:
    # This player is black
    player_black()

PlayerSocket.close()

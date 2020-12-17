import socket
import random

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
PlayerCount = 0
Player_list = []
game = True
# pick a random number to then determine the color of the players
Player_color = (random.randint(1, 10) % 2)
if Player_color == 0:
    send_player = 1
    recv_player = 0
else:
    send_player = 0
    recv_player = 1

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print("Waiting for connection...")
ServerSocket.listen(2)


while PlayerCount < 2:
    Player, address = ServerSocket.accept()
    PlayerCount += 1
    print("Connected to:" + address[0] + ':' + str(address[1]))
    print("Player Number:", PlayerCount)
    Player_list.append(Player)
    # tell the player what color they are going to be then update color
    Player.sendall(str.encode("Welcome to the Server, Player " + str(PlayerCount)))
    # notify player 1 they are waiting for the next player to join
    if PlayerCount == 1:
        Player.sendall(str.encode("\nWaiting for other Player.."))

# Notify the players we are ready
Player_list[0].sendall(str.encode("Connected!"))
Player_list[1].sendall(str.encode("Connected!"))
# Tell the players their color
print(Player_color)
Player_list[0].sendall(str.encode(str(Player_color)))
Player_color = (Player_color + 1) % 2
print(Player_color)
Player_list[1].sendall(str.encode(str(Player_color)))

while game:
    # here we just transfer the moves between the players
    for i in range(6):
        data = Player_list[send_player].recv(2048)
        if not data:
            game = False
        if data.decode('utf-8') == 'quit':
            Player_list[send_player].sendall(data)
            Player_list[recv_player].sendall(data)
            game = False
        Player_list[recv_player].sendall(data)
        # add this last line here so that the sending program knows the other player received
        Player_list[send_player].send(data)
    send_player = (send_player + 1) % 2
    recv_player = (recv_player + 1) % 2


Player_list[0].close()
Player_list[1].close()
ServerSocket.close()

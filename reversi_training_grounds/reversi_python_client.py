import reversi
import sys

if __name__ == '__main__':
    server_address = sys.argv[1]
    bot_move_number = int(sys.argv[2])
    strand = sys.argv[3]

    print("client", strand)

    reversi_game = reversi.ReversiGame(server_address, bot_move_number, strand)
    reversi_game.play()

#!/home/acaruso/anaconda3/bin/python
import os
import sys
import chess
import chess.pgn
import chess.engine #StockFish engine
import pandas as pd
import numpy as np

pgn = sys.stdin 
path = os.readlink('/proc/self/fd/0')
filename = path.split('/')[-1].split('.')[0] 
num_games = int(sys.argv[1:][0]) #the number of games from the pgn file to parse into csv representation
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish") #install with sudo apt-get install stockfish

count = 0 #count the number of games that have been parsed
scores = []
board_positions = []
piece_list = ('p','n','b','r','q','k','P','N','B','R','Q','K')

while chess.pgn.read_game(pgn):
    game = chess.pgn.read_game(pgn)
    board = game.board() #fresh game
    move_num = 1
    while not game.is_end(): #iterate through every board position in the game
        node = game.variations[0]
        board = game.board()
        game = node 

        feature_vector = [] #stores a length 768 representation of the current board position
        # 12 elements for each square, corresponding to each unique piece (black and white)
        # 1 if the square is occupied the player whose turn is, -1 if occupied by opposing player, 0 otherwise

        for square in str(board)[0::2]: #remove spaces between squares with [0::2]
            if square.islower() and move_num % 2 != 0: #whites move
                for piece in piece_list:
                    if square == piece:
                        feature_vector.append(np.int8(-1)) 
                    else:
                        feature_vector.append(np.int8(0))
            elif square.islower() and move_num % 2 == 0: #blacks move
                for piece in piece_list:
                    if square == piece:
                        feature_vector.append(np.int8(1))
                    else:
                        feature_vector.append(0)
            elif square.isupper() and move_num % 2 != 0: #whites move
                for piece in piece_list:
                    if square == piece:
                        feature_vector.append(np.int8(1))
                    else:
                        feature_vector.append(0)
            elif square.isupper() and move_num % 2 == 0: #blacks move
                for piece in piece_list:
                    if square == piece:
                        feature_vector.append(np.int8(-1))
                    else:
                        feature_vector.append(np.int8(0))
            else: # if the square is empty, append 12 0s (one for each piece)
                for i in range(12):
                    feature_vector.append(np.int8(0))

        board_positions.append(feature_vector)

        info = engine.analyse(board, chess.engine.Limit(time=0.100)) #get Stockfish score for current board position
        scores.append(str(info["score"]))

        move_num += 1

    count += 1
    if count%500 == 0:
        print(f"{count} games processed")

    if count == num_games: # write to csv and break loop
        features = pd.DataFrame(board_positions)
        response = pd.DataFrame(scores)
        data = pd.concat([features, response], axis=1)

        data.to_csv(f"./data/parsed/{filename}_{num_games}games.csv", sep=',', header=False, index=False, chunksize=100000)
        print('done parsing & wrote to csv')
        break

exit()

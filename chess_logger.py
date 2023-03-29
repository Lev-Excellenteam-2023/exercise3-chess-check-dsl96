import datetime
import logging

import chess_logger
import datetime as dt

import enums


class chess_logger():
    def __init__(self ):
        # Create and configure logger
        logging.basicConfig(level=logging.INFO,
                            filename="chess_log.log",
                            filemode='w')
        self.move_num = 0
        self.ai_player = None


    def start_new_game(self,board):

        log =f'\n *-----------------------------------*' +\
               '\n        NEW GAME                      '+\
               f'\n time start:{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '

        logging.info(log)
        self.log_board(board)

    def log_move(self, board, move):
        self.move_num += 1
        _from = (move.starting_square_row, move.starting_square_col)
        to = (move.ending_square_row ,move.ending_square_col)
        piece_name = move.moving_piece.get_name()
        player =  move.moving_piece.get_player()

        ai =''
        if player == self.ai_player:
            ai = 'ai '
        logging.info(f'\n\n{self.move_num}: {ai} player: {player} move {piece_name} from:{_from} to" {to}')
        self.log_board(board)

    def set_ai_mode(self, ai_player):
        '''
        set ai player
        so the log print its ai player
        '''
        self.ai = ai_player

    def warning(self, msg):
        logging.warning(msg)

    def log_check(self, player):
        logging.info(f'check to {player}')

    def log_undo_move(self, board, undo_move):
        self.move_num-=1
        logging.info("\nUNDO")
        self.log_move(board, undo_move)

    def game_over(self, board, winner=None):
        end_time = f' time end:{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        if winner:
            logging.info(f'\nGAME OVER\n '
                         f'number of moves: {self.move_num}+ '
                         f'\n{end_time}{winner} won')
        else:
            logging.info(f'\nGAME OVER\n number of moves: {self.move_num}+ \n{end_time}+\nno winner')

    def log_board(self,board):
        for row in board:
            row_to_log =''
            for p in row:
                 if p is enums.Player.EMPTY:
                     row_to_log = row_to_log + ' -- '
                 else:

                     if p.get_player() == enums.Player.PLAYER_1:
                         player = 'W'
                     else:
                         player = 'B'

                     row_to_log = row_to_log +' '+player+':'+ p.get_name()
            logging.info(row_to_log)








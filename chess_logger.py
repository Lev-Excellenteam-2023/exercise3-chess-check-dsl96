import datetime
import logging

import chess_logger
import datetime as dt

import enums


class chess_logger():
    def __init__(self):
        # Create and configure logger
        logging.basicConfig(level=logging.INFO,
                            filename="chess_log.log",
                            filemode='a')
        self.move_num = 0
        self.ai_player = None
        self.w_first_eat = None
        self.b_first_eat = None

        self.count_knight_move = 0

    def start_new_game(self, board):

        log = f'\n *-----------------------------------*' + \
              '\n        NEW GAME                      ' + \
              f'\n time start:{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '

        logging.info(log)
        self.log_board(board)

        self.move_num = 0
        self.ai_player = None
        self.w_first_eat = None
        self.b_first_eat = None


    def log_move(self, board, move):
        self.move_num += 1

        if move.removed_piece != enums.Player.EMPTY:
            if not self.w_first_eat and move.removed_piece.get_player() == enums.Player.PLAYER_1:
                self.w_first_eat = self.move_num
            elif not self.b_first_eat and move.removed_piece.get_player() == enums.Player.PLAYER_2:
                self.b_first_eat = self.move_num

        _from = (move.starting_square_row, move.starting_square_col)
        to = (move.ending_square_row, move.ending_square_col)
        piece_name = move.moving_piece.get_name()
        player = move.moving_piece.get_player()

        if piece_name == 'n':
            self.count_knight_move += 1
        ai = ''
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
        self.move_num -= 1
        logging.info("\nUNDO")
        self.log_move(board, undo_move)

    def game_over(self, board, winner=None):
        end_time = f' time end:{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

        log_msg = f'\nGAME OVER\n ' \
                  f'number of moves: {self.move_num}' \
                  f'\n{end_time}'
        if winner:
            log_msg += f'{winner} won'
        else:
            log_msg += 'no winner'

        if self.w_first_eat:
            log_msg += f'\nfirst W eaten {self.w_first_eat}\n'
        if self.b_first_eat:
            log_msg += f'\nfirst B eaten {self.b_first_eat}\n'

        log_msg += f'sum knight moves: {self.count_knight_move}'

        logging.info(log_msg)


    def log_board(self, board):
        for row in board:
            row_to_log = ''
            for p in row:
                if p is enums.Player.EMPTY:
                    row_to_log = row_to_log + ' --- '
                else:

                    if p.get_player() == enums.Player.PLAYER_1:
                        player = 'W'
                    else:
                        player = 'B'

                    row_to_log = row_to_log + ' ' + player + ':' + p.get_name()
            logging.info(row_to_log)

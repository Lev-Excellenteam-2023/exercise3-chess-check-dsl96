#
# The GUI engine for Python Chess
#
# Author: Boo Sung Kim, Eddie Sharick
# Note: The pygame tutorial by Eddie Sharick was used for the GUI engine. The GUI code was altered by Boo Sung Kim to
# fit in with the rest of the project.
#
import chess_engine
import pygame as py

import ai_engine
from enums import Player
import random


"""Variables"""
WIDTH = HEIGHT = 512  # width and height of the chess board
DIMENSION = 8  # the dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSION  # the size of each of the squares in the board
MAX_FPS = 20  # FPS for animations
IMAGES = {}  # images for the chess pieces
colors = [py.Color("white"), py.Color("gray")]

# TODO: AI black has been worked on. Mirror progress for other two modes
def load_images():
    '''
    Load images for the chess pieces
    '''
    for p in Player.PIECES:
        IMAGES[p] = py.transform.scale(py.image.load("images/" + p + ".png"), (SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, game_state, valid_moves, square_selected):
    ''' Draw the complete chess board with pieces

    Keyword arguments:
        :param screen       -- the pygame screen
        :param game_state   -- the state of the current chess game
    '''
    draw_squares(screen)
    highlight_square(screen, game_state, valid_moves, square_selected)
    draw_pieces(screen, game_state)


def draw_squares(screen):
    ''' Draw the chess board with the alternating two colors

    :param screen:          -- the pygame screen
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            py.draw.rect(screen, color, py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, game_state):
    ''' Draw the chess pieces onto the board

    :param screen:          -- the pygame screen
    :param game_state:      -- the current state of the chess game
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = game_state.get_piece(r, c)
            if piece is not None and piece != Player.EMPTY:
                screen.blit(IMAGES[piece.get_player() + "_" + piece.get_name()],
                            py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_square(screen, game_state, valid_moves, square_selected):
    if square_selected != () and game_state.is_valid_piece(square_selected[0], square_selected[1]):
        row = square_selected[0]
        col = square_selected[1]

        if (game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_1)) or \
                (not game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_2)):
            # hightlight selected square
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(py.Color("blue"))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

            # highlight move squares
            s.fill(py.Color("green"))

            for move in valid_moves:
                screen.blit(s, (move[1] * SQ_SIZE, move[0] * SQ_SIZE))

def random_bool():
     if not bool(random.getrandbits(2)):
         return False
     else: return True
def other_player(player):
    if player is Player.PLAYER_1:
        return Player.PLAYER_2
    else:
        return Player.PLAYER_1

from datetime import datetime

def main():
    start_time = datetime.now()
    print(start_time)
    for _ in range(10):
        py.init()
        screen = py.display.set_mode((WIDTH, HEIGHT))
        clock = py.time.Clock()

        load_images()
        running = True
        square_selected = ()  # keeps track of the last selected square
        player_clicks = []  # keeps track of player clicks (two tuples)
        valid_moves = []
        game_over = False
        ai = ai_engine.chess_ai()
        game_state = chess_engine.game_state()

        # log
        game_state.set_ai_mode(ai_player=Player.PLAYER_2)

        turn = Player.PLAYER_1
        while running:

            do_ai_move = random_bool()

            if do_ai_move:
                    if turn is Player.PLAYER_2:
                        ai_move = ai.minimax_white(game_state, 3, -100000, 100000, True, Player.PLAYER_2)
                    elif turn is Player.PLAYER_1:
                        ai_move = ai.minimax_black(game_state, 3, -100000, 100000, True, Player.PLAYER_1)

                    if type(ai_move) != int:
                       game_state.move_piece(ai_move[0], ai_move[1], True, log=True)
                       print('ai')
            else:
                all_valid_move = game_state.get_all_legal_moves(turn)
                rand_move = random.choice(all_valid_move)
                game_state.move_piece(rand_move[0], rand_move[1],True, log=True)
                print("rand")



            turn  = other_player(turn)
            draw_game_state(screen, game_state, valid_moves, square_selected)

            endgame = game_state.checkmate_stalemate_checker()
            if endgame == 0:
                    game_over = True
                    draw_text(screen, "Black wins.")
                    running = False
            elif endgame == 1:
                    game_over = True
                    draw_text(screen, "White wins.")
                    running = False
                    #return
            elif endgame == 2:
                    game_over = True
                    draw_text(screen, "Stalemate.")
                    running = False
                    #return


            clock.tick(MAX_FPS)
            py.display.flip()

            elapsed = datetime.now() - start_time
            if elapsed.seconds/60 > 90:
                print('end time')
                return

def draw_text(screen, text):
    font = py.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, False, py.Color("Black"))
    text_location = py.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                      HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)


if __name__ == "__main__":
    main()

import numpy
import time

class Player:
    Black = 8
    White = 16

class Piece:
    Empty = 0
    Pawn = 1
    Knight = 2
    Bishop = 3
    Rook = 4
    Queen = 5
    King = 6

    Black = 8
    White = 16

class Move:    
    def __init__(self, start_square, target_square):
        self.start_square = start_square
        self.target_square = target_square


class Board:
    def __init__(self):
        self.board = numpy.array([0]*64)
        self.to_play = Player.White
    
    def make_move(self, move):
        self.board[move.target_square] = self.board[move.start_square]
        self.board[move.start_square] = Piece.Empty

        self.to_play = Player.Black if self.to_play == Player.White else Player.White

    def print(self):
        for y in range(64):
            if(y % 8 == 0):
                print("", end="\033[49m\033[39m\n" if y != 0 else "\n")
                print(str(int(((64 - y) / 8))) + " ", end = "")
            print(Board.print_piece(self.board[int((63 - y) / 8) * 8 + y % 8], y % 2 + int(y / 8) % 2), end = "")

        print("\033[49m\033[39m\n   a  b  c  d  e  f  g  h", end="\n\n")

        print("To play: " + ("white" if self.to_play & Player.White else "black"))
    
    def print_piece(piece, squarecolor):
        piece_character = " "
        match piece & 7:
            case Piece.Pawn:
                piece_character = "♟︎"
            case Piece.Knight:
                piece_character = "♞"
            case Piece.Bishop:
                piece_character = "♝"
            case Piece.Rook:
                piece_character = "♜"
            case Piece.Queen:
                piece_character = "♛"
            case Piece.King:
                piece_character = "♚"
     
        padding_left = ' '
        padding_right = ' '


        piece_character = padding_left + piece_character + padding_right

        foreground = ""
        if piece & Piece.Black > 0:
            foreground = "\033[38;5;0m"
        if piece & Piece.White > 0:
            foreground = "\033[38;2;255;255;255m"

        background = "\033[48;5;215m" if squarecolor == 1 else "\033[48;5;94m"

        return foreground + background + piece_character

    def from_fen(pgn):
        chessboard = Board()
        board = chessboard.board
        head = 0
        for character in pgn:
            if character.isnumeric():
                head += int(character)
                continue

            if character == '/':
                continue

            color = Piece.White if character.isupper() else Piece.Black

            piece = Piece.Empty
            character = character.lower()
            match character:
                case 'p':
                    piece = Piece.Pawn
                case 'n':
                    piece = Piece.Knight
                case 'b':
                    piece = Piece.Bishop
                case 'r':
                    piece = Piece.Rook
                case 'q':
                    piece = Piece.Queen
                case 'k':
                    piece = Piece.King

            board[int((63 - head) / 8) * 8 + head % 8] = piece + color
            head += 1
            if head >= 64:
                break
        return chessboard

    def initial():
        return Board.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

class Chess:
    def __init__(self):
        self.gamestate = Board.initial()

    def print(self):
        self.gamestate.print()

start = time.time()
c = Chess()

c.print()
end = time.time()
print(f"ended in {end - start} seconds")
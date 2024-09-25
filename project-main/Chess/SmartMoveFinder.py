import random



CHECKMATE = 1000
STALEMATE = 0


def FindBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    findMoveNegaMax(gs, validMoves, 3, float('-inf'), float('inf'), 1 if gs.whiteToMove else -1)
    return nextMove

# Modify findMoveNegaMax function to prioritize capturing moves
def findMoveNegaMax(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scorePosition(gs)

    # Order moves based on captures and checks
    ordered_moves = prioritizeMoves(gs, validMoves)

    for playerMove in ordered_moves:
        gs.makeMove(playerMove)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        gs.undoMove()

        if score > alpha:
            alpha = score
            if depth == 3:
                nextMove = playerMove
        if alpha >= beta:
            break

    return alpha

# Function to prioritize moves (for example, capturing moves first)
def prioritizeMoves(gs, moves):
    capture_moves = [move for move in moves if gs.board[move.endRow][move.endCol] != '--']
    non_capture_moves = [move for move in moves if move not in capture_moves]
    ordered_moves = capture_moves + non_capture_moves
    return ordered_moves


def scorePosition(gs):
    score = 0

    # Piece values
    score += scoreMaterial(gs.board)

    # Mobility - count available moves
    white_moves = len(gs.getValidMoves()) if gs.whiteToMove else 0
    black_moves = len(gs.getValidMoves()) if not gs.whiteToMove else 0
    score += (white_moves - black_moves)

    # Pawn structure
    score += scorePawnStructure(gs)

    # King safety - check if kings are protected
    score += scoreKingSafety(gs)

    return score

def scoreMaterial(board):
    piece_values = {
        'p': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100
    }
    score = 0
    for row in board:
        for piece in row:
            if piece[0] == 'w':
                score += piece_values[piece[1]]
            elif piece[0] == 'b':
                score -= piece_values[piece[1]]
    return score

def scorePawnStructure(gs):
    score = 0
    for r in range(len(gs.board)):
        for c in range(len(gs.board[r])):
            if gs.board[r][c][1] == 'p':  # Check if it's a pawn
                # Evaluate based on pawn structure, pawn islands, doubled pawns, etc.
                # Example: penalize for doubled pawns
                score -= 10  # Adjust this score based on your evaluation criteria

                # Example: give a bonus for pawns close to promotion
                if (gs.board[r][c][0] == 'w' and r < 3) or (gs.board[r][c][0] == 'b' and r > 4):
                    score += 20  # Adjust as needed

                # More evaluations based on pawn structure can be added
    return score

def scoreKingSafety(gs):
    white_king_row, white_king_col = gs.whiteKingLocation
    black_king_row, black_king_col = gs.blackKingLocation
    score = 0

    # Evaluate based on the king's position
    if gs.whiteToMove:
        # Example: Give a bonus for a shield of pawns in front of the king
        if white_king_row < 4 and gs.board[white_king_row + 1][white_king_col] == '--':
            score += 30  # Adjust this bonus

        # Evaluate if the king is exposed to checks or threats
        if gs.squareUnderAttack(white_king_row, white_king_col):
            score -= 50  # Penalize for an exposed king
    else:
        # Similar evaluations for black king if it's black's turn
        # Example: Give a bonus for a shield of pawns in front of the king
        if black_king_row > 3 and gs.board[black_king_row - 1][black_king_col] == '--':
            score += 30  # Adjust this bonus

        # Evaluate if the king is exposed to checks or threats
        if gs.squareUnderAttack(black_king_row, black_king_col):
            score -= 50  # Penalize for an exposed king

    return score



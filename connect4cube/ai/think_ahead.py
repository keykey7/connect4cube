from connect4cube.ai.board import CBoard
from connect4cube.ai.check import is_win


WIN_SCORE = 1000
MAX_SCORE = 1124


def negamax(board: CBoard, opponent_move_id, depth, alpha, beta):
    board.nodes_counter += 1
    if depth == 0:
        return 0  # not the best estimation :)

    # ok let's do the actual move
    board.move(opponent_move_id)
    possible_moves = board.get_valid_moves()

    # quick lookahead of 1
    for next_move_id in possible_moves:
        if is_win(board, next_move_id):
            board.undo_move()
            return MAX_SCORE - board.round  # we win, yay!

    # quick lookahead of 2
    forced_move_id = -1
    board.current_player ^= 1  # quick zero-move
    for next_move_id in possible_moves:
        if is_win(board, next_move_id):
            if forced_move_id != -1:
                # we will loose next round
                board.current_player ^= 1  # reset to actual player
                board.undo_move()
                return -(MAX_SCORE - board.round - 1)
            forced_move_id = next_move_id
    board.current_player ^= 1

    if forced_move_id != -1:
        sorted_moves = [forced_move_id]
    else:
        # TODO: actual sorting
        sorted_moves = possible_moves

    best_score = -MAX_SCORE
    for next_move_id in sorted_moves:
        current_score = -negamax(board, next_move_id, depth - 1, -beta, -alpha)
        if current_score > best_score:
            best_score = current_score
            if best_score > alpha:
                alpha = best_score
                if alpha >= beta:
                    board.beta_cutoffs += 1
                    break  # cut-off
    board.undo_move()
    return best_score


def negamax_full(board: CBoard, depth=3):
    """
    :param board:
    :param depth: search depth
    :param alpha: minimum score we assume to achieve
    :param beta: maximum score we assume to achieve
    :return:
    """
    sorted_moves = board.get_valid_moves()
    results = []
    for next_move_id in sorted_moves:
        if is_win(board, next_move_id):
            current_score = MAX_SCORE - board.round
        else:
            current_score = -negamax(board, next_move_id, depth, -MAX_SCORE, MAX_SCORE)
        results.append((next_move_id, current_score))
    return sorted(results, key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    board = CBoard()
    board.move(1)
    board.move(6)
    board.move(2)
    board.move(7)
    print(board)
    best_move = negamax_full(board)
    print(best_move)

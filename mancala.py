import time


def get_possible_actoins(s):
    if s[1] == 1:
        return [i for i, value in enumerate(s[0][0:6]) if not value == 0]
    else:
        return [i + 7 for i, value in enumerate(s[0][7:13]) if not value == 0]


def get_result_state_without_steeling(s, a):
    # TODO: raise exception if unallowed action is passed
    board, player = s[:]
    s_new = board[:], player
    s_new = list(s_new)
    num_of_stones = s[0][a]
    index = 1
    s_new[0][a] = 0
    while num_of_stones > 0:
        if (s[1] == 0 and (a + index) % 14 == 6) or (s[1] == 1 and (a + index) % 14 == 13):
            index += 1
        s_new[0][(a + index) % 14] += 1
        index = (index + 1) % 14
        num_of_stones -= 1
    index -= 1
    if (a + index) % 14 == 6:
        s_new[1] = 1
    elif (a + index) % 14 == 13:
        s_new[1] = 0
    else:
        s_new[1] = int(not bool(s[1]))
    return tuple(s_new)


def get_result_state_with_steeling(s, a):
    # TODO: raise exception if unallowed action is passed
    board, player = s[:]
    s_new = board[:], player
    s_new = list(s_new)
    num_of_stones = s[0][a]
    index = 1
    s_new[0][a] = 0
    while num_of_stones > 0:
        if (s[1] == 0 and (a + index) % 14 == 6) or (s[1] == 1 and (a + index) % 14 == 13):
            index += 1
        s_new[0][(a + index) % 14] += 1
        index = (index + 1) % 14
        num_of_stones -= 1
    index -= 1
    last_index = (a + index) % 14
    if s_new[0][last_index] == 1 and (not last_index == 6) and (not last_index == 13) \
            and ((last_index < 6 and s[1] or last_index > 6 and not s[1])):
        s_new[0][last_index] = 0
        s_new[0][6 * s[1] + 13 * (1 - s[1])] += s_new[0][12 - last_index] + 1
        s_new[0][12 - last_index] = 0
    if last_index == 6:
        s_new[1] = 1
    elif last_index == 13:
        s_new[1] = 0
    else:
        s_new[1] = int(not bool(s[1]))
    return tuple(s_new)


def is_end_game(s):
    if all([i == 0 for i in s[0][:6]]) or all([i == 0 for i in s[0][7:13]]):
        # print(s)
        return True
    else:
        return False


def evaluate_state_score(s):
    if is_end_game(s):
        if s[0][6] > s[0][13]:
            return float('inf')
        elif s[0][6] < s[0][13]:
            return float('-inf')
        else:
            return 0
    return (s[0][6] - s[0][13])


def max_value(s, depth, alpha=float('-inf'), beta=float('inf'), stealing=True):
    if is_end_game(s) or depth == 0:
        return evaluate_state_score(s), -1
    v = float('-inf')
    action = -1
    for a in get_possible_actoins(s):
        v_prev = v
        if stealing:
            v = max(v, min_value(get_result_state_with_steeling(s, a), depth - 1, alpha, beta)[0])
        else:
            v = max(v, min_value(get_result_state_without_steeling(s, a), depth - 1, alpha, beta)[0])
        if not v == v_prev:
            action = a
        if v > alpha:
            alpha = v
        if alpha > beta:
            break
    return v, action


def min_value(s, depth, alpha=float('-inf'), beta=float('inf'), stealing=True):
    if is_end_game(s) or depth == 0:
        return evaluate_state_score(s), -1
    v = float('inf')
    action = -1

    for a in get_possible_actoins(s):
        v_prev = v
        if stealing:
            v = min(v, max_value(get_result_state_with_steeling(s, a), depth - 1, alpha, beta)[0])
        else:
            v = min(v, max_value(get_result_state_without_steeling(s, a), depth - 1, alpha, beta)[0])
        if not v == v_prev:
            action = a
        if v < beta:
            beta = v
        if alpha > beta:
            break
    return v, action

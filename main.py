from random import randint

board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
thisdict = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 7,
    "H": 8,
    "I": 9,
    "J": 10,
    "K": 11,
    "L": 12,
}


def convert(str):
    return thisdict[str.upper()]


def Game_design(board):
    print("    ,|L:{}|,|K:{}|,|J:{}|,|I:{}|,|H:{}|,|G:{}|,".format(board[12], board[11], board[10], board[9], board[8],
                                                                   board[7]))
    print("|{}|                                          |{}|".format(board[13], board[6]))
    print("    ,|A:{}|,|B:{}|,|C:{}|,|D:{}|,|E:{}|,|F:{}|,".format(board[0], board[1], board[2], board[3], board[4],
                                                                   board[5]))




def moving(board, num, stealing):
    flag = 0
    sum = board[num]
    board[num] = 0
    index = num + 1
    for i in range(sum):

        if index == 6:
            if num > 5:
                index += 1
                board[index % 14] += 1
            else:
                board[index % 14] += 1
        elif index == 13:
            if num <= 5:
                index += 1
                board[index % 14] += 1
            else:
                board[index % 14] += 1
        else:
            board[index % 14] += 1

        index += 1
    vr = index - 1 % 14
    if (stealing):
        if num <= 5 and vr <= 5:
            if board[vr] == 1:
                if board[12 - vr] != 0:
                    board[6] += (board[12 - vr] + 1)
                    board[12 - vr], board[vr] = 0, 0
        elif num > 6 and 6 < vr < 13:
            if board[vr] == 1:
                if board[12 - vr] != 0:
                    board[13] += (board[12 - vr] + 1)
                    board[vr], board[12 - vr] = 0, 0

    if vr == 6 or vr == 13:
        flag = 1

    return flag


def is_end(board):  # check if game is end
    if sum(board[0:6]) == 0 or sum(board[7:13]) == 0:
        board[13] += sum(board[7:13])
        board[6] += sum(board[0:6])
        for i in range(14):
            if i != 13 and i != 6:
                board[i] = 0
        return True
    return False


def end_of_game(board):  # if game is end so print scores
    flag = 0
    if is_end(board):
        Game_design(board)
        flag = 1
        print("Game over")
        if board[6] > board[13]:
            print("player one win ")
            print("score", board[6], ":", board[13])

        else:
            print("player two win ")
            print("score", board[13], ":", board[6])
        for i in range(14):
            if i != 13 and i != 6:
                board[i] = 0
    return flag


value = randint(0, 1)  # if value = 0 player start else bot start
if value == 0:
    print("=============== Player One ===============")
else:
    print("=============== Player Two ===============")
Game_design(board)
print("==========================================")
playing = True
bot = False
playerone = True

if value == 1:
    playerone = False
    bot = True

while playing:

    playagain = 0
    while playerone:
        num = input("player one Enter the number: ")
        num = convert(num)
        if 0 <= num <= 5 and board[num] != 0:
            playagain = moving_withstealing(board, num)

            Game_design(board)
            print("==========================================")
            print("\n")
            if playagain != 1:
                playerone = False
        else:
            print("invalid play")
            print("\n")
        bot = True
        if is_end(board):
            playing = False
            break

    playagain = 0
    if end_of_game(board):
        playing = False
        break

    while bot:
        num = input("player two Enter the number")
        num = convert(num)

        if 7 <= num <= 12 and board[num] != 0:
            playagain = moving_withstealing(board, num)

            print("=============that is bot ================")
            Game_design(board)
            print("==========================================")
            if playagain != 1:
                bot = False
        else:
            print("invalid play")
            print("\n")
        playerone = True
        if is_end(board):
            playing = False
            break

    if end_of_game(board):
        playing = False
        break

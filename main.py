from random import randint
from datetime import datetime
import mancala
from mancala import max_value, min_value
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
loadList = []

def convert(str):
    return thisdict[str.upper()]


def get_key(val):
    for key, value in thisdict.items():
        if val == value:
            return key


def listToString(s):
    # initialize an empty string
    return ' '.join([str(elem) for elem in s])


def save(board, playerOne, mode, stealing):
    f = open("data.txt", "a")
    st = listToString(
        [str(datetime.now()), ",", listToString(board), ",", str(playerOne), ",", str(mode), ",", str(stealing), "\n"])
    f.write(st)
    f.close()


def load():
    f = open("data.txt", "r")
    string = ""
    string = f.read()
    loadList = str(string).split("\n")
    for i in range(len(loadList) - 1):
       print(i + 1, "    ", str(loadList[i]).replace(",", "     "))
    loadGame = int(input("Pick a game to load: "))
    string = loadList[loadGame - 1]
    loaded = str(string).split(",")
    f.close()
    return loaded


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


playerone = True
bot = False
stealing = 0
depth = 7
loadGame = int(input("Enter 0 for New Game, 1 to Load a saved game: "))
if loadGame == 1:
    loadedGame = load()
    temp = loadedGame[1].split(" ")
    for i in range(len(temp)):
        board [i] = int(temp[i])
    if loadedGame[2] != "True":
        playerone = False
        bot = True
        print("=============== Player Two ===============")
    else:
        print("=============== Player One ===============")
    Game_design(board)
    print("==========================================")
    depth = int(loadedGame[3])
    stealing = int(loadedGame[4])
else:
    stealing = int(input("Enter 1 for stealing and 0 for not stealing: "))
    mode = int(input("Enter 1 for easy ,2 for medium and 3 for hard "))
    if mode == 1:
        depth = 4
    elif mode == 2:
        depth = 7
    else:
        depth = 10
    value = randint(0, 1)  # if value = 0 player start else bot start
    if value == 0:
        print("=============== Player One ===============")
    else:
        playerone = False
        bot = True
        print("=============== Player Two ===============")
    Game_design(board)
    print("==========================================")


playing = True
while playing:

    playagain = 0
    while playerone:
        num = input("player one Enter the number: ")
        if num == "save":
            save(board, playerone, depth, stealing)
            num = input("player one Enter the number: ")
        num = convert(num)
        if 0 <= num <= 5 and board[num] != 0:
            playagain = moving(board, num, stealing)
            print("Move ==> {}".format(get_key(num)))
            Game_design(board)
            print("==========================================")
            if playagain != 1:
                playerone = False
        else:
            print("invalid play")
            print("\n")
        bot = True

    playagain = 0
    if end_of_game(board):
        playing = False
        break

    while bot:
        # num = input("player two Enter the number")
        # num = convert(num)
        # _, num = minnmax(board, depth, -100000, 100000, True, stealing)
        _, num = min_value((board, 0), depth, stealing = stealing)
        if 7 <= num <= 12 and board[num] != 0:
            playagain = moving(board, num, stealing)
            print("Move ==> {}".format(get_key(num)))
            print("=============that is bot ================")
            Game_design(board)
            print("==========================================")
            if playagain != 1:
                bot = False
        elif num == -1:
            end_of_game(board)
            playing = False
            break
        else:
            print("invalid play")
            print("\n")
        playerone = True

    if end_of_game(board):
        playing = False
        break

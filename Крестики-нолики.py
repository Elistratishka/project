def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def game_board():
    size = input('Введите размер игрового поля(по умолчанию 3): ')
    if size:
        try:
            size = int(size)
        except ValueError:
            size = 3
    else:
        size = 3
    board = [['-' for j in range(size)] for i in range(size)]
    return board, size


def print_board(board, size):
    for i in range(size):
        print(board[i])

def players():
    first = input('Введите имя первого игрока: ')
    second = input('Введите имя второго игрока: ')
    if len(first) == 0:
        first = 'X'
    if len(second) == 0:
        second = 'O'
    return first, second


def result(play_ground, size):
    r = size-1
    res = []
    tab = []
    diag = []
    rev_diag = []
    for i in range(size):
        if len(set(play_ground[i])) == 1:
            if set(play_ground[i]) != '-':
                return set(play_ground[i])
    for n in range(size):
        for j in range(size):
            res.append(play_ground[j][n])
    tab = split(res, size)
    for k in range(size):
        if len(set(tab[k])) == 1:
            if set(tab[k]) != '-':
                return set(tab[k])
    for t in range(size):
        m = t
        diag.append(play_ground[m][t])
    if len(set(diag)) == 1:
        if set(diag) != '-':
            return set(diag)
    for i in range(size):
        rev_diag.append(play_ground[i][r])
        r-=1
    if len(set(rev_diag)) == 1:
        if set(rev_diag) != '-':
            return set(rev_diag)


def input_and_check(board, player, item):
    x = input(f'{player} введите строку: ')
    y = input(f'{player} введите столбец: ')
    while True:
        try:
            x = int(x)
            y = int(y)
            board[x - 1][y - 1] = item
        except ValueError:
            x = input('Строка - ведите цифру: ')
            y = input('Столбец - введите цифру: ')
            continue
        except IndexError:
            x = input('Строка - ведите цифру в пределах поля: ')
            y = input('Столбец - ведите цифру в пределах поля: ')
            continue
        else: return x, y
        break


def game():
    print('''Добро пожаловать в игру "крестики-нолики"!''')
    print('Размер игрового поля по умолчанию 3x3, но при желании можно использовать любое поле')
    print('Нумерация строк и столбцов начинается с 1, а не с 0')
    print("Занятые другим игроком клетки можно перезаписывать (можно, конечно, это доработать, но пусть будет фича)")
    print('Побеждает игрок, полностью занявший строку, столбец или диагональ игрового поля')
    player_1, player_2 = players()
    print(f'Первый игрок {player_1}')
    print(f'Второй игрок {player_2}')
    board, size = game_board()
    while True:
        print_board(board, size)
        item_1 = 'X'
        input_and_check(board, player_1, item_1)
        print_board(board, size)
        winner = result(board, size)
        if winner == {'X'}:
            print(f"Победил {player_1}")
            break
        item_2 = 'O'
        input_and_check(board, player_2, item_2)
        winner = result(board, size)
        if winner == {'O'}:
            print(f'Победил {player_2}')
            break

game()











from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Клетка за паределами доски!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Клетка уже была использована!"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, start, long, direction):
        self.long = long
        self.start = start
        self.direction = direction
        self.health = long

    @property
    def dots(self):
        ship_dots = []
        head_x = self.start.x
        head_y = self.start.y
        for i in range(self.long):
            if not self.direction:
                head_x += 1
            elif self.direction:
                head_y += 1

            ship_dots.append(Dot(head_x, head_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count_ship = 0

        self.game_board = [[chr(9898)] * size for _ in range(size)]

        self.used_dots = []
        self.list_ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.used_dots:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.game_board[d.x][d.y] = chr(9724)
            self.used_dots.append(d)

        self.list_ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.used_dots:
                    if verb:
                        self.game_board[cur.x][cur.y] = "T"
                    self.used_dots.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.game_board):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace(chr(9724), chr(9898))
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.used_dots:
            raise BoardUsedException()

        self.used_dots.append(d)

        for ship in self.list_ships:
            if d in ship.dots:
                ship.lives -= 1
                self.game_board[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count_ship += 1
                    self.contour(ship, verb=True)
                    print("Убил!")
                    return True
                else:
                    print("Попал!")
                    return True

        self.game_board[d.x][d.y] = "T"
        print("Мимо!")
        return False

    def begin(self):
        self.used_dots = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print(" в украденной игре ")
        print("    морской бой    ")
        print("    мне немного    ")
        print("не хватило времени")
        print("на выходных добью:)")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
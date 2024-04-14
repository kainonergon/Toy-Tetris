from typing import Callable

PIECES = {
    'O': [[(1, 0), (1, 1), (2, 1), (2, 0)]],
    'I': [[(1, 0), (1, 1), (1, 2), (1, 3)],
          [(0, 0), (1, 0), (2, 0), (3, 0)]],
    'S': [[(1, 0), (2, 0), (1, 1), (0, 1)],
          [(1, 0), (1, 1), (2, 1), (2, 2)]],
    'Z': [[(1, 0), (2, 0), (2, 1), (3, 1)],
          [(2, 0), (2, 1), (1, 1), (1, 2)]],
    'L': [[(1, 0), (1, 1), (1, 2), (2, 2)],
          [(2, 0), (2, 1), (1, 1), (0, 1)],
          [(1, 0), (2, 0), (2, 1), (2, 2)],
          [(3, 0), (2, 0), (1, 0), (1, 1)]],
    'J': [[(2, 0), (2, 1), (2, 2), (1, 2)],
          [(2, 1), (2, 0), (1, 0), (0, 0)],
          [(2, 0), (1, 0), (1, 1), (1, 2)],
          [(1, 0), (1, 1), (2, 1), (3, 1)]],
    'T': [[(1, 0), (1, 1), (1, 2), (2, 1)],
          [(1, 0), (0, 1), (1, 1), (2, 1)],
          [(2, 0), (2, 1), (2, 2), (1, 1)],
          [(1, 0), (2, 0), (3, 0), (2, 1)]]
}


class Tetris:
    def __init__(self, width_: int = 10, height_: int = 20):
        self.width: int = width_
        self.height: int = height_
        self.piece: str = ''
        self.direction: int = 0
        self.x: int = (self.width - 4) // 2
        self.y: int = 0
        self.is_running: bool = True
        self.commands: dict[str: Callable] = {
            'exit': self.exit,
            'rotate': self.rotate,
            'left': self.left,
            'right': self.right,
            'down': self.down,
            'piece': self.new_piece,
            'break': self.remove_line
        }
        self.board: list[str] = ['-' * self.width for _ in range(self.height)]

    def run(self):
        while self.is_running:
            self.show()
            command = input()
            if command in self.commands:
                self.commands[command]()

    def exit(self):
        self.is_running = False

    def new_piece(self):
        self.piece = input()
        self.x = (self.width - 4) // 2
        self.y = 0
        self.direction = 0

    def rotate(self):
        if self.check_bottom():
            return
        new_direction = (self.direction + 1) % len(PIECES[self.piece])
        if not self.check_wall(direction=new_direction):
            self.direction = new_direction
        self.down()

    def left(self):
        if self.check_bottom():
            return
        self.x += (0 if self.check_wall(-1) else -1)
        self.down()
    
    def right(self):
        if self.check_bottom():
            return
        self.x += (0 if self.check_wall(1) else 1)
        self.down()

    def down(self):
        if not self.check_bottom():
            self.y += 1

    def check_wall(self, x_offset: int = 0, y_offset: int = 0, direction=None) -> bool:
        if direction is None:
            direction = self.direction
        if self.piece in PIECES:
            for dx, dy in PIECES[self.piece][direction]:
                check_x = self.x + dx + x_offset
                check_y = self.y + dy + y_offset
                if (check_x < 0 or check_x >= self.width or check_y >= self.height
                        or self.board[check_y][check_x] == '0'):
                    return True
        return False

    def check_bottom(self) -> bool:
        if self.check_wall(y_offset=1):
            self.fix_piece()
            return True
        return False

    def remove_line(self):
        for index, line in enumerate(self.board):
            if line == '0' * self.width:
                self.board.pop(index)
                self.board.insert(0, '-' * self.width)

    def fix_piece(self):
        grid = [list(line) for line in self.board]
        if self.piece in PIECES:
            for dx, dy in PIECES[self.piece][self.direction]:
                grid[self.y + dy][self.x + dx] = '0'
        self.piece = ''
        self.board = [''.join(row) for row in grid]
        if '0' in self.board[0]:
            self.show()
            print('Game Over!')
            self.exit()

    def show(self):
        grid = [list(line) for line in self.board]
        if self.piece in PIECES:
            for dx, dy in PIECES[self.piece][self.direction]:
                grid[self.y + dy][self.x + dx] = '0'
        for row in grid:
            print(' '.join(row))
        print()


def main():
    w, h = map(int, input().split())
    Tetris(w, h).run()


if __name__ == '__main__':
    main()

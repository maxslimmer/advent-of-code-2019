"doc string "

from collections import defaultdict
from itertools import groupby
from day11.script import Computer

TILE_MAP = {
    0: " ",
    1: "#",
    2: "@",
    3: "=",
    4: "*",
}

def print_screen(screen):
    pixels = sorted(sorted([(x, y) for x, y in screen], key=lambda p: p[0]), key=lambda p: p[1])
    for k, g in groupby(pixels, lambda p: p[1]):
        print("".join([TILE_MAP[screen[p]] for p in g]))

def main():

    with open("input.txt", "r") as input_file:
        input_text = input_file.read().strip()

    program = [int(v) for v in input_text.split(",")]
    program[0] = 2

    joystick = Joystick([])
    joystick.center()
    computer = Computer(program, joystick)

    screen = defaultdict(int)
    block_count = None
    score = 0
    paddle_x = None

    while True:
        try:

            x, y, tile = next(computer), next(computer), next(computer)
        except StopIteration:
            print(f"score: {score}")
            break
        if x == -1 and y == 0:
            score = tile
            continue
        if tile == 3:
            paddle_x = x
        if tile == 4 and paddle_x is not None:
            if x < paddle_x:
                joystick.left()
            elif x > paddle_x:
                joystick.right()
            else:
                joystick.center()

        screen[(x, y)] = tile
        if block_count is None and len(screen) % (45 * 26) == 0:
            block_count = list(screen.values()).count(2)
            print(f"block count: {block_count}")

class Joystick(list):
    def pop(self, *args):
        return self.direction
    def center(self):
        self.direction = 0
    def left(self):
        self.direction = -1
    def right(self):
        self.direction = 1

if __name__ == "__main__":
    main()

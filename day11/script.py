from collections import defaultdict

    # A robot that
    # - tracks it's orientation and position,
    # - has a hull structure that reads and writes the color of a panel at a given location
    # - has a "camera" that reads the panel at it's current location,
    # - can write the output of it's program to the current panel as a color (paint),
    # - can move to a new position relative to its orientation and location.

    # A run loop that drives the robot according to algo and computer output

def main():

    with open("input.txt", "r") as input_file:
        input_text = input_file.read().strip()
    program = [int(address) for address in input_text.split(",")]
    computer = Computer(program, [])
    robot = Robot(computer)
    robot.run()
    robot.print()

class Robot:
    FACING_STATES = ['up', 'right', 'down', 'left']
    def __init__(self, computer):
        self.hull_map = defaultdict(int)
        self.location = (0, 0)
        self.paint(1)
        self.facing = "up"
        self.computer = computer

    def rotate(self, direction):
        if direction == 0:
            step = -1
        elif direction == 1:
            step = 1
        else:
            raise ValueError(f"Invalid value [{direction}] for direction.")
        idx = self.FACING_STATES.index(self.facing)
        idx += step
        self.facing = self.FACING_STATES[idx % len(self.FACING_STATES)]

    def run(self):
        try:
            while True:
                color = self.hull_map[self.location]
                # Use the current color as input to the computer
                self.computer.inputs.append(color)
                # Use the output to paint the panel and make next move
                color = next(self.computer)
                # Paint the panel
                self.paint(color)
                direction = next(self.computer)
                self.rotate(direction)
                # Move forward in new direction
                self.move()
        except StopIteration:
            pass

    def print(self):
        panels = sorted(sorted(list(self.hull_map.keys()), key=lambda panel: panel[1]), key=lambda panel: panel[0])

        max_y = max(panels, key=lambda panel: panel[1])[1]
        min_y = min(panels, key=lambda panel: panel[1])[1]
        max_x = max(panels, key=lambda panel: panel[0])[0]
        min_x = min(panels, key=lambda panel: panel[0])[0]
        for y in range(max_y, min_y-1, -1):
            for x in range(min_x, max_x, 1):
                print("#" if self.hull_map[(x, y)] else " ", end="")
            print("")

    def move(self, distance=1):
        if self.facing == 'up':
            self.location = (self.location[0], self.location[1] + distance)
        elif self.facing == 'right':
            self.location = (self.location[0] + distance, self.location[1])
        elif self.facing == 'down':
            self.location = (self.location[0], self.location[1] - distance)
        elif self.facing == 'left':
            self.location = (self.location[0] - distance, self.location[1])

    def paint(self, color):
        self.hull_map[self.location] = color

class Computer:
    def __init__(self, program, inputs):
        self.program = program[:]
        self.inputs = inputs
        self.output_value = None
        self._debug_mode = False
        self._memory = defaultdict(int, enumerate(program))
        self._inst_pointer = 0
        self.relative_base = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.output_value = None
        while True:
            mem = self._memory

            opcode = str(mem[self._inst_pointer])
            opcode, mem_modes = int(opcode[-2:]), [int(mode) for mode in opcode[:-2]]
            mem_modes.reverse()
            if opcode == 99:
                raise StopIteration
            op = self.ops[opcode]
            input_count = op.get("inputs") or 0
            output_count = op.get("output") or 0

            fn = op["operator"]

            # make params into adjusted memory addresses
            params = []
            for address,mode in zip(range(self._inst_pointer+1,
                                   self._inst_pointer+1+input_count+output_count),
                             continue_with_zeros(mem_modes)):
                params.append(self.get_value(address, mode=mode))


            self._inst_pointer += input_count + output_count + 1
            fn(self, params)
            if self.output_value is not None:

                return self.output_value

    def get_input(self, args):

        input_ = self.inputs.pop(0)  # int(input("Type the input: ").strip())

        # push the result into memory
        self._memory[args[0]] = input_

    def jump_if_true(self, args):
        if self.get_value(args[0]) != 0:
            self._inst_pointer = self.get_value(args[1])

    def jump_if_false(self, args):
        if self.get_value(args[0]) == 0:
            self._inst_pointer = self.get_value(args[1])

    def less_than(self, args):
        self._memory[args[2]] = 1 if self.get_value(args[0]) < self.get_value(args[1]) else 0

    def equal_to(self, args):
        self._memory[args[2]] = 1 if self.get_value(args[0]) == self.get_value(args[1]) else 0

    def output(self, args):
        address_value = self.get_value(args[0])

        self.output_value = address_value

    def add(self, args):
        result = self.get_value(args[0]) + self.get_value(args[1])
        self._memory[args[2]] = result

    def mul(self, args):
        result = self.get_value(args[0]) * self.get_value(args[1])
        self._memory[args[2]] = result

    def adjust_relative_base(self, args):

        self.relative_base += self.get_value(args[0])

    def get_value(self, param, mode=0):
        if mode == 1:    # Immediate mode
            return param
        elif mode == 0:  # Positional mode
            return self._memory[param]
        elif mode == 2:  # Relative mode
            return self._memory[param] + self.relative_base
        else:
            raise ValueError(f"Invalid memory mode [{mode}]")

    ops = {
        99: {"operator": exit, },
        1: {"inputs": 2, "output": 1, "operator": add, },
        2: {"inputs": 2, "output": 1, "operator": mul, },
        3: {"output": 1, "operator": get_input, },
        4: {"inputs": 1, "operator": output, },
        5: {"inputs": 2, "operator": jump_if_true},
        6: {"inputs": 2, "operator": jump_if_false},
        7: {"inputs": 2, "operator": less_than, "output": 1, },
        8: {"inputs": 2, "operator": equal_to, "output": 1, },
        9: {"inputs": 1, "operator": adjust_relative_base, },
    }

def continue_with_zeros(i):
    i = iter(i)
    while True:
        yield next(i, 0)

if __name__ == "__main__":
    main()

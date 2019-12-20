from itertools import zip_longest


def deref(address, memory):
    try:
        return (memory[address], memory[memory[address]])

    except IndexError:
        return (memory[address], None)


class Computer:
    def __init__(self, program, inputs):
        self.program = program[:]
        self.inputs = inputs
        self.output_value = None
        self._debug_mode = False
        self._memory = self.program[:]
        self._inst_pointer = 0

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
            input_mem = mem[self._inst_pointer + 1:self._inst_pointer + 1 + input_count]

            # Get instruction parameters
            params = [self.get_value(address, mode) for address, mode in
                      (zip_longest(input_mem, mem_modes, fillvalue=0))]

            params += [mem[self._inst_pointer + input_count + output_count]] if output_count else []
            self._inst_pointer += input_count + output_count + 1
            fn(self, params)
            if self.output_value is not None:

                return self.output_value

    def get_input(self, args):

        input_ = self.inputs.pop(0)  # int(input("Type the input: ").strip())

        # push the result into memory
        self._memory[args[0]] = input_

    def jump_if_true(self, args):
        if args[0] != 0:
            self._inst_pointer = args[1]

    def jump_if_false(self, args):
        if args[0] == 0:
            self._inst_pointer = args[1]

    def less_than(self, args):
        self._memory[args[2]] = 1 if args[0] < args[1] else 0

    def equal_to(self, args):
        self._memory[args[2]] = 1 if args[0] == args[1] else 0

    def output(self, args):
        address_value = args[0]

        self.output_value = address_value
        if address_value != 0 and self._debug_mode:
            print("----Dereferenced memory----")
            for address in range(self._inst_pointer - 8, self._inst_pointer + 2):
                print(f"{address}: {str(deref(address, self._memory))}")

    def add(self, args):
        result = args[0] + args[1]
        self._memory[args[2]] = result

    def mul(self, args):
        result = args[0] * args[1]
        self._memory[args[2]] = result

    def get_value(self, param, mode=0):
        return param if mode == 1 else self._memory[param]

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
    }


def get_combo(start, end):

    combo = [None]
    size = end - start + 1
    used_in_pos = {}
    pos = 0

    while pos >= 0:
        avail = set(range(start, end + 1)).difference(combo).difference(used_in_pos.setdefault(
            pos, set()))

        try:
            value = avail.pop()

        except KeyError:
            value = None

        if value is not None:
            combo[pos] = value
            used_in_pos[pos].add(value)
            # last position
            if pos == size - 1:
                yield combo
            else:
                pos += 1
                combo.append(None)
        else:
            used_in_pos.pop(pos)
            combo = combo[:pos]
            pos -= 1


with open("input.txt", "r") as input_file:

    input_str = input_file.read().strip()
    program = [int(a) for a in input_str.split(",")]

# Part 1
signals = []
for phase_combo in get_combo(0, 4):
    signal = 0
    for phase in phase_combo:
        amp = Computer(program, [phase, signal])
        signal = next(amp)
    signals.append((signal, phase_combo))
print(f"{max(signals, key=lambda sp: sp[0])}")

signals = []
for phase_combo in get_combo(5, 9):

    amplifiers = []
    for phase in phase_combo:
        amplifiers.append(Computer(program, [phase]))

    go_thruster = False
    signal = 0
    while not go_thruster:

        for i, amplifier in enumerate(amplifiers):
            amplifier.inputs.append(signal)
            try:

                signal = next(amplifier)
            except StopIteration:
                signals.append((signal, phase_combo))
                go_thruster = True

print(f"{max(signals, key=lambda sp: sp[0])}")

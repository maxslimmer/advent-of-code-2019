from collections import defaultdict


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

def main():

    with open("input.txt", "r") as input_file:
        input_text = input_file.read().strip()

    program = [int(inst) for inst in input_text.split(",")]
    boost = Computer(program, [1])
    print(f"{list(boost)}")

    boost = Computer(program, [2])
    print(f"{list(boost)}")

if __name__ == "__main__":
    main()

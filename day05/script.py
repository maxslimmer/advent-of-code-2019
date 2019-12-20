from operator import mul, add
from itertools import zip_longest

# Get input data
with open("input.txt", "r") as input_file:
    program = [int(address) for address in input_file.read().strip().split(",")]


def get_input(*args):
    return 1 # int(input("Type the input: ").strip())

def deref(address, memory):
    try:

        return (memory[address], memory[memory[address]])

    except IndexError:
        return (memory[address], None)

def computer(memory):
    def output(arg, *rest):

        print(f"Test result: {arg}.")
        if arg != 0:
            print("----Dereferenced memory----")
            for address in range(instruction_pointer-8, instruction_pointer + 2):
                print(f"{address}: {str(deref(address, memory))}")

    instructions = {
        99: {"operator": exit, },
        1: {"in_size": 2, "operator": add, "out_size": 1, },
        2: {"in_size": 2, "operator": mul, "out_size": 1, },
        3: {"out_size": 1, "operator": get_input, },
        4: {"in_size": 1, "operator": output, },
    }

    def get_value(param, mode=0):

        if mode == 0:

            return memory[param]
        elif mode == 1:
            return param
        else:
            raise ValueError(f"{mode} is not a valid parameter mode.")

    # initialize computer
    instruction_pointer = 0

    while True:

        opcode = str(memory[instruction_pointer])
        opcode, mem_modes = int(opcode[-2:]), [int(mode) for mode in opcode[:-2]]
        mem_modes.reverse()
        if opcode == 99:
            return memory
        instruct = instructions[opcode]
        inputs_size = instruct.get("in_size") or 0
        outputs_size = instruct.get("out_size") or 0

        # Get instruction parameters
        inputs = [get_value(address, mode) for address, mode in
                  (zip_longest(memory[instruction_pointer + 1:instruction_pointer + 1 + inputs_size], mem_modes, fillvalue=0))]

        result = instruct["operator"](*inputs)

        # push the result into memory
        if outputs_size:
            memory[memory[instruction_pointer + 1 + inputs_size]] = result

        # move instruction pointer forward
        instruction_pointer += 1 + inputs_size + outputs_size


print(computer(program))

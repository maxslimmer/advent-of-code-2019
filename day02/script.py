from operator import mul, add

with open("input.txt", "r") as input_file:

    program = [int(datum) for datum in
           input_file.read()
           .split(",")]

operator_ = {
    1: add,
    2: mul,
}

def puter(program, pos=0):

    # get opcode
    opcode = program[pos]

    # process opcode
    if opcode == 99:
        return program

    operand1 = program[program[pos+1]]
    operand2 = program[program[pos+2]]
    result_pos = program[pos+3]
    result = operator_[opcode](operand1, operand2)
    program[result_pos] = result

    return puter(program, pos=pos+4)

instructions = {
    99: {"size": 1,},
    1: {"size": 4, "operator": add, },
    2: {"size": 4, "operator": mul, },
}

def iterative_puter(memory):

    # initialize computer
    instruction_pointer = 0

    while True:
        opcode = memory[instruction_pointer]
        inst_info = instructions[opcode]
        if opcode == 99:
            return memory

        # Get instruction parameters
        inst = memory[instruction_pointer:instruction_pointer+inst_info["size"] ]
        operands = [memory[address] for address in inst[1:inst_info["size"] - 1]]
        result = inst_info["operator"](*operands)

        # push the result into memory
        memory[inst[-1]] = result

        # move instruction pointer forward
        instruction_pointer += inst_info["size"]


memory = program[:]
# Restore to before fire
memory[1] = 12
memory[2] = 2

part1=puter(memory, 0)[0]
print(f"part 1: {part1}")

# second part
desired_answer = 19690720
for noun in range(0, 100):
    for verb in range(0, 100):
        memory = program[:]
        memory[1] = noun
        memory[2] = verb
        if iterative_puter(memory)[0] == desired_answer:
            part2 = 100 * noun + verb
            print(f"part2: {part2}")



with open("input.txt", "r") as input_file:

    input_ = input_file.read().strip()

start, stop = [int(i) for i in input_.split("-")]

first_part_count = 0
second_part_count = 0
for candidate in range(start, stop+1):

    candidate = str(candidate)
    candidate_set = set(candidate)

    if len(candidate_set) != len(candidate) and candidate == "".join(sorted(candidate)):
        first_part_count += 1

    # second part
    if candidate == "".join(sorted(candidate)):
        for num in candidate_set:
            if candidate.count(num) == 2:
                second_part_count += 1
                break


print(f"first part: {first_part_count}")   # 1748
print(f"second part: {second_part_count}") # 1180


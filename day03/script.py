def get_nodes_from_path(path):
    nodes = [(0, 0)]

    for vector in path:
        nodes.extend(get_nodes_from_vector(vector, nodes[-1]))

    return nodes


def get_nodes_from_vector(vector, start_node=(0, 0)):
    nodes = []
    x, y = start_node
    direction, mag = vector[0], int(vector[1:])
    for _ in range(mag):

        if direction == "R":
            x += 1
        elif direction == "L":
            x -= 1
        elif direction == "U":
            y += 1
        elif direction == "D":
            y -= 1

        nodes.append((x, y))
    return nodes


def find_intersections(wire_1, wire_2):
    wire_1, wire_2 = [set(wire) for wire in [wire_1, wire_2]]

    return wire_1.intersection(wire_2)


def get_manhattan_distance(node):
    return abs(node[0]) + abs(node[1])


def get_step_distance(node, wire):
    return wire.index(node)


with open("input.txt", "r") as input_file:
    wires = [get_nodes_from_path(line.strip().split(",")) for line in input_file]

intersections = find_intersections(*wires)
min_man_dist = min(
    get_manhattan_distance(intersection)
    for intersection in intersections
    if intersection != (0, 0)
)
mid_step_dist = min(
    get_step_distance(node, wires[0]) + get_step_distance(node, wires[1])
    for node in intersections
    if node != (0, 0)
)

print(f"smallest manhattan distance: {min_man_dist}")
print(f"smallest step distance: {mid_step_dist}")

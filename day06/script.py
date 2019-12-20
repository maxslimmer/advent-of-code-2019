with open("input.txt", "r") as input_file:
    orbits = [orbit.strip().split(")") for orbit in input_file]


graph = {orbit[1]: orbit[0] for orbit in orbits}

def get_ancestors(child, ancestors=None, stop_at=None):

    if ancestors is None:
        ancestors = []
    if stop_at is None:
        stop_at = set([])

    parent = graph.get(child)
    if parent:
        ancestors.append(parent)
        if parent in stop_at:
            return ancestors
        return get_ancestors(parent, ancestors=ancestors, stop_at=stop_at)
    else:
        return ancestors

count = 0
for orbit in orbits:

    count += len(get_ancestors(orbit[1]))

print(f"Total orbits: {count}")

# Find common ancestor
my_ancestors = get_ancestors("YOU")
san_ancestors = get_ancestors("SAN")

common_ancestors = set(my_ancestors).intersection(set(san_ancestors))
common_ancestor = min((ca for ca in common_ancestors), key=lambda a: my_ancestors.index(a) )

print(f"Common Orbit: {common_ancestor}")

dist_YOU_COM = my_ancestors.index(common_ancestor)
dist_SAN_COM = san_ancestors.index(common_ancestor)
print(f"Transfers from YOU to {common_ancestor}: {dist_YOU_COM}")
print(f"Transfers from {common_ancestor} to SAN: {dist_SAN_COM}")

print(f"Total Transfers: {dist_SAN_COM + dist_YOU_COM}")

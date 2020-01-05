from math import atan2, degrees, sqrt
from collections import defaultdict

def main():

    with open("input.txt", "r") as input_file:
        input_text = input_file.read().strip()

    asteroids = {(x, y): 0 for y, line in enumerate(input_text.splitlines()) for x, loc in enumerate(line.strip()) if loc == '#'}

    for asteroid in asteroids:
        # Find detectables
        directions = set([find_direction(a, asteroid) for a in asteroids if a != asteroid])
        asteroids[asteroid] = len(directions)

    base_asteroid = max(asteroids, key=lambda a: asteroids[a])
    print(f"Selecting asteroid {base_asteroid} for base, with {asteroids[base_asteroid]} other asteroids detectable.")

    # Fire laser from base_asteroid while rotating clockwise, starting at direction (0,-1). Count and note vaporized asteroids as we go.
    angles = defaultdict(list)
    for target in sorted([a for a in asteroids if a != base_asteroid],
                         key=lambda t: find_distance(t, base_asteroid)):
        direction = find_direction(target, base_asteroid)
        # Transform atan2 params so angles start from the y-axis and increase clockwise.
        angle = degrees(atan2(direction[0], direction[1] * -1)) % 360
        angles[angle].append(target)

    vaporized = []
    while angles:
        for angle in sorted(angles):
            vaporized.append(angles[angle].pop(0))
            if not angles[angle]:
                angles.pop(angle)

    print(f"{vaporized[199]} will be the 200th asteroid vaporized --> {vaporized[199][0]*100 + vaporized[199][1]}")

def find_distance(a, b):
    x, y = (a[0] - b[0], a[1] - b[1])
    return sqrt(x**2 + y**2)

def find_direction(a, b):
    """Return the direction of a vector as tuple (direction, magnitude)."""
    # Find common factors
    x, y = (a[0] - b[0], a[1] - b[1])
    smaller = min(abs(x), abs(y))
    if smaller == 0:
        return (x and (x // abs(x)), y and y // abs(y))
    for f in range(smaller, 0, -1):
        if x % f == 0 and y % f == 0:
            return (x // f, y // f)

if __name__ == "__main__":
    main()

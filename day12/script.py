"Doc string"
from collections import defaultdict
def main():

    with open("input.txt", "r") as input_file:
        input_text = input_file.read().strip()

    moons = [Moon(Position(**parse(line))) for number, line in enumerate(input_text.splitlines())]
    axis_period = {}
    axis_states = defaultdict(set)
    tick = 0
    while True:
        # Look for position alignment periodicity along each axis
        # inspired by/stolen from aspitel [https://github.com/aspittel/advent-of-code/blob/master/2019/dec-12/script.py]
        for axis in ("x", "y", "z"):
            if axis_period.get(axis) is None:

                state = tuple([(getattr(m.position, axis), getattr(m.velocity, axis)) for m in moons])
                if state not in axis_states[axis]:
                    axis_states[axis].add(state)
                else:
                    axis_period[axis] = tick

        tick += 1
        step(moons)
        if tick == 100:
            total_energy = sum([moon.total_energy for moon in moons])
            print(f"total energy: {total_energy}")

        if len(axis_period) == 3:
            print(lcm(lcm(axis_period["x"], axis_period["y"]), axis_period["z"]))
            break

def gcd(a, b):
    if 0 in (a, b):
        return a or b
    return gcd(b, a % b)

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def step(moons):

    for moon in moons:
        for other_moon in [other for other in moons if not other is moon]:
            moon.apply_gravity(other_moon)

    for moon in moons:

        moon.apply_velocity()


def parse(txt: str):
    axes = {k.strip(): int(v) for k, v in [exp.split("=") for exp in txt.strip("<>").split(",")]}

    return axes

class Moon:
    def __init__(self, position, velocity=None):
        self.position = position
        self.velocity = velocity or Velocity()
        self.orbit_path = set()
        self.orbit_path.add((self.position.x, self.position.y, self.position.z))

    def apply_gravity(self, moon):
        for axis in ('x', 'y', 'z'):

            if getattr(self.position, axis) > getattr(moon.position, axis):
                setattr(self.velocity, axis, getattr(self.velocity, axis) - 1)
            elif getattr(self.position, axis) < getattr(moon.position, axis):
                setattr(self.velocity, axis, getattr(self.velocity, axis) + 1)

    def apply_velocity(self):
        for axis in ('x', 'y', 'z'):
            v = getattr(self.velocity, axis)
            pos = getattr(self.position, axis)
            setattr(self.position, axis, pos + v)
        if (self.position.x, self.position.y, self.position.z) in self.orbit_path:
            self.orbit_length = len(self.orbit_path)
        else:
            self.orbit_path.add((self.position.x, self.position.y, self.position.z))

    @property
    def potential_energy(self):
        return sum([abs(getattr(self.position, axis)) for axis in ('x', 'y', 'z')])

    @property
    def kinetic_energy(self):
        return sum([abs(getattr(self.velocity, axis)) for axis in ('x', 'y', 'z')])

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy

    def __repr__(self):
        return f"pos={self.position}, vel={self.velocity}"

class Position:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return f"<x={self.x}, y={self.y}, z={self.z}>"
    def __hash__(self):
        return self.__repr__()

class Velocity:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return f"<x={self.x}, y={self.y}, z={self.z}>"

if __name__ == "__main__":
    main()

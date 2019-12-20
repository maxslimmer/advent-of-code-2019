
WIDTH = 25
HEIGHT = 6

def main(input_text):

    px_per_layer = WIDTH * HEIGHT
    layers = []

    for layer in range(layers_count:=len(input_text) // px_per_layer):
        pixels = input_text[layer*px_per_layer:(layer+1)*px_per_layer]
        layers.append(pixels)

    min_zeroes = min(layers, key=lambda pixels: pixels.count('0'))
    checksum = min_zeroes.count("1") * min_zeroes.count("2")
    print(f"There are {layers_count} layers.")
    print(f"The checksum of layer with the fewest 0 digits is {checksum}")

    value_map = {"0": " ", "1": "#",}
    # part 2
    flat_image = []
    for pos in range(px_per_layer):
        for pixel in range(pos, len(input_text) + 1, px_per_layer):
            if not (value := input_text[pixel]) == '2':
                flat_image.append(value_map[value])
                break

    print("The flattened image:")

    for line in range(HEIGHT):

        print("".join(flat_image[line*WIDTH:(line+1)*WIDTH]))

if __name__ == "__main__":

    with open("input.txt", "r") as input_file:
        input_text = input_file.read().strip()

    main(input_text)

from rembg import remove


def remove_background(input_path, output_path):
    with open(input_path, "rb") as file:
        input_data = file.read()

    output = remove(input_data)

    with open(output_path, "wb") as file:
        file.write(output)
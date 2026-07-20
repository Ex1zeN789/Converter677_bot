from PIL import Image


def convert_image(input_path, output_path, output_format):

    image = Image.open(input_path)

    if output_format == "JPEG":
        image = image.convert("RGB")

    image.save(output_path, output_format)
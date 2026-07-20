import easyocr

reader = easyocr.Reader(["ru", "en"])


def recognize_text(image_path):

    result = reader.readtext(image_path)

    text = "\n".join(
        item[1] for item in result
    )

    return text
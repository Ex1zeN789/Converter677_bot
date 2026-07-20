import ffmpeg


def convert_audio(input_path, output_path):

    (
        ffmpeg
        .input(input_path)
        .output(output_path)
        .overwrite_output()
        .run(quiet=True)
    )
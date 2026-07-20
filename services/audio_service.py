import ffmpeg


def convert_audio(input_path, output_path):
    try:
        (
            ffmpeg
            .input(input_path)
            .output(output_path)
            .overwrite_output()
            .run()
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode() if e.stderr else e)
        raise
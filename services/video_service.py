import ffmpeg


def video_to_mp3(input_path, output_path):
    (
        ffmpeg
        .input(input_path)
        .output(
            output_path,
            acodec="libmp3lame",
            q=2
        )
        .overwrite_output()
        .run(quiet=True)
    )


def video_to_gif(input_path, output_path):
    (
        ffmpeg
        .input(input_path)
        .output(
            output_path,
            vf="fps=12,scale=480:-1:flags=lanczos"
        )
        .overwrite_output()
        .run(quiet=True)
    )
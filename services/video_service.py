import ffmpeg


def video_to_mp3(input_path, output_path):
    try:
        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                acodec="libmp3lame",
                audio_bitrate="192k"
            )
            .overwrite_output()
            .run()
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode() if e.stderr else e)
        raise


def video_to_gif(input_path, output_path):
    try:
        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                vf="fps=12,scale=480:-1:flags=lanczos"
            )
            .overwrite_output()
            .run()
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode() if e.stderr else e)
        raise
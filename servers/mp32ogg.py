import subprocess

def mp3toogg(input_file, output_file, quality):
    command = ["ffmpeg", "-y", "-loglevel", "error", "-i", input_file, "-c:a", "libvorbis", "-q:a", quality, "-b:a", "16k", output_file]
    subprocess.run(command, check=True)
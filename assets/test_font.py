import subprocess
import os

base = r"C:\Users\Dao\Downloads\military_shorts\assets"
cmd = [
    "ffmpeg", "-y",
    "-f", "lavfi", "-i", "color=c=black:s=1080x1920:d=1",
    "-vf", "subtitles=filename='test_font.ass':fontsdir='fonts'",
    "-vframes", "1",
    os.path.join(base, "test_font_render.jpg")
]
subprocess.run(cmd, cwd=base, check=True)
print("Rendered test ASS frame successfully!")

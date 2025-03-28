import os
import tempfile
import glob
from datetime import datetime
from tzlocal import get_localzone

REC_FOLDER = tempfile.gettempdir() + "\\rec"
OUT_FOLDER = os.getenv('UserProfile') + "\\Desktop\\ContentWarning"
FFMPEG = "ffmpeg -hide_banner -loglevel error"

# Concatenates the videos in list_file.txt and outputs to out_file
def ffmpeg_concat(list_file, out_file):
    CMD = f"{FFMPEG} -y -f concat -safe 0 -i {list_file} -c copy {out_file}"
    os.system(CMD)

# Converts one file to another
def ffmpeg_transmux(in_file, out_file):
    os.system(f"{FFMPEG} -i {in_file} {out_file}")

# Given a directory will return a list of folders sorted by date created (oldest folders first)
def get_sorted_folders(dir):
    files = list(filter(os.path.isdir, glob.glob(dir + "\\*")))
    files.sort(key=lambda x: os.path.getmtime(x))
    return files


# Formats unix timestamp with datetime (eg: "%Y-%m-%d") in your local timezone
def unix_timestamp_to_human_readable(timestamp, format):
    local_time = datetime.fromtimestamp(timestamp, get_localzone())
    return local_time.strftime(format)

# Checks if a Tmp/rec/GUID clip was recovered and viewed or lost to all players dying
# Checks for fullRecording.webm
def is_clip_found_footage(dir):
    return not os.path.isfile(dir + "\\fullRecording.webm")

# For every folder in content warning's rec/ directory
for recording_dir in get_sorted_folders(REC_FOLDER):
    # Get some information
    recording_guid = recording_dir.split("\\")[-1]
    recording_is_found_footage = is_clip_found_footage(recording_dir)
    recording_created_time = os.path.getmtime(recording_dir)
    recording_hr_created_time = unix_timestamp_to_human_readable(recording_created_time, "%I-%M-%S-%p")
    print(f"Recovering {recording_guid}... (is_found_footage: {recording_is_found_footage} & time: {recording_hr_created_time})")

    # Get every individual clip for this recording in the correct order
    clips = get_sorted_folders(recording_dir)

    # Create and write a list file for ffmpeg to concat
    list_file = ""
    for clip_dir in clips:
        list_file += f"file '{clip_dir}\\output.webm'\n"
    with open("tmp.txt", "w") as f:
        f.write(list_file)

    # Setup output location
    out_folder = OUT_FOLDER + f"\\{unix_timestamp_to_human_readable(recording_created_time, r"%Y-%m-%d")}"
    out_file_name = f"{"unseen" if recording_is_found_footage else "seen"}_{recording_hr_created_time}__{recording_guid}.mp4"
    os.makedirs(out_folder, exist_ok=True)

    # Concat the clips and then convert to mp4 (and move to output directory)
    ffmpeg_concat("tmp.txt", "tmp.webm")
    ffmpeg_transmux("tmp.webm", out_folder + "\\" + out_file_name)

# Clean up temporary files
os.remove("tmp.txt")
os.remove("tmp.webm")

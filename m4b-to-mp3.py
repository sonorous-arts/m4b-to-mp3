"""
m4b to mp3
A little script which converts chapterized m4b files to separate mp3 files using ffmpeg

Author: Sonorous Arts
License: MIT
https://github.com/sonorous-arts/m4b-to-mp3
"""
from traceback import print_exc
import json
from subprocess import Popen, PIPE, STDOUT
import os
import sys

def run_cmd(cmd):
	p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
	return p.stdout.read().decode()

def get_chapters(file):
	chapters = run_cmd(["ffprobe", "-i", file, "-print_format", "json", "-show_chapters", "-hide_banner", "-loglevel", "panic"])
	try:
		chapters = json.loads(chapters)
		return chapters["chapters"]
	except Exception:
		print_exc()
		return None

def split_chapters(input_file, bitrate=96, output_dir="output"):
	chapters = get_chapters(input_file)
	if chapters:
		filename = os.path.basename(os.path.splitext(input_file)[0])
		extention = os.path.splitext(input_file)[1]
		if not os.path.exists(output_dir+"/"+filename):
			os.makedirs(output_dir+"/"+filename)
		for chapter in chapters:
			print("Splitting", chapter["tags"]["title"])
			output = run_cmd(["ffmpeg", "-y", "-i", input_file, "-ss", chapter["start_time"], "-to", chapter["end_time"], "-c:a", "mp3", "-b:a", str(bitrate)+"k", "-hide_banner", "-loglevel", "error", output_dir+"/"+filename+"/"+chapter["tags"]["title"]+".mp3"])
			if output: # Means we've encountered an error
				break
		print("Done")
	else:
		return


if __name__ == "__main__":
	if len(sys.argv) == 1 or sys.argv[1] == "--help":
		print("Usage:\n[filename] [bitrate] [output directory]\n - Bitrate defaults to 96KBPS if omitted\n - Output directory defaults to \"output\" if omitted\n - The default behaviour will replace the newly converted files if they exist")
	if len(sys.argv) == 2:
		split_chapters(sys.argv[1])
	elif len(sys.argv) == 3:
		split_chapters(sys.argv[1], sys.argv[2])
	elif len(sys.argv) == 4:
		split_chapters(sys.argv[1], sys.argv[2], sys.argv[3])
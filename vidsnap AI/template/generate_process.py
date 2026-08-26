1 # This file looks for  new folders inside user uploads and convert them to reel if they not converted
print("SCRIPT CHALU HUA KYA???")
import os
import time
import subprocess
from text_to_audio import text_to_speech_file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_PATH = os.path.join(SCRIPT_DIR, "user_uploads")
def text_to_audio(folder):
    print("TTA - ", folder)
    with open(f"user_uploads/{folder}/desc.txt") as f:
        text = f.read()
        print(text, folder)
    text_to_speech_file(text, folder)

def create_reel(folder):
    command = f'''ffmpeg -f concat -safe 0 -i user_uploads/f8b7cbae-871e-11f1-9ecf-ec91619abb0c/input.txt -i user_uploads/f8b7cbae-871e-11f1-9ecf-ec91619abb0c/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/reel.mp4'''
    subprocess.run(command, shell=True, check=True)
    print("CR - ", folder)

if __name__ == "__main__":
    while True:
        print("Processing queue...")
        if not os.path.exists("done.txt"):
          open("done.txt", "w").close()


        with open("done.txt", "r") as f:
          done_folder = [line.strip() for line in f.readlines()]
          print("Done.txt se padha:", done_folder)

          print("Uploads path:", UPLOADS_PATH)
          folders = os.listdir(UPLOADS_PATH)
          print(folders, done_folder)
        for f in folders:
           if not os.path.isdir(os.path.join("UPLOADS_PATH", f)):
             continue
        if f not in done_folder:
           print("PROCESS KAR RAHA", f)
           desc_path = os.path.join(UPLOADS_PATH, f, "desc.txt")
           if not os.path.exists(desc_path):
              print(f"SKIP: {f} me desc.txt nhi mila")
              continue
           text_to_audio(f) # Generate the audio.mp3 from desc.txt
           create_reel(f) # convert the images and audio.mp3 inside the folder to a reel

           with open("done.txt", "a") as file:
               file.write(f + "\n")


        time.sleep(5)
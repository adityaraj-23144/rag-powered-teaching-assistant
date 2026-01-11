import os
import subprocess

files = os.listdir("videos")
print(files)
for file in files:
    lecture_number= file.split("_")[0]
    file_name=file.split("_")[1].split(".")[0]
    print(lecture_number,file_name)
    subprocess.run(["ffmpeg", "-i", f"videos/{file}", f"audios/{lecture_number}_{file_name}.mp3"])
    



@echo off
set hash="42ba21b0-6a9b-4cae-a5ee-4b58f175a45e"
cd "C:\Users\creare\Desktop\save\%hash%"
del mylist.txt
for /d %%F in (*) do echo file './%%F/output.webm' >> mylist.txt
ffmpeg -y -f concat -safe 0 -i mylist.txt -c copy "%hash%.webm"
del mylist.txt

@REM Optionally convert the webm to mp4
@REM ffmpeg -y -i "%hash%.webm" "%hash%.mp4"
@REM del "%hash%.webm"
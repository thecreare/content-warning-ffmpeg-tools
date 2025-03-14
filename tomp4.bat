cd "C:\Users\creare\Desktop\ContentWarning\2025-13-3"
set location=".\mp4ized"
mkdir %location%
for /f "tokens=*" %%F in ('dir /b *.*') do ffmpeg -y -i "%%F" -acodec mp3 "%location%\%%F.mp4"

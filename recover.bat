@echo off

@REM Hash of clip to concatenate
set hash="42ba21b0-6a9b-4cae-a5ee-4b58f175a45e"

@REM Get date in YYYY-MM-DD format
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "datestamp=%YYYY%-%MM%-%DD%"

@REM Output location of clip
set out_dir="%UserProfile%\Desktop\ContentWarning\%datestamp%"
mkdir %out_dir%
set out_file="%out_dir%\%hash%"

@REM Enter folder for this group of clips
cd "%LocalAppData%\rec\%hash%"

@REM Remove list of webms from previous runs of this script
del mylist.txt

@REM Take every folder and add ./folder/output.webm to the text file
for /d %%F in (*) do echo file './%%F/output.webm' >> mylist.txt

@REM Use ffmpeg to concat the videos from the list
ffmpeg -y -f concat -safe 0 -i mylist.txt -c copy "%out_file%.webm"

@REM Clean up
del mylist.txt

@REM Optionally convert the webm to mp4
@REM ffmpeg -y -i "%out_file%.webm" "%out_file%.mp4"
@REM del "%out_file%.webm"
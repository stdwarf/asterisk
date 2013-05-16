#!/bin/sh
echo "Create MOH from MP3"
mohdir="/var/spool/asterisk/moh"
cd $mohdir;
for i in *.mp3; do
wav=$(basename "$file".mp3).wav;
moh=$(ready_"$wav")
lame --decode "$file" "wav";
sox "$wav" -r 8000 -c 1 -s "$moh"
chmod 444 "$moh"; 
#mv "$moh" /var/spool/asterisk/sounds; 
#rm -f "$file"; 
echo "READY"
done

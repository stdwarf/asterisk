#!/bin/bash 
recorddir="${1:-/var/spool/asterisk/monitor}" 
cd $recorddir; 
for file in *.wav; do 
mp3=$(basename "$file" .wav).mp3; 
nice lame -b 16 -m m -q 9-resample "$file" "$mp3"; 
#touch --reference "$file" "$mp3"; 
chown asterisk.asterisk "$mp3"; 
chmod 444 "$mp3"; 
mv "$mp3" /var/www/html/monitor; 
rm -f "$file"; 
done

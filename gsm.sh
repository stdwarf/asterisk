#!/bin/bash
for x in {0..2}{0..9}
 do
  asterisk -rx "polygator show channel gsm chan_$x" | grep -e '"chan_' -e ICCID -e operator | tr '\n' ' '| awk -F "  --" '{print $1 $2 $3}' | awk '{print $2,$5,$8}'
done

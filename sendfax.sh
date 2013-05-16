#!/bin/sh
faxfrom=$1;
recipient=$2;
tifffilename=$3;
dirnm=`dirname $tifffilename`;
filebasename=`basename -s .tiff $tifffilename`;
filename=$filebasename".pdf";
fullfilename=$dirnm/$filename;

echo $fullfilename
echo $tifffilename
/usr/local/bin/tiff2pdf -o $fullfilename $tifffilename


sendmail "$recipient"<<!
To: $recipient
From: "FaxServer <username@domain>"
Sender: "FaxServer <username@domain>"
Subject: "Fax received from: $faxfrom"
MIME-Version: 1.0
Content-Type: multipart/mixed\;
 boundary="_=_swift_v4_1234567_=_"

--_=_swift_v4_1234567_=_
Content-Type: application/pdf\; name="$filename"
Content-Description: FAX Document (PDF)
Content-Disposition: attachment\; filename="$filename"
Content-Transfer-Encoding: base64

`/usr/bin/b64encode $fullfilename $filename | grep -v 'begin-base64'`
!


echo ok

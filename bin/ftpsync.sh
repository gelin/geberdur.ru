#!/bin/sh

FTP_HOST="geberdur.ru"

CRED_FILE=$(dirname "$0")/../.credentials
if [ -f "$CRED_FILE" ]
then
    . "$CRED_FILE"
fi

LCD="build"
RCD="public_html"
#DELETE="--delete"
lftp -c "set ftp:list-options -a;
open --user '$FTP_USER' --password '$FTP_PASSWORD' '$FTP_HOST';
lcd $LCD;
cd $RCD;
mirror --reverse $DELETE --verbose;"

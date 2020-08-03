echo off
cls

call activate
call conda activate alana
rasa run --enable-api --log-file server-log.log
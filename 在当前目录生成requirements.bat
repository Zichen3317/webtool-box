@echo off    
start cmd /k "cd /d %~dp0&&pipreqs . --encoding=utf8 --force "


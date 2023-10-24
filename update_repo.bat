@REM  batch file that adds all and commits changes to git repository
@REM check if user has entered a commit message
@echo off
if "%1"=="" goto error

echo "commit message => %1"
git add --all
git commit -m "%1"
git push origin master
goto success

:error
echo NO COMMIT MESSAGE

:success

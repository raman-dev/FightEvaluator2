@REM  batch file that adds all and commits changes to git repository
git add --all
git commit -m "%1"
git push origin master


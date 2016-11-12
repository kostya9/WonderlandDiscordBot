robocopy .\ ..\deploy_heroku_wonderland\ settings.json main.py ps_db.py check_summoner.py 
cd ..\deploy_heroku_wonderland\
git add .
git commit -m "deploy_update"
git push heroku master
cd ..\WonderlandDiscordBot
heroku restart -a super-leg-discord-bot

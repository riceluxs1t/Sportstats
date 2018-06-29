# ELO based Soccer prediction

## Setup

1. Install Python 3.5+
2. run "pip install pipenv"
3. run "pipenv install".
(if you are not familiar with pipenv, 
more on information https://robots.thoughtbot.com/how-to-manage-your-python-projects-with-pipenv)


## Reference Paper

https://arxiv.org/pdf/1806.01930.pdf

## Training Data Source

http://eloratings.net/

## Real Time 2018 World Cup Match Data

http://worldcup.sfg.io/

## Deployment

http://ec2-13-125-192-62.ap-northeast-2.compute.amazonaws.com/

## Loaing Match Data into DB

python manage.py load_data [year1] [year2] [year3] ... [yearN]

e.g. python manage.py load_manual 2018 2017

## Make Prediction

http://ec2-13-125-192-62.ap-northeast-2.compute.amazonaws.com/prediction/?home_team=[home_team]&away_team=[away_team]

e.g.

http://ec2-13-125-192-62.ap-northeast-2.compute.amazonaws.com/prediction/?home_team=Japan&away_team=Belgium

Highly recommend you get a Chrome JSON Formatter for human friendly rendering (https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa?hl=ko) 

## React Front with Ant-Design
http://v1k45.com/blog/modern-django-part-1-setting-up-django-and-react/
https://ant.design/docs/react/introduce

## Run Nginx and Gunicorn

gunicorn elosoccer.wsgi:application --bind=127.0.0.1:8001 &

/etc/init.d/nginx restart # (ubuntu)

/var/log/nginx
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

https://obscure-savannah-41248.herokuapp.com/

## Loaing Match Data into DB

python manage.py load_manual [year1] [year2] [year3] ... [yearN]

e.g. python manage.py load_manual 2018 2017

## Make Prediction

https://obscure-savannah-41248.herokuapp.com/prediction/?home_team=[home_team_name]&away_team=[away_team_name]

e.g.

https://obscure-savannah-41248.herokuapp.com/prediction/?home_team=Iran&away_team=Spain

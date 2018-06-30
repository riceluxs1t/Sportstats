from prediction import independent_poisson_model,tournament

def get_current_model():
    return independent_poisson_model.IndependentPoissonModel()

def get_tournament():
    return tournament.Tournament()

def make_prediction_output_currnet_model(model_outcome):
    return independent_poisson_model.make_prediction_output(model_outcome)

def make_tournament_output(tournament_outcome):
    return tournament.make_prediction_output(tournament_outcome)

def predict(home_team, away_team):
    model = get_current_model()
    model_prediction_outcome = model.predict(home_team, away_team)
    return make_prediction_output_currnet_model(model_prediction_outcome)

def predict_winner_worldcup():
    tournament = get_tournament()
    # return tournament
    tournament_winner = tournament.get_winner_probability()
    return make_tournament_output(tournament_winner)
from prediction import independent_poisson_model,tournament

def get_current_model():
    return independent_poisson_model.IndependentPoissonModel()

def get_current_tournament(model):
    return tournament.Tournament(model)

def make_prediction_output_currnet_model(model_outcome):
    return independent_poisson_model.make_prediction_output(model_outcome)

def make_prediction_output_current_tournament(tournament_winner_prediction):
    return tournament.make_tournament_prediction_output(tournament_winner_prediction)

def predict(home_team, away_team):
    model = get_current_model()
    model_prediction_outcome = model.predict(home_team, away_team)
    return make_prediction_output_currnet_model(model_prediction_outcome)

def predict_winner_worldcup():
    model = get_current_model()
    tournament = get_current_tournament(model)

    # return tournament 
    tournament_winner_prediction = tournament.get_winner_probability()
    return make_prediction_output_current_tournament(tournament_winner_prediction)
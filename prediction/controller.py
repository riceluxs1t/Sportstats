from prediction import independent_poisson_model,tournament, tournament_prediction



def get_current_single_match_model():
    return independent_poisson_model.IndependentPoissonModel()

def get_current_tournament(round_16):
    return tournament.Tournament(round_16)

def get_current_tournament_model():
    model = get_current_single_match_model()
    return tournament.TournamentPredictionModel(model)


def make_prediction_output_current_single_match_model(model_outcome):
    return independent_poisson_model.make_prediction_output(model_outcome)

def make_prediction_output_current_tournament(model,tournament):
    return tournament_prediction.TournamentPredictionModel(model,tournament).predict()



def predict(home_team, away_team):
    model = get_current_single_match_model()
    model_prediction_outcome = model.predict(home_team, away_team)
    return make_prediction_output_current_single_match_model(model_prediction_outcome)

def predict_winner_worldcup():
    round_16 = [
        "uruguay","portugal",
        "france","argentina",   
        "brazil","mexico",
        "belgium","japan",
        "spain","russia",
        "croatia","denmark",
        "sweden","switzerland",
        "colombia","england"]
    model = get_current_model()
    tournament = get_current_tournament(round_16)
    return make_prediction_output_current_tournament(model, tournament)
    
    # return tournament 
    # tournament_winner_prediction = tournament.get_winner_probability()
    # return make_prediction_output_current_tournament(tournament_winner_prediction)

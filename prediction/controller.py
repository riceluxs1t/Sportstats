from prediction import independent_poisson


def get_current_model():
    return independent_poisson.IndependentPoissonModel()


def make_prediction_output_currnet_model(model_outcome):
    return independent_poisson.make_prediction_output(model_outcome)


def predict(home_team, away_team):
    model = get_current_model()
    model_prediction_outcome = model.predict(home_team, away_team)
    return make_prediction_output_currnet_model(model_prediction_outcome)

from prediction import independent_poisson_model, bivariate_poisson


def get_current_model():
    return independent_poisson_model.IndependentPoissonModel()

def get_bivariate_model():
    return bivariate_poisson.BivariatePoissonModel()

def make_prediction_output_currnet_model(model_outcome):
    return independent_poisson_model.make_prediction_output(model_outcome)

def make_prediction_output_bivariate_model(model_outcome):
    return bivariate_poisson.make_prediction_output(model_outcome)

def predict(home_team, away_team):
        model = get_current_model()
        model_prediction_outcome = model.predict(home_team, away_team)
        return make_prediction_output_currnet_model(model_prediction_outcome)

def predict_bivariate_model(home_team,away_team):
        model = get_bivariate_model()
        model_prediction_outcome = model.predict(home_team, away_team)
        return make_prediction_output_bivariate_model(model_prediction_outcome)


    

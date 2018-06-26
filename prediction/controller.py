from prediction.independent_poisson import IndependentPoissonModel


def get_current_model():
    print("inthe controller")
    return IndependentPoissonModel()

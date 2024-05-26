def trainer_name(feature, scenario) -> str:
    return feature.name + "_" + scenario.name


def model_path(feature, scenario) -> str:
    return "./models/" + feature.name + "/" + scenario.name

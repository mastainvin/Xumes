
def parse_json_with_eval(json_obj):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            json_obj[key] = parse_json_with_eval(value)
        return json_obj
    elif isinstance(json_obj, list):
        return [parse_json_with_eval(item) for item in json_obj]
    elif isinstance(json_obj, str):
        try:
            return eval(json_obj)
        except (SyntaxError, NameError, TypeError):
            # Si l'évaluation échoue, on laisse la valeur inchangée
            return json_obj
    else:
        return json_obj

def serving_to_data(serving):
    """
    Converts the form field 'serving' to the food model fields 'data_value'
    and 'data_measurement'.
    """
    data = {}
    if serving == '100g':
        data['data_value'] = 100
        data['data_measurement'] = 'g'
    elif serving == '100ml':
        data['data_value'] = 100
        data['data_measurement'] = 'ml'
    else:
        data['data_value'] = 1
        data['data_measurement'] = 'srv'
    return data


def data_to_serving(data):
    """
    Coverts the food model fields 'data_value' and 'data_measurement' to the
    form field 'serving'.
    """
    serving = None
    if data == 'g':
        serving = '100g'
    elif data == 'ml':
        serving = '100ml'
    else:
        serving = '1 Serving'
    return serving
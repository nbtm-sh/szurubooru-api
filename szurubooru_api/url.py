def get_opts(**kwargs):
    # TODO: Escape strings
    output = []
    for key in kwargs.keys():
        output.append("=".join(key, str(kwargs[key])))
    re = "&".join(output)
    return "?" + re

from collections import defaultdict

RATINGS = {'': 'n/a',
           '½': 0.5,
           '★': 1,
           '★½': 1.5,
           '★★': 2,
           '★★½': 2.5,
           '★★★': 3,
           '★★★½': 3.5,
           '★★★★': 4,
           '★★★★½': 4.5,
           '★★★★★': 5}

def get_rating(stars):
    if stars is None:
        return 'n/a'
    else:
        return RATINGS[stars.strip()]

def generate_args_string(values):
    args_str = ",".join("(%s)" % ", ".join("%s" for _ in range(len(t))) for t in values)
    return args_str

def collapse_data(data):
    collapsed_data = defaultdict(list)
    for entry in data:
        key = entry[0]
        value = entry[1:]
        if len(value) == 1:
            collapsed_data[key].append(value[0])
        else:
            collapsed_data[key].append(value)
    result = [(key, value) for key, value in collapsed_data.items()]
    return result
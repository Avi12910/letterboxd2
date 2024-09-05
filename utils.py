
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
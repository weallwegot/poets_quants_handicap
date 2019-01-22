#!/usr/bin/env python3

# schools and their synonyms for label creation
SCHOOLS = {'Harvard': ['Harvard'],
           'Stanford': ['Stanford'],
           'Berkeley': ['Berkeley', 'Haas'],
           'Wharton': ['Wharton'],
           'Tuck': ['Tuck', 'Dartmouth'],
           'Kellogg': ['Kellogg', 'Northwestern'],
           'Cornell': ['Cornell'],
           'Duke': ['Duke'],
           'Booth': ['Booth', 'Chicago'],
           'Columbia': ['Columbia'],
           'Michigan': ['Michigan', 'Ross'],
           'NYU': ['NYU', 'New York University'],
           'UCLA': ['UCLA', 'Anderson'],
           'Sloan': ['Sloan', 'MIT'],
           'Yale': ['Yale'],
           'INSEAD': ['INSEAD']
           }

# create another dictionary with the keys and values reversed
SCHOOLS_REVERSED = {}
for k, v in SCHOOLS.items():
    for name in v:
        SCHOOLS_REVERSED[name] = k

TARGET_LABELS = list(set(SCHOOLS_REVERSED.values()))

# setup the random state for stochastic models
RANDOM_STATE = 545510477

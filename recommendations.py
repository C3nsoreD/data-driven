# c3nsored 
from math import sqrt

# A dictionary of movie critics and their ratings of a small
# set of movies



critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


# Returns a distance based similarity score for x and y
# Score is 0-1 1 being the highest
def sim_distance(prefs, x, y):
    # Get the list of shared_items
    si = {}
    for item in prefs[x]:
        if item in prefs[y]:
            si[item] = 1

    # if no ratings are common then return 0
    if len(si) == 0: return 0

    # Add up the squares of all the differences 
    sum_of_squares = sum([pow(prefs[x][item]-prefs[y][item], 2) 
                        for item in prefs[x] if item in prefs[y]])

    return 1/(1 + sum_of_squares)

# Returns the Pearson correlation coefficient for x and y
def sim_pearson(prefs, x, y):
    # get the list of mutually rated items
    si = {}
    for item in prefs[x]:
        if item in prefs[y]:
            si[item] = 1

    # find the number of elements
    n = len(si)

    # if no ratings are common to x and y return 0
    if n==0: return 0

    # Add up all the preferences
    sum1 = sum([prefs[x][it] for it in si])
    sum2 = sum([prefs[y][it] for it in si])

    # sum up the squares 
    sum1_Sq = sum([pow(prefs[x][it], 2) for it in si])
    sum2_Sq = sum([pow(prefs[y][it], 2) for it in si])

    # Sum up the products
    p_Sum = sum([prefs[x][it]*prefs[y][it] for it in si])

    # Calculate the pearson score
    num = p_Sum-(sum1*sum2/n)
    den = sqrt((sum1_Sq - pow(sum1, 2) / n) * (sum2_Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    
    r = num/den
    return r

# Returns the best matches for person from the prefs dictionary
# Number of results and similarity function are optional params.

def top_matches(prefs, person, n=5, similarity=sim_pearson):
    scores = [
        (similarity(prefs, person, other), other) for other in prefs if other != person
    ]
    scores.sort()
    scores.reverse()
    # Return a 5 top matches
    return scores[0:n]

# Get recommendations for a person by using a weightedd average
# of every other user's rankings.
def get_recommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    sim_sums = {}

    for other in prefs:
        # dont compare me to myself
        if other == person: 
            continue

        sim = similarity(prefs, person, other)

        if sim <= 0:
            continue

        for item in prefs[other]:
            # only score moovies I havent seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # similarity * score
                totals.setdefault(item, 0) 
                totals[item] += prefs[other][item] * sim
                # sum of similarities
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim
        
        # create the normalized list
        rankings = [(total/sim_sums[item], item) for item, total in totals.items()]

        # return the sorted list 
        rankings.sort()
        rankings.reverse()
        return rankings

def transform_prefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})

            # flip item and person
            result[item][person] = prefs[person][item]
    
    return result


if __name__ == "__main__":
    # Running tests here.
    # Two methods used for determing the similarities of individuals based on there ratings on movies
    # Eucleadin and Pearson.
    # print(top_matches(critics, 'Lisa Rose', n=3))
    # Transform the data and 
    movies = transform_prefs(critics)
    print(top_matches(movies, 'Superman Returns'))
    print(get_recommendations(movies, 'Just My Luck'))
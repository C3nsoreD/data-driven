from recommendations import *
import json

def calculateSimilarItems(prefs, n=10):
    # Create a dictionary of items showing which other items they 
    # are most similar to.
    result = {}

    # Invert the preference matrix to be item-centric
    itemsPrefs = transform_prefs(prefs)
    c = 0
    for item in itemsPrefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0:
            print(f'{c} / {len(itemPrefs)}')
        
        # Find the  most similar items to this one
        scores = top_matches(
            itemsPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    
    return result

def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}

    # loop over items rated by this user
    for (item, rating) in userRatings.items():
        # Loop over items similiar to this one
        for (similarity, item2) in itemMatch[item]:

            # ignore if this uer has already rated this item
            if item2 in userRatings:
                continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity*rating
            
            #sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    # divide each total score by total weight to get an average
    rankings = [
        (score/totalSim[item], item) for item, score in scores.items()
    ]
    
    # return the rankings from hishes to lowest
    rankings.sort()
    rankings.reverse()
    return rankings



if __name__ == "__main__":
    result = calculateSimilarItems(critics)
    print(json.dumps(calculateSimilarItems(critics)['Superman Returns'], indent=2))
    
    # Output the results to a json file.
    with open('item_similarities.json', 'w') as f:
        json.dump(result, f)

    # [print(k, v, ) for k, v in calculateSimilarItems(critics).items()]
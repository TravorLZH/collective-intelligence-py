#!/usr/bin/python3

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

from math import sqrt

# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
	# Get the list of shared_items
	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:	si[item]=1
	# If they have no rating in common, return 0
	if len(si)==0:	return 0
	
	# Add up the squares of all the differences
	sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
		for item in prefs[person1] if item in prefs[person2]])
	return 1/(1+sum_of_squares)

# Returns the best matches for person from the prefs dictionary
def top_matches(prefs,person,n=5,similarity=sim_distance):
	scores=[(similarity(pref,person,other),other) for other in prefs if other!=person]
	scores.sort()
	scores.reverse()
	return scores[0:n]

def get_recommendations(prefs,person,similarity=sim_distance):
	totals={}	# Total recommendations
	simSums={}	# Total similarities
	for other in prefs:
		# Do not compare me to myself
		if other==person: continue
		sim=similarity(prefs,person,other)
		# Ignore scores <= 0
		if sim<=0: continue
		for item in prefs[other]:
			if item not in prefs[person] or prefs[person][item]==0:
				totals.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim
				simSums.setdefault(item,0)
				simSums[item]+=sim
	rankings=[(total/simSums[item],item) for item,total in totals.items()]
	rankings.sort()
	rankings.reverse()
	return rankings

def transform_prefs(prefs):
	result={}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item,{})
			result[item][person]=prefs[person][item]
	return result

def calculate_similar_items(prefs,n=10):
	result={}
	itemPrefs=transform_prefs(prefs)
	c=0
	for item in itemPrefs:
		c+=1
		if c%100==0:	print("%d / %d" % (c,len(itemPrefs)))
		scores=top_matches(itemsPrefs,item,n=n,similarity=sim_distance)
		result[item]=scores
	return result

def get_recommended_items(prefs,itemMatch,user):
	userRatings=prefs[user]
	scores={}
	totalSim={}
	# Loop over items rated by the user
	for (item,rating) in userRatings.items():
		for (similarity,item2) in itemMatch[item]:
			if item2 in userRatings: continue
			scores.setdefault(item2,0)
			scores[item2]+=similarity*rating
			totalSim[item2]+=similarity
	rankings=[(score/totalSim[item],item) for item,score in scores.items()]
	rankings.sort()
	rankings.reverse()
	return rankings

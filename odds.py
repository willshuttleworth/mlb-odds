import requests

response = requests.get('https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/?apiKey=0cab240dc523348350b8fb9625db06c0&regions=us&markets=h2h,spreads&oddsFormat=decimal')

response = response.json()

# gonna be a bunch of loops lol
# first is gonna be iterating through all matchups
# next is iterating through each book
# nvm only nested for loops so not horrible

# iterating over all matchups
for i in range(len(response)):
    favorite = ''
    underdog = ''
    fav_odds = 0
    dog_odds = 0
    first_team = response[i]['bookmakers'][0]['markets'][0]['outcomes'][0]['name']
    second_team = response[i]['bookmakers'][0]['markets'][0]['outcomes'][1]['name']
    first_sum = 0 
    second_sum = 0

    # iterate over specific matchup to find consensus ml and favorite
    for j in range(len(response[i]['bookmakers'])):
        first_sum += response[i]['bookmakers'][j]['markets'][0]['outcomes'][0]['price']
        second_sum += response[i]['bookmakers'][j]['markets'][0]['outcomes'][1]['price']
    first_odds = first_sum / len(response[i]['bookmakers'])
    second_odds = second_sum / len(response[i]['bookmakers'])
    if first_odds < second_odds:
        favorite = first_team
        fav_odds = first_odds
        underdog = second_team
        dog_odds = second_odds
    else:
        favorite = second_team
        fav_odds = second_odds
        underdog = first_team
        dog_odds = first_odds
    #print(favorite + ":", round(fav_odds, 2), underdog + ":", round(dog_odds, 2))

    # iterate over same matchup to find consensus spread odds
    fav_sum = 0
    num_books = 0
    for j in range(len(response[i]['bookmakers'])):
        if len(response[i]['bookmakers'][j]['markets']) > 1 and response[i]['bookmakers'][j]['markets'][1]['key'] == 'spreads':
            if response[i]['bookmakers'][j]['markets'][1]['outcomes'][0]['name'] == favorite and response[i]['bookmakers'][j]['markets'][1]['outcomes'][0]['point'] == -1.5:
                fav_sum += response[i]['bookmakers'][j]['markets'][1]['outcomes'][0]['price']
                num_books += 1
            elif response[i]['bookmakers'][j]['markets'][1]['outcomes'][1]['name'] == favorite and response[i]['bookmakers'][j]['markets'][1]['outcomes'][1]['point'] == -1.5:
                fav_sum += response[i]['bookmakers'][j]['markets'][1]['outcomes'][1]['price']
                num_books += 1
    if num_books == 0:
	    print("odds not available for", first_team, "vs", second_team)
    else:
        spread_consensus = fav_sum / num_books
        ml_implied = (1 / fav_odds) * 100
        spread_implied = (1 / spread_consensus) * 100
        diff = ml_implied - spread_implied
        diff = round(diff, 2)
        print(favorite + ":", str(diff) + "%")
# issues:
# so many variables, not readable
# for some games, -1.5 favorite is different than ML favorite. has something to do with home/away hitting in top/bottom of inning
# cannot control dates for odds, getting matchups that have odds from the next day (need new api most likely lol)

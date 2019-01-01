# python3

import json
import random
import subprocess
import string


BET_COST = 7


def run():
    # read db
    with open('db.json', 'r') as f:
        data = json.load(f)
    
    # read in template file
    with open('template.js', 'r') as f:
        template = string.Template(f.read())
    
    # get winning numbers
    numbers = set(random.sample(range(1, 50), 6))
    print('\t', numbers)
        
    # iterate over players
    mapping = {
        'history': json.dumps(data['history']),
        'cost': BET_COST
    }
    for player in data["players"]:
        player["founds"] += 100
        # TODO: check if file processing is needed
        # read player submitted fnction
        with open('submitted/' + player['file'], 'r') as f:
            player_func = f.read()
        
    	# prepare data for function
        mapping['founds'] = player['founds']
        output = player_func + template.substitute(mapping)
    
        # save file to execute
        filename = 'run_ready/' + player['file'] 
        with open(filename, 'w') as f:
            f.write(output)
    
        # execute a file in js
        proc = subprocess.run(['js', filename], stdout=subprocess.PIPE, universal_newlines=True)
    
        if proc.returncode == 0:
            bets = json.loads(proc.stdout.strip())
            player['founds'] -= BET_COST - len(bets)
            for bet in bets:
                print(bet, len(numbers.intersection(bet)))
    
if __name__ == "__main__":
    run()

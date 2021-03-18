import json

def fileExists(filename):
    try:
        f = open(filename)
        f.close()
        return True
    except IOError:
        return False

def serializeJSON(fileName, players): 
    f = open(fileName, 'w') 
    json.dump(players, f) 
    f.close()

def deserializeJSON(fileName): 
    f = open(fileName, 'r') 
    players = json.load(f) 
    f.close()
    return players

def serialize(filename, players):
    f = open(filename, 'w')
    for p in players:
        f.write(f'{p},{str(players[p])}\n')
    f.close()

def deserialize(filename, players):
    f = open(filename, 'r')

    for entry in f:
        line = entry.split(',')
        name, score = line[0], int(line[1])
        players[name] = score

players = { 'Anna': 10000, 'Barney': 9000, 'Jane': 8000, 'Fred': 7000 }
serialize('highscores.txt', players)

players = { } 
deserialize('highscores.txt', players) 
print(players)
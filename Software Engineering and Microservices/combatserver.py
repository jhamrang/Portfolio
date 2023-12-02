#
#   Combat server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Fight" from gameclient, replies with a string containing 
#   a dictionary of the randomly selected enemy
#

import zmq
import random

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from gameclient
    message = socket.recv()
    print("Received request for a %s" % message)

    #  Randomly select an enemy and randomly adjust its damage and gold values
    enemies = [{'enemy': 'Bandit', 'damage': 2, 'gold': 1},
           {'enemy': 'Goblin', 'damage': 3, 'gold': 2},
           {'enemy': 'Wolf', 'damage': 4, 'gold': 3},
           {'enemy': 'Brigand', 'damage': 7, 'gold': 4},
           {'enemy': 'Dragon', 'damage': 10, 'gold': 7}]

    enemy = {}
    number = random.randint(0, len(enemies) - 1)
    enemy['enemy'] = enemies[number]['enemy']
    enemy['damage']= enemies[number]['damage'] + random.randint(-2, 2)
    enemy['gold'] = enemies[number]['gold'] + random.randint(-2, 2)

    #  Send reply back to gameclient
    socket.send_string(str(enemy))
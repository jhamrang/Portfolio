# Importing
import random
import time
import zmq
import ast

random.seed(time.time())

# Defining functions to be used later in the script
def user_input_test(user_input):
    """Tests if user input is valid or not"""
    if user_input == "fight" or user_input == "shop" or user_input[0:3] == "buy" or user_input == "leave" or user_input == "commands" or user_input == "save" or user_input == "load" or user_input == "reset":
        return True
    return False


def save(enctr, gold, hp, damage_reduction, no_shopping_ctr):
    """Saves game. Overwrites previous save"""
    with open("savefile.txt", "w") as save_file:
        out_list = [enctr, gold, hp, damage_reduction, no_shopping_ctr]
        save_file.write(str(out_list))
    "Game Saved, what would you like to do?"


def load():
    """Returns data from the save file"""
    try:
        open("savefile.txt", "r")
    except:
        print("No save data found")
        return

    with open("savefile.txt", "r") as save_file:
        load_line = save_file.read()
        load_list = load_line.split(",")
    print("Game loaded")
    enctr = int(load_list[0][1:])
    gold = int(load_list[1])
    hp = int(load_list[2])
    damage_reduction = int(load_list[3])
    no_shopping_ctr = int(load_list[4][0:len(load_list[4])-1])
    return (enctr), (gold), (hp), (damage_reduction), (no_shopping_ctr)


def reset():
    """Resets the game back to the start"""
    return (1), (0), (100), (0), (0)

# Defining variables to be used within the script
enctr = 1
gold = 0
hp = 100
damage_reduction = 0
max_num_enctr = 20
no_shopping_ctr = 0
welcome_statement = "Welcome to the game.  Your goal is to get through 20 encounters. You are on encounter "+ str(enctr) +". You have "+ str(gold) + " gold and "+str(hp) +" hp. If you go through 5 encounters in a row without going to the shop you will get 5 gold. A list of commands are as follows. "
command_list = "fight - start the current encounter and find out the outcome \n"\
               "shop - go to the shop between encounters. armor and health are purchasable for 10 and 20 gold respectively \n"\
                "buy x - buy item number x in the shop \n"\
                "leave - exit the shop without buying anything \n"\
                "commands - relist the commands \n"\
                "save - saves progress to be loaded later \n"\
                "load - loads saved progress to be loaded later \n"\
                "reset - resets back to the start of the game\n"\
                "Please enter one of the commands above "


print(welcome_statement)
print(command_list)

# looping until the user either wins the game or loses
while enctr <= max_num_enctr:
    user_input = input()
    user_input = user_input.lower()
    context = zmq.Context()

    if user_input_test(user_input) is not True:
        print("Invalid command entered. Here is a list of commands")
        print(command_list)
    else:
        if user_input == "fight":
            # Implementing my partners microservice
            # the following lines are based around my partners gameclient.py code, which was an example of how to
            # implement his microservice: https://github.com/johnc341/CS361_Assignment7
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://localhost:5555")
            socket.send_string("Fight")
            message = socket.recv_string()
            result = ast.literal_eval(message)
            enemy = result["enemy"]
            damage = result["damage"]

            # Making sure values are validated , and taking damage reduction into account  before calculating hp
            enctr_gold = result["gold"]
            if enctr_gold <= 0:
                enctr_gold =0

            damage -=  damage_reduction
            print("You encountered a " + enemy)
            if damage < 0:
                damage = 0
            hp -= damage
            if hp <= 0:
                print("You have perished on encounter number " + str(enctr) + " out of " + str(max_num_enctr) + ". Please run again")
                break
            else:
                enctr += 1
                no_shopping_ctr += 1
                gold += int(enctr_gold)
                print("The " + enemy + " did " + str(damage) + " damage to you. You now have " + str(hp) + " hp, and " + str(gold) + " gold. It is now encounter number "+ str(enctr) + " out of " + str(max_num_enctr))
                if no_shopping_ctr == 5:
                    gold += 5
                    print(
                        "You gained 5 gold for not going to the shop for 5 encounters in a row. You currently have " + str(
                            gold))
                    no_shopping_ctr = 0

        if user_input == "shop":
            shop_input = ""
            no_shopping_ctr = 0
            # user must buy an item or leave the shop to return to the other possible commands
            while shop_input != "leave":
                print("Type 'buy 1' to  buy option 1, 'buy 2' to buy option 2, type 'leave' to leave the shop when done")
                print("1. Armor/weapon Upgrade, provides 1 additional point of damage reduction, 10 gold")
                print("2. Health Kit, restores 5 points of health, 20 Gold")
                print("What would you like to do?")
                shop_input = input()
                shop_input = shop_input.lower()
                if shop_input[4] == "1":
                    if gold >=10:
                        gold = gold - 10
                        damage_reduction += 1
                        print("Thank you for your purchase. You now have " + str(damage_reduction) + " armor and " +str(hp) + " health. You have " + str(gold) + " gold.")
                    else:
                        print("Not enough gold. You have " + str(gold) + " gold. You need 10")
                elif shop_input[4] == "2":
                    if gold >= 20:
                        gold = gold - 20
                        hp += 5
                    else:
                        print("Not enough gold. You have " + str(gold) + " gold. You need 20")
                elif "leave" !=shop_input:
                    print(command_list)
                    print("Only the commands to buy ('buy 1' or 'buy 2', or leave is valid in the shop")
            print("It is now encounter number "+ str(enctr) + " out of " + str(max_num_enctr)+ ". What would you like to do?")

        if user_input == "save":
            save(enctr, gold, hp, damage_reduction, no_shopping_ctr)
            print("game saved, what would you like to do now?")

        if user_input == "load":
            enctr, gold, hp, damage_reduction, no_shopping_ctr = load()
            print("Welcome to the game.  Your goal is to get through 20 encounters. You are on encounter "+ str(enctr) +". You have "+ str(gold) + " gold and "+str(hp) +" hp, " + str(damage_reduction) + "  damage reduction, and the shopping counter is " + str(no_shopping_ctr))

        if user_input == "reset":
            enctr, gold, hp, damage_reduction, no_shopping_ctr = reset()
            print("Game reset")
            print("Welcome to the game.  Your goal is to get through 20 encounters. You are on encounter " + str(
                enctr) + ". You have " + str(gold) + " gold and " + str(hp) + " hp.")

        if user_input == "commands":
            print(command_list)

if hp>0:
    print("Congrats you beat the game!")





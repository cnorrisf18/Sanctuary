from classes import Players, Animal, Board, Feed, Workforce
import random



#mode = text/graphics

def simpleSetup():
    team = Players(1)
    sizes = ['large', 'large', 'large', 'medium', 'small']
    species = ['cow', 'pig', 'horse', 'goat', 'chicken']
    names = ['Betsy', 'Junior', 'Teddy', 'Hector', 'Cluckers']

    for i in range(0, 5):
        animal = Animal(sizes[i], names[i], species[i])
        animal.calculate_stats()
        team.total_sanctuary_animals.append(animal)
        team.boardlist[0].add_animals([animal])
        #print(f'the sanctuary has:{team.total_sanctuary_animals} and the board has:   {team.boardlist[0].ambassadors}')

    feed = Feed()
    feed.total_supply = 100
    return team, feed



def simpleRejuv(team):
    [board.reset() for board in team.boardlist]
    team.earn_money(50)

def simpleAction(team, feed):
    num_actions = team.players * 2
    for n in range(1,num_actions+1):
        poss_actions = ['upkeep', 'purchase feed', 'organize fundraiser']
        action = input(f'What action would you like to do? Type an option:{poss_actions}').lower()
        if action == 'upkeep':
            end = [board.labor(feed, False) for board in team.boardlist]
            print(f'Performed upkeep, end = {end}')
            if not any(end):
                print(f'Success. Food left:{feed.total_supply}')
            if any(end):
                print('Failed to feed everyone')
                return end
        elif action == 'purchase feed':
            neededfeed = sum([animal.feed for animal in team.total_sanctuary_animals])
            possible_feed = team.total_money//2
            neededmoney = neededfeed*2
            food_avail = feed.total_supply
            print(f'You have ${team.total_money}.')
            print(f'You can buy {possible_feed} feed with your money and you have {food_avail} available.')
            print(f'You need {neededfeed} in order to feed all of your animals.')
            amt = int(input('How much feed would you like to buy?'))
            if amt <= possible_feed:
                feed.buy_feed(amt * 2)
                team.spend_money(amt * 2)
                print(f'You bought {amt} feed. You have ${team.total_money} left.')
        elif action == 'organize fundraiser':
            d20 = random.randint(1,20)
            team.earn_money(d20)
            print(f'You earned ${d20}.')

def simpleResolution(team):
    for animal in team.total_sanctuary_animals:
        if not animal.hasbeenfed:
            print(f'You did not feed {animal.aname}! You have lost the game.')
            return True
    return False


def main():
    roundnum = 1
    team, feed = simpleSetup()
    gameended = False
    while not gameended:
        simpleRejuv(team)
        feedfail = simpleAction(team, feed)
        if feedfail:
            gameended = True
            print('Could not feed an animal, game ending')
            break
        upfail = simpleResolution(team)
        if upfail:
            gameended = True
            print('Did not feed all of the animals, game ending')
            break
        print(f'Round {roundnum} ended, moving onto next round')
        roundnum = roundnum + 1
main()
from classes import Players, Animal, Board, Workforce
import random



#mode = text/graphics

def Setup():
    num = int(input('How many players?'))
    team = Players(num)
    for player in range(0,team.players):
        team.earn_money(10)
        name = input(f'Player {player}, what is your name?')
        team.add_names(name)
        possible_animals = []
        with open('textfiles/animals','r') as afile:
            zespecies = [line.strip().split(',') for line in afile]
            possible_animals = [an[0] for an in zespecies]
        added_an_animal = False
        while not added_an_animal:
            animal = input(f'{name}, what would you like your starter animal to be? Choose from the following: {possible_animals[1:]}')
            if animal.lower() in possible_animals:
                compname = input(f'What would you like to name your {animal}?')
                added_ani = Animal(aname= compname, species = animal, special = True)
                added_ani.calculate_stats()
                team.total_sanctuary_animals.append(added_ani)
                team.boardlist[player].add_animals([added_ani])
                print(f'Added {compname} the {animal} to the sanctuary!')
                added_an_animal = True
            else:
                print('We do not have that animal, please rescue something else')

    team.feed = 10 * team.players
    print(f'Welcome to your sanctuary! Your founders are {[name for name in team.playernames]}, and your '
          f'starting ambassadors are {[a.aname for a in team.total_sanctuary_animals]}. May you keep the animals happy'
          f' and work to build a strong and lasting \n sanctuary! Let us begin, shall we? You will start with ${team.total_money}'
          f' and {team.feed} feed.')
    return team



def Rejuv(team):
    [board.reset() for board in team.boardlist]
    team.earn_money((10 * team.players) + team.supporters)
    print(f'Earned ${10 * team.players} from savings and ${team.supporters} from supporters')
    team.gain_inspiration_from_animals()
    team.overworked = 0

def actionUpkeep(team):
    where = int(input('Where would you like to perform upkeep? Choose an integer corresponding to the player number.'))
    try:
        if not team.boardlist[where].hasbeenlabored:
            end = team.boardlist[where].labor(team, False)
            print(f'Performed upkeep, end = {end}')
            if not end:
                print(f'Success. Food left:{team.feed}')
            if end:
                print('Failed to feed everyone')
                return end
        else:
            print('That board has already been done this turn! Action wasted.')
    except IndexError as e:
        print('tried to perform upkeep on a board that is not part of the sanctuary, action wasted!')
    # end = [board.labor(team, False) for board in team.boardlist]
def actionPurchaseFeed(team):
    neededfeed = sum([animal.feed for animal in team.total_sanctuary_animals])
    possible_feed = team.total_money // 2
    neededmoney = neededfeed * 2
    food_avail = team.feed
    print(f'You have ${team.total_money}.')
    print(f'You can buy {possible_feed} feed with your money and you have {food_avail} available.')
    print(f'You need {neededfeed} in order to feed all of your animals, which will cost ${neededmoney}.')
    try:
        amt = int(input('How much feed would you like to buy?'))
    except ValueError:
        print('Did not enter an integer, action wasted!')
        return
    if 0 <= amt <= possible_feed:
        if team.buy_feed(amt * 2):
            print(f'You bought {amt} feed. You have ${team.total_money} left.')
    else:
        print(
            'Could not perform action. You are either trying to buy too much feed or trying to buy negative feed! Action wasted')
def actionOrganizeFundraiser(team):
    d20 = random.randint(1, 20)
    team.earn_money(d20)
    insp = 0
    if 0 <= d20 <= 5:
        insp = -10
    elif 6 <= d20 <= 15:
        insp = 0
    elif 16<= d20 <= 19:
        insp = 5
    elif d20 == 20:
        insp = 10
    team.gain_inspiration(insp)
    print(f'You earned ${d20} and got {insp} inspiration.')

def Action(team, thirdact):
    if thirdact:
        num_actions = 1
        print('Someone is performing a third action, and the team will lose 10 inspiration at the end of the round!')
        team.overworked += 1
    else:
        num_actions = team.players * 2 + team.employees + (team.volunteers // 5)
    for n in range(0,num_actions):
        if not thirdact:
            if n >= team.players * 2:
                name = 'Employees and Volunteers'
            else:
                name = team.playernames[n//2]
            print(f"{name}'s actions.")
        else:
            name = 'Player'
        poss_actions = ['upkeep', 'purchase feed', 'organize fundraiser', 'hire employees', 'recruit volunteers', 'public outreach']
        action = input(f'{name}, what action would you like to do? Type an option:{poss_actions}').lower()
        if action == 'upkeep':
            actionUpkeep(team)
        elif action == 'purchase feed':
            actionPurchaseFeed(team)
        elif action == 'organize fundraiser':
            actionOrganizeFundraiser(team)
        elif action == 'hire employees':
            team.hire_employees(1)
        elif action == 'recruit volunteers':
            team.recruit_volunteers(1)
        elif action == 'public outreach':
            team.public_outreach()
        else:
            print('Invalid option, action wasted!')
        if not thirdact and n % 2 == 1 and n < team.players * 2:
            thirdaction = input(f'{name}, would you like to perform a third action? WARNING: this will cause you to become'
                                f' overworked! Enter yes or no. ').lower()
            if thirdaction == 'yes' or thirdaction == 'y':
                Action(team, thirdact = True)


def Resolution(team):
    team.lose_inspiration(team.overworked * 10)
    if team.employees != 0:
        team.pay_employees()
    if team.new_employees != 0:
        team.change_new_to_ready_employees()
    if team.inspiration <= -50:
        print(f'Lost the game; not enough inspiration to keep going! You ended with {team.inspiration} inspiration.')
        return True
    for animal in team.total_sanctuary_animals:
        if not animal.hasbeenfed:
            print(f'You did not feed {animal.aname}! You have lost the game.')
            return True
    return False


def main():
    roundnum = 1
    team = Setup()
    gameended = False
    while not gameended:
        feedfail = Action(team, thirdact=False)
        if feedfail:
            gameended = True
            print('Could not feed an animal, game ending')
            break
        upfail = Resolution(team)
        if upfail:
            gameended = True
            print('Did not feed all of the animals, game ending')
            break
        Rejuv(team)
        print(f'Round {roundnum} ended, moving onto next round. You have ${team.total_money} dollars and {team.feed} feed.')
        roundnum = roundnum + 1
        if roundnum >= 22:
            gameended = True
            print('It has been 22 rounds, and the game has ended!')
            vptotal = 0
            for animal in team.total_sanctuary_animals:
                vptotal += animal.vp
            print(f'Your total victory points were {vptotal}. Try to beat that score next time! Thanks for playing!')
main()
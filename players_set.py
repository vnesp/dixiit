import random
from player import Player

class PlayersSet:

    def __init__(self, data, deck, cards_in_hand):
        self.playersByName = {}
        self.potetialHosts = []
        for playerData in data:
            name = playerData['name']
            if name in self.playersByName:
                raise NameError('There are two players with name {}'.format(name))
            player = Player(playerData, deck, cards_in_hand)
            self.playersByName[name] = player
            self.potetialHosts.append(name)
        self.positionInPotetialHosts = {}
        for index, name in enumerate(self.potetialHosts):
            self.positionInPotetialHosts[name] = index


    def names(self):
        return self.playersByName.keys()


    def len(self):
        return len(self.playersByName)


    def items(self):
        return self.playersByName.items()


    def getPlayer(self, name):
        return self.playersByName[name]


    def removePotentialHost(self, index, name):
        lastName = self.potetialHosts[-1]
        self.potetialHosts[index] = lastName
        self.potetialHosts.pop()
        self.positionInPotetialHosts[lastName] = index
        del self.positionInPotetialHosts[name]


    def getHost(self, name):
        index = self.positionInPotetialHosts.get(name)
        if index is None:
            raise IndexError('Player {} have already been a host'.format(name))
        self.removePotentialHost(index, name)
        return self.getPlayer(name)


    def getRandomHost(self):
        index = random.randrange(0, len(self.potetialHosts))
        name = self.potetialHosts[index]
        self.removePotentialHost(index, name)
        return name, self.getPlayer(name)


    def getResults(self):
        return dict(map(
            lambda item: (item[0], item[1].getScore()),
            self.playersByName.items()
        ))

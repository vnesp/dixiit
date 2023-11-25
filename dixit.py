import random


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = set()

    def __str__(self):
        return self.name

    def putCard(self, card):
        self.hand.add(card)

    def getCard(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return True
        print("Player {} doesn't have card {}".format(self.name, card))
        return False

    def printState(self):
        print(self.name, self.hand)


class Deck:

    def __init__(self, numCards):
        self.numCards = numCards
        self.cards = list(range(1, numCards + 1))

    def getRandom(self):
        deckSize = len(self.cards)
        if deckSize == 0:
            print('Cannot get card from deck. Deck is empty!')
            ## TODO: Reshuffle all cards played in previous turns
            return
        index = random.randrange(0, deckSize)
        result = self.cards[index]
        self.cards[index] = self.cards[-1]
        self.cards.pop()
        return result


class Game:
       
    def __init__(self):
        self.file = open('game.txt', 'r', encoding='utf8')
        self.numPlayers, self.numTotalCards, self.numCardsInHand = map(int, self.file.readline().split())
        assert(self.numPlayers * (self.numCardsInHand + self.numPlayers - 1) <= self.numTotalCards)

        self.createPlayers()
        self.createDeck()
        self.giveCardsToEachPlayer(5)


    def createPlayers(self):
        self.players = []
        self.playersByName = {}
        for _ in range(self.numPlayers):
            name = self.file.readline().strip()
            player = Player(name)
            self.players.append(player)
            self.playersByName[name] = player
        random.shuffle(self.players)


    def createDeck(self):
        self.deck = Deck(self.numTotalCards)


    def giveCardFromDeck(self, player):
        card = self.deck.getRandom()
        if card is None:
            return
        player.putCard(card)


    def giveCardsToEachPlayer(self, count = 1):
        for player in self.players:
            for _ in range(count):
                self.giveCardFromDeck(player)


    def printState(self):
        for player in self.players:
            player.printState()
        print('Deck:', self.deck.cards)


game = Game()
game.printState()

import random


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = set()
        self.usedCards = set()
        self.score = 0


    def putCard(self, card):
        self.hand.add(card)


    def getCard(self, card):
        if card in self.hand:
            self.hand.remove(card)
            self.usedCards.add(card)
            return True
        print("Player {} doesn't have card {}".format(self.name, card))
        return False


    def takeBackCard(self, card):
        if card in self.usedCards:
            self.usedCards.remove(card)
            self.hand.add(card)
            return True
        print("Player {} haven't used card {}".format(self.name, card))
        return False


    def createAssociation(self):
        description = input('{}, give your assocciaton: '.format(self.name))
        card = self.chooseCard()
        return description, card


    def chooseCard(self):
        while True:
            card = int(input('{}, choose one of your cards ({}): '.format(self.name, self.hand)))
            if self.getCard(card):
                return card


    def printState(self):
        print(self.name)
        print('  hand:', self.hand)
        print('  score:', self.score)
        print()


    def addPoints(self, score):
        self.score += score


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


class Gallery:

    def __init__(self, host, players, playersByName):
        print('Stage 1: Making association')
        self.host = host
        self.players = players
        self.playersByName = playersByName
        self.cards = {}
        self.descriprion, self.hostcard = host.createAssociation()
        self.cards[host.name] = self.hostcard


    def choosePlayer(self, action):
        name = input('Choose player who is {} (name or number, 0 - end of stage): '.format(action))
        if name == '' or name == '0':
            return 0
        if name in self.playersByName:
            return self.playersByName[name]
        if not name.isdigit():
            return
        index = int(name) - 1
        if index >= len(self.players):
            return
        return self.players[index]


    def debtors(self, complete):
        return set(self.playersByName.keys()).difference(set(complete))


    def getCards(self):
        return self.cards.values()


    def pushCards(self):
        print('Stage 2: Pushing cards to gallery')
        while True:
            debtors = self.debtors(self.cards.keys())
            print('Gallery:', self.cards)
            print('Debtors:', debtors)
            player = self.choosePlayer('pushing card')
            if player is None:
                print('Unknown player')
                continue
            if player == 0:                
                if len(debtors) == 0 or input("Some players don't push their cards. Are you sure (y/n)? ").lower() == 'y':
                    break
                continue
            print('You have chosen', player.name)
            card = self.cards.get(player.name)
            if card is not None:
                print('Player {} have already pushed card {}'.format(player.name, card))
                if input('Are you sure to change player card in gallery (y/n)? ').lower() != 'y':
                    continue
                player.takeBackCard(card)
            card = self.cards[player.name] = player.chooseCard()
            if player == self.host:
                self.hostcard = card


    def chooseCard(self, name):
        galleryCards = set(self.getCards())
        card = self.cards.get(name)
        if card is not None:
            galleryCards.remove(card)
        while True:
            card = int(input('{}, choose one of gallery cards ({}): '.format(name, galleryCards)))
            if card in galleryCards:
                return card


    def voting(self):
        print('Stage 3: Voting')
        self.votes = {}
        while True:
            debtors = self.debtors(self.votes.keys())
            print('Votes:', self.votes)
            print('Debtors:', debtors)
            player = self.choosePlayer('sending vote')
            if player is None:
                print('Unknown player')
                continue
            if player == 0:                
                if len(debtors) == 0 or input("Some players don't send their votes. Are you sure (y/n)? ").lower() == 'y':
                    break
                continue
            print('You have chosen', player.name)
            card = self.votes.get(player.name)
            if card is not None:
                print('Player {} have already voted for card {}'.format(player.name, card))
                if input('Are you sure to change player vote (y/n)? ').lower() != 'y':
                    continue
            self.votes[player.name] = self.chooseCard(player.name)


    def calcResults(self):
        print('Stage 4: Calculating results')

        self.results = {}
        for name in self.playersByName.keys():
            self.results[name] = {
                'votes': [],
                'score': 0
            }

        owners = {}
        for name, card in self.cards.items():
            owners[card] = name

        hostResult = self.results[self.host.name]

        for name, card in self.votes.items():
            owner = owners[card]
            self.results[owner]['votes'].append(name)

        if len(hostResult['votes']) in {0, len(self.votes) - (self.host.name in self.votes)}:
            for name in self.cards.keys():
                self.results[name]['score'] = 2
            hostResult['score'] = 0
        else:
            if self.host.name in self.votes:
                hostResult['score'] = 3
            for name in hostResult['votes']:
                self.results[name]['score'] = 3

        for name, result in self.results.items():
            card = self.cards.get(name, '?')
            votes = result['votes']
            if name != self.host.name:
                result['score'] += len(votes)
            score = result['score']
            print('{} (card {}) - {} votes {} - {} points'.format(name, card, len(votes), votes, score))
            self.playersByName[name].addPoints(score)


class Game:
       
    def __init__(self):
        self.file = open('game.txt', 'r', encoding='utf8')
        self.numPlayers, self.numTotalCards, self.numCardsInHand = map(int, self.file.readline().split())
        assert(self.numPlayers * (self.numCardsInHand + self.numPlayers - 1) <= self.numTotalCards)
        self.createPlayers()
        self.createDeck()


    def start(self):
        random.shuffle(self.players)
        self.giveCardsToEachPlayer(self.numCardsInHand)
        self.round = 0
        for self.host in self.players:
            self.round += 1
            self.printState()
            currentGallery = Gallery(self.host, self.players, self.playersByName)
            print()
            currentGallery.pushCards()
            galleryCards = list(currentGallery.getCards())
            random.shuffle(galleryCards)
            print('Gallery for players:', galleryCards)
            print()
            currentGallery.voting()
            print('Voting:', currentGallery.votes)
            print()
            currentGallery.calcResults()
            print()
            self.giveCardsToEachPlayer()

    def createPlayers(self):
        self.players = []
        self.playersByName = {}
        for _ in range(self.numPlayers):
            name = self.file.readline().strip()
            player = Player(name)
            self.players.append(player)
            self.playersByName[name] = player


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
        print('Round {}\n'.format(self.round))
        print('Host: {}\n'.format(self.host.name))
        for player in self.players:
            player.printState()
        print('Deck:', self.deck.cards)
        print()


game = Game()
game.start()

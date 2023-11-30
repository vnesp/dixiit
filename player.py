import random

class Player:

    def __init__(self, data, deck, cards_in_hand):
        self.data = data
        if 'start_hand' not in self.data:
            self.data['start_hand'] = []
        self.createHand(self.data['start_hand'], deck, cards_in_hand)
        self.scoreByTurn = []
        self.score = 0


    def getName(self):
        return self.data['name']

    def getScore(self):
        return {
            'byTurn': self.scoreByTurn,
            'total': self.score
        }

    def createHand(self, start_hand, deck, cards_in_hand):
        if len(start_hand) > cards_in_hand:
            raise IndexError('Too much cards in start hand of player {}'.format(self.getName()))
        self.hand = {}
        for _id in start_hand:
            card = deck.popById(_id)
            self.hand[_id] = card
        for _ in range(len(start_hand), cards_in_hand):
            card = deck.popRandom()
            _id = card.getId()
            start_hand.append(_id)
            self.hand[_id] = card


    def pushCard(self, card):
        _id = card.getId()
        if _id in self.hand:
            raise IndexError('Player {} already have card {}'.format(self.getName(), _id))
        self.hand[_id] = card


    def popCard(self, _id):
        if _id not in self.hand:
            raise IndexError('Player {} does not have card {}'.format(self.getName(), _id))
        return self.hand.pop(_id)


    def popRandomCard(self):
        if len(self.hand) == 0:
            raise IndexError('Player {} does not have any cards'.format(self.getName()))
        _id = random.choice(list(self.hand.keys()))
        return _id, self.hand.pop(_id)


    def addPoints(self, score):
        self.scoreByTurn.append(score)
        self.score += score

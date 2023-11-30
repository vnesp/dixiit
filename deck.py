import random
from card import Card

class Deck:

    def __init__(self, data, allow_reshuffle):
        self.deck = []
        self.positionInDeck = {}
        self.playedCards = []
        self.allow_reshuffle = allow_reshuffle
        for cardData in data:
            card = Card(cardData)
            self.deck.append(card)
        self.indexingDeck()


    def indexingDeck(self):
        for index, card in enumerate(self.deck):
            _id = card.getId()
            self.positionInDeck[_id] = index


    def popByIndex(self, index):
        result = self.deck[index]
        lastCard = self.deck[-1]
        self.deck[index] = lastCard
        self.deck.pop()
        self.positionInDeck[lastCard.getId()] = index
        self.positionInDeck[result.getId()] = None
        return result


    def popRandom(self):
        deckSize = len(self.deck)
        if deckSize == 0 and self.allow_reshuffle:
            self.deck = self.playedCards
            self.indexingDeck()
            self.playedCards = []
        if deckSize == 0:
            raise IndexError('Cannot get card from deck. Deck is empty!')
        return self.popByIndex(random.randrange(0, deckSize))


    def popById(self, _id):
        index = self.positionInDeck.get(_id)
        if index is None:
            raise IndexError('Thers is no card {} in deck'.format(_id))
        return self.popByIndex(index)


    def pushBack(self, cards):
        self.playedCards.extend(cards)

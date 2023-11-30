import random

class Gallery:

    def __init__(self, host, description, hostcard):
        self.host = host
        self.descriprion = description
        self.hostcard = hostcard
        self.pushed = {}
        self.voted = {}
        self.pushed[host.getName()] = hostcard


    def getHost(self):
        return self.host


    def isHost(self, name):
        return self.host.getName() == name


    def isPushing(self, name):
        return name in self.pushed


    def popCard(self, name):
        card = self.pushed.pop(name)
        return card


    def pushCard(self, name, card):
        if self.isPushing(name):
            raise('Player {} has already pushed card'.format(name))
        self.pushed[name] = card


    def pushingPlayers(self):
        return set(self.pushed.keys())


    def shuffleCards(self):
        cards = list(map(lambda item: item.getId(), self.pushed.values()))
        random.shuffle(cards)
        self.cards = set(cards)
        return {
            'description': self.descriprion,
            'cards': cards
        }


    def isVoting(self, name):
        return name in self.voted


    def voteRandom(self, name):
        card = self.pushed.get(name)
        cardsForVote = list(self.cards - ({} if card is None else {card.getId()}))
        self.voted[name] = _id = random.choice(cardsForVote)
        return _id


    def vote(self, name, _id):
        if _id not in self.cards:
            raise IndexError('Player {} try to vote for card {}, but it is not in gallery'.format(name, _id))
        card = self.pushed.get(name)
        if card is not None and _id == card.getId():
            raise IndexError('Player {} try to vote for his card {}'.format(name, _id))
        self.voted[name] = _id


    def votingPlayers(self):
        return set(self.voted.keys())


    def calcStats(self):
        self.results = {}
        for name, card in self.pushed.items():
            _id = card.getId()
            self.results[_id] = { 'pushedBy': name }
        for name, _id in self.voted.items():
            votedBy = self.results[_id].setdefault('votedBy', [])
            votedBy.append(name)
        return self.results


    def getCountCorrectState(self):
        _id = self.hostcard.getId()
        votedBy = self.results[_id].get('votedBy')
        if votedBy is None:
            return 'none'
        elif len(votedBy) == len(self.voted) - (self.host.getName() in self.voted):
            return 'all'
        else:
            return 'general'


    def isCorrectVote(self, name):
        return self.voted[name] == self.hostcard.getId()


    def getAttractedCount(self, name):
        _id = self.pushed[name].getId()
        votedBy = self.results[_id].get('votedBy', [])
        return len(votedBy)


    def isAttractingHost(self, name):
        _id = self.pushed[name].getId()
        hostVoteId = self.voted.get(self.host.getName())
        return _id == hostVoteId


    def getPushedCards(self):
        return self.pushed.values()

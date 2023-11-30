from gallery import Gallery

class Turn:

    def __init__(self, data, settings, deck, players):
        self.data = data
        self.settings = settings
        self.deck = deck
        self.players = players


    def giveCards(self, data, playerNames, count):

        def giveTo(name, count, cards = None):
            if cards is None:
                if name in data:
                    return
                cards = []
            if not isinstance(cards, list):
                cards = [cards]
            if len(cards) > count:
                raise('Too much cards for player {}'.format(name))
            player = self.players.getPlayer(name)
            for _id in cards:
                card = self.deck.popCard(_id)
                player.pushCard(card)
            for _ in range(len(cards), count):
                card = self.deck.popRandom()
                _id = card.getId()
                cards.append(_id)
                player.pushCard(card)
            if count != 0:
                data[name] = cards[0] if count == 1 else cards

        host = self.gallery.getHost()
        for name, cards in data.items():
            if name == host.getName():
                giveTo(name, host, count['host'], cards)
            else:
                if name not in playerNames:
                    if len(cards) > 0:
                        raise('Player {} has not take part in stage and must not get cards')
                    continue
                giveTo(name, count['players'], cards)

        giveTo(host.getName(), count['host'])
        for name in playerNames:
            giveTo(name, count['player'])


    def associating(self):
        hostname = self.data.get('host')
        association = self.data.setdefault('association', { 'description': '' })
        if hostname is None:
            self.data['host'], host = self.players.getRandomHost()
        else:
            host = self.players.getHost(hostname)
        _id = association.get('card')
        if _id is None:
            association['card'], hostcard = host.popRandomCard()
        else:
            hostcard = host.popCard(_id)
        self.gallery = Gallery(host, association['description'], hostcard)
        self.giveCards(
            self.data.setdefault('cards_after_associating', {}),
            set(), self.settings['give_cards']['associating']
        )


    def pushing(self):
        data = self.data.setdefault('push', [])
        allow_changing_push = self.settings['allow_changing_push']
        if_no_push = self.settings['if_no_push']
        for item in data:
            name = item['player']
            player = self.players.getPlayer(name)
            if self.gallery.isHost(name):
                raise NameError('Host {} must not push card'.format(name))
            if self.gallery.isPushing(name):
                if not allow_changing_push:
                    raise NameError('Player {} has already pushed card'.format(name))
                card = self.gallery.popCard(name)
                player.pushCard(card)
            _id = item.get('card')
            if _id is None:
                item['card'], card = player.popRandomCard()
            else:
                card = player.popCard(_id)
            self.gallery.pushCard(name, card)
        if if_no_push != 'ignore':
            for name, player in self.players.items():
                if self.gallery.isPushing(name):
                    continue
                if if_no_push != 'randomize':
                    raise IndexError('Player {} has not pushed card'.format(name))
                _id, card = player.popRandomCard()
                self.gallery.pushCard(name, card)
                item = {
                    "player": name,
                    "card": _id
                }
                data.append(item)
        self.giveCards(
            self.data.setdefault('cards_after_pushing', {}),
            self.gallery.pushingPlayers(), self.settings['give_cards']['pushing']
        )
        self.data['gallery'] = self.gallery.shuffleCards()


    def voting(self):
        data = self.data.setdefault('vote', [])
        allow_changing_vote = self.settings['allow_changing_vote']
        if_no_vote = self.settings['if_no_vote']
        for item in data:
            name = item['player']
            if self.gallery.isVoting(name):
                if not allow_changing_vote:
                    raise NameError('Player {} has already voted'.format(name))
            _id = item.get('card')
            if _id is None:
                item['card'] = self.gallery.voteRandom(name)
            else:
                self.gallery.vote(name, _id)
        if if_no_vote != 'ignore':
            for name in self.players.names():
                if self.gallery.isVoting(name):
                    continue
                if if_no_vote != 'randomize':
                    raise IndexError('Player {} has not voted'.format(name))
                _id = self.gallery.voteRandom(name)
                item = {
                    "player": name,
                    "card": _id
                }
                data.append(item)
        self.giveCards(
            self.data.setdefault('cards_after_voting', {}),
            self.gallery.votingPlayers(), self.settings['give_cards']['voting']
        )
        self.data['results'] = self.gallery.calcStats()


    def scoring(self):
        data = self.data['score'] = {}
        scoring_table = self.settings['scoring']
        threshold_for_attracting = scoring_table.get('threshold_for_attracting', self.players.len())
        scheme = {}
        scheme.update(scoring_table['default'])
        scheme.update(scoring_table.get(self.gallery.getCountCorrectState(), {}))

        for name, player in self.players.items():
            item = data[name] = {}
            if self.gallery.isHost(name):
                score = scheme['host' if self.gallery.isVoting(name) else 'nonvoting_host']
                item['host'] = score
            else:
                score = 0
                if self.gallery.isVoting(name):
                    vote_score = scheme['correct_vote' if self.gallery.isCorrectVote(name) else 'incorrect_vote']
                    item['vote'] = vote_score
                    score += vote_score
                if self.gallery.isPushing(name):
                    attracted_count = self.gallery.getAttractedCount(name)
                    attracted_host = self.gallery.isAttractingHost(name)
                    attracted_count -= attracted_host
                    if attracted_count > threshold_for_attracting:
                        attracted_count = threshold_for_attracting
                    if attracted_count != 0:
                        players_attraction_score = attracted_count * scheme['attracted_player']
                        item['players_attraction'] = players_attraction_score
                        score += players_attraction_score
                    if attracted_host:
                        host_attraction_score = scheme['attracted_host']
                        item['host_attraction'] = host_attraction_score
                        score += host_attraction_score
            player.addPoints(score)

        self.deck.pushBack(self.gallery.getPushedCards())

        self.giveCards(
            self.data.setdefault('cards_after_scoring', {}),
            set(self.players.names()), self.settings['give_cards']['scoring']
        )

from deck import Deck
from players_set import PlayersSet
from turn import Turn

class Game:
       
    def __init__(self, data):
        self.data = data
        self.settings = data['settings']
        self.deck = Deck(data['deck'], self.settings['reshuffle'])
        self.players = PlayersSet(data['players'], self.deck, self.settings['cards_in_hand'])


    def start(self):
        self.turns = []
        for turnData in self.data['turns']:
            turn = Turn(turnData, self.settings, self.deck, self.players)
            turn.associating()
            turn.pushing()
            turn.voting()
            turn.scoring()
            self.turns.append(turn)

    def calcResults(self):
        self.data['results'] = self.players.getResults()

import json
from game import Game

# Read game object
with open('game.json', 'r', encoding='utf8') as file:
    obj = json.load(file)

# Create and start game
game = Game(obj)
game.start()
game.calcResults()

# Save game object
with open('game_after.json', 'w', encoding='utf8') as file:
   json.dump(obj, file, ensure_ascii=False, indent=2)

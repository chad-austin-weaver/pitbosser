class Dealer:

    def __init__(self, name, known_games):
        self.name = name
        self.known_games = known_games

    def __str__(self):
        return f"{self.name} {self.known_games}"

    def add_game(self, game):
        self.known_games.append(game)

    def getKnownGames(self):
        return self.known_games

    def getName(self):
        return self.name

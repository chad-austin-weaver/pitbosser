class Table:
    def __init__(self, table_id, game_type):
        self.table_id = table_id
        self.game_type = game_type

    def __str__(self):
        return f"{self.table_id} {self.game_type}"

    def getTableID(self):
        return self.table_id

    def getGameType(self):
        return self.game_type
    
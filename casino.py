import casinodealer
from constraint import *
import constraintfunction
import casinotable
import pandas as pd


class Casino:
    def __init__(self):
        self.maxReliefTables = 3
        self.gameTypes = []
        self.dealers = []
        self.dealersGames = {}
        self.tables = []
        self.tableVars = []
        self.reliefVars = []
        self.tables_of_type = {}

    def import_casino_from_upload_file(self, upload_file):
        df = pd.read_csv(upload_file)
        rows = [df.columns.tolist()]
        values = df.values.tolist()
        for value in values:
            rows.append(value)
        self.load_casino(rows)

    def load_casino(self, rows):
        self.maxReliefTables = int(rows[0][0])
        game_types = rows[0][1:]
        for game_type in game_types:
            self.gameTypes.append(game_type.strip().lower())

        i = 0
        for row in rows[2:]:
            temp_dealer = casinodealer.Dealer(str(row[0]), [])
            self.dealers.append(temp_dealer)
            j = 0
            for elem in row[1:]:
                if bool(int(elem)):
                    self.dealers[i].add_game(self.gameTypes[j])
                j += 1
            i += 1
        for game_type in self.gameTypes:
            self.dealersGames[game_type] = []
            for dealer in self.dealers:
                if game_type in dealer.getKnownGames():
                    self.dealersGames[game_type].append(dealer.name)

        input_tables = rows[1][:-1]
        if all(int(v) == 0 for v in input_tables):
            self.set_default_game_tables()
        else:
            i = 0
            for game_type in game_types:
                self.tables_of_type[game_type] = int(rows[1][i])
                for j in range(int(rows[1][i])):
                    self.tables.append(casinotable.Table(game_type + str(j), game_type))
                i += 1

    # TODO: Break some functions into helpers for readability(?)
    def set_default_game_tables(self):
        # Set tables for casino based on the below report's unit table mix for 2023.
        # See : https://gaming.library.unlv.edu/reports/strip_game_mix.pdf
        strip_game_mix = {
            "blackjack": 0.4841,
            "craps": 0.0781,
            "roulette": 0.1217,
            "3-card poker": 0.0377,
            "baccarat": 0.1608,
            "mini-baccarat": 0.0260,
            "let it ride": 0.0076,
            "pai gow": 0.0058,
            "pai gow poker": 0.0395,
            "other": 0.0386
        }

        total_share = 0.0
        remainders = {}

        for game_type in self.gameTypes:
            total_share += strip_game_mix[game_type]

        if "craps" in self.gameTypes:
            self.tables_of_type["craps"] = 0
            craps_ratio = strip_game_mix["craps"] / total_share
            least_diff = 1
            other_tables = (len(self.dealers)) * self.maxReliefTables // (self.maxReliefTables + 1)
            other_game_types = [x for x in self.gameTypes if x != "craps"]

            # Evaluates each possible combination of craps:other games for maximal closeness.
            # Must be found first, as this determines number of 'other' games to be assigned to other game types later.
            for i in range(len(self.dealersGames["craps"]) // 4 + 1):
                current_diff = abs(i / (other_tables - self.tables_of_type["craps"]) - craps_ratio)
                if current_diff <= least_diff:
                    least_diff = current_diff
                    self.tables_of_type["craps"] = i
                    other_tables = (len(self.dealers) - self.tables_of_type["craps"] * 4) * self.maxReliefTables // (
                            self.maxReliefTables + 1)
            for i in range(self.tables_of_type["craps"]):
                self.tables.append(casinotable.Table("craps" + str(i), "craps"))

            remaining_tables = other_tables
            # Finds whole number count for each other type of game.
            for game_type in other_game_types:
                div_count = int(strip_game_mix[game_type] * other_tables // total_share)
                self.tables_of_type.update({game_type: div_count})
                remaining_tables += -div_count
                remainder = strip_game_mix[game_type] * other_tables % total_share
                remainders.update({remainder: game_type})

            # Finds the games with the highest remainder of game share to maximize open tables.
            for i in range(remaining_tables):
                max_remain = max(remainders.keys())
                game_type = remainders.pop(max_remain)
                self.tables_of_type[game_type] += 1

            for game_type in other_game_types:
                for i in range(self.tables_of_type[game_type]):
                    self.tables.append(casinotable.Table(game_type + str(i), game_type))

        else:
            # Similar to assignment logic above, only, skipping the pre-eminent dice procedures.
            remainders = {}
            other_tables = len(self.dealers) * self.maxReliefTables // (self.maxReliefTables + 1)

            remaining_tables = other_tables
            for game_type in self.gameTypes:
                div_count = int(strip_game_mix[game_type] * other_tables // total_share)
                self.tables_of_type.update({game_type: div_count})
                remaining_tables += -div_count
                remainder = strip_game_mix[game_type] * other_tables % total_share
                remainders.update({remainder: game_type})

            for i in range(remaining_tables):
                max_remain = max(remainders.keys())
                game_type = remainders.pop(max_remain)
                self.tables_of_type[game_type] += 1

            for game_type in self.gameTypes:
                for i in range(self.tables_of_type[game_type]):
                    self.tables.append(casinotable.Table(game_type + str(i), game_type))

    def set_table_variables(self, problem):
        for table in self.tables:
            if table.getGameType() == "craps":
                craps_table = []
                for x in range(4):
                    table_var = table.getTableID() + f"({x})"
                    craps_table.append(table_var)
                    self.tableVars.append(table_var)
                    problem.addVariable(table_var, self.getDealersByGame("craps"))
                problem.addConstraint(FunctionConstraint(constraintfunction.sort_craps_table), craps_table)

            else:
                table_var = table.getTableID()
                relief_var = 'r-' + table.getTableID()
                self.tableVars.append(table_var)
                self.reliefVars.append(relief_var)
                problem.addVariable(table_var, self.getDealersByGame(table.getGameType()))
                problem.addVariable(relief_var, self.getDealersByGame(table.getGameType()))

    def getMaxReliefTables(self):
        return self.maxReliefTables

    def getGameTypes(self):
        return self.gameTypes

    def getDealers(self):
        return self.dealers

    def getDealersGames(self):
        return self.dealersGames

    def getDealersByGame(self, game):
        return self.dealersGames[game]

    def getTables(self):
        return self.tables

    def getTablesOfType(self):
        return self.tables_of_type

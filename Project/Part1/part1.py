
import pandas as pd
from collections import defaultdict, Counter

import unittest

import os, sys

from pathlib import Path

""" Aggregation function used by pandas dataframe """
def agg_score(x):
    res = {
        "Pts": x["Pts"].sum(),
        "GD": x["Net"].sum(),
        "GF": x["Score"].sum(),
    }
    return pd.Series(res)


def basic(df_agg, df, messages):
    """ Sorting by Pts, GD and GF descendingly """
    df_agg.sort_values(by=["Pts", "GD", "GF"], ascending=[False, False, False], inplace=True)

def FIFA2018(df_agg, df, messages):
    """ Sorting by Pts, GD and GF descendingly """
    df_agg.sort_values(by=["Pts", "GD", "GF"], ascending=[False, False, False], inplace=True)

    """ Find if using Pts, GD and GF still results in any draw. """
    draws = df_agg.duplicated(subset=["Pts", "GD", "GF"], keep=False)

    """ If there is any draw, need to check the matches among those teams. """
    if any(draws):
        df_agg.reset_index(inplace=True)

        """
        Find which teams belong to the same (Pts, GD, GF) set using row id.
        """
        stats = defaultdict(list)
        for i in range(len(df_agg)):
            idx = df_agg.Team[i]
            pts, net, score = list(df_agg.loc[df_agg.Team==idx, ["Pts", "GD", "GF"]].values[0])
            stats[pts, net, score].append(i)

        """
        Loop over the (Pts, GD, GF) sets to rank the draw teams.
        """
        for k in sorted(stats, key=lambda x: len(stats[x]), reverse=True):
            "Row id of (Pts, GD, GF) k"
            ids = stats[k]

            """ No need to rank if the team has a unique (Pts, GD, GF). """
            if len(ids) <= 1: continue

            """ Convert row id to team name """
            teams = list(map(df_agg.Team.__getitem__, ids))

            msg = "{} are in a draw.".format('-'.join(teams))
            print(msg)

            """ Extract from the original data for only the concerned teams. """
            df_concerned = df.loc[(df.Team.isin(teams)) & (df.Opponent.isin(teams))]

            """ Do the same aggregation and sorting as done before. """
            df_concerned_agg = df_concerned.groupby(["Team"])["Score", "Pts", "Net"].apply(agg_score)
            df_concerned_agg.sort_values(by=["Pts", "GD", "GF"], ascending=[False, False, False], inplace=True)

            """ Check if there is still duplicated (Pts, GD, GF) for stats among the concerned teams. """
            draws_concerned = df_concerned_agg.duplicated(subset=["Pts", "GD", "GF"], keep=False)
            
            if any(draws_concerned):
                """ 
                If those teams are still draw, give up since lack the cards data.
                """
                msg = "{} cannot be ranked.".format('-'.join(teams))
                print(msg)
                messages.append(msg)
                return pd.DataFrame()
            else:
                """
                Since there is no more duplicates, the strategy is successful.
                Now we need to change the order of team data in the original aggregated dataframe
                to the new order as in df_concerned_agg.
                """
                msg = "{} should be reordered to {} based on concerned matches.".format('-'.join(teams), '-'.join(list(df_concerned_agg.index)))
                print(msg)

                """ Get the row id in the original agg dataframe of the new team name order """
                ids2 = list(map(list(df_agg["Team"]).index, list(df_concerned_agg.index)))
                for id1, id2 in zip(ids, ids2):
                    if ids == ids2: break
                    if id1 != id2:
#                        print("Swap {} and {}".format(df_agg.Team[id1], df_agg.Team[id2]))
                        """ Swap the two entries by row id """
                        df_agg.iloc[id1], df_agg.iloc[id2] = df_agg.iloc[id2], df_agg.iloc[id1]
                        j, k = ids.index(id1), ids.index(id2)
                        ids[j], ids[k] = ids[k], ids[j]

        df_agg.set_index("Team", inplace=True)
    return df_agg

class Rank:
    """
    The Rank class applies a rule for a match dataset.
    The default rule is basic that only ranks based 
    (Pts, GD, GF) descendingly. To use the FIFA2018 rule
    please do:
        rank = Rank(FIFA2018)
    The calculation is done in the call function so you
    can run a sample data as:
        res = rank("some_test_data")
    """

    def __init__(self, rule=basic):
        """ Initialize with desired rule """
        self.rule = rule

    def calc_pts(self, df):
        """
        Calculate Pts and net goals from the score data
        A win is 3 pts while a draw is 1 for both teams
        """
        df["Team 1 Pts"] = 1
        df["Team 2 Pts"] = 1
        df.loc[df["Team 1 score"] > df["Team 2 score"], "Team 1 Pts"] = 3
        df.loc[df["Team 1 score"] > df["Team 2 score"], "Team 2 Pts"] = 0
        df.loc[df["Team 1 score"] < df["Team 2 score"], "Team 1 Pts"] = 0 
        df.loc[df["Team 1 score"] < df["Team 2 score"], "Team 2 Pts"] = 3

        """ Calculate the net score for each match """
        df["Team 1 Net"] = df["Team 1 score"] - df["Team 2 score"]
        df["Team 2 Net"] = -df["Team 1 Net"]

    def __call__(self, input_file):
        """ Read the input file """
        print("Input: {}, rule: {}".format(input_file, self.rule.__name__))
        df = pd.read_csv(input_file)

        base = os.path.basename(input_file)

        """ Call the calc_pts function to calculate the points for each match """
        self.calc_pts(df)

        """ 
        Duplicate the data to get 12 rows by swapping Team 1 and Team 2, 
        convenient for aggregation 
        """
        df1 = df.copy(deep=True)
        df2 = df.copy(deep=True)
        df1.columns = ["Game", "Team", "Opponent", "Score", "Opponent Score", "Pts", "Opponent Pts", "Net", "Opponent Net"]
        df2.columns = ["Game", "Opponent", "Team", "Opponent Score", "Score", "Opponent Pts", "Pts", "Opponent Net", "Net"]
        df = pd.concat([df1, df2], sort=False)

        """ 
        Using function agg_score to aggregate the points, can use sum() instead.
        """ 
        df_agg = df.groupby(["Team"])["Score", "Pts", "Net"].apply(agg_score)

        """ Save the output stats files in ./results """
        path = Path("./results")
        if not os.path.exists(path):
            os.makedirs(path)

        """ Output messages """
        messages = []
        try:
            """ Applying the rule for ranking """
            df_agg = self.rule(df_agg, df, messages)
        except Exception as e:
            print("Exception in using rule {}, {}".format(self.rule.__name__, e))
        else:
            """ Save the stats file """
            df_agg.to_csv(path / ("stats_" + base), index=True)
            result = ""

            """ Result rank string is team names separated by : """
            if not df_agg.empty:
                result = ":".join(list(df_agg.index))

            """ Add message to the output file """
            with open(path / ("result_" + base), 'w') as f:
                f.write(result + '\n' + " ".join(messages))

            """ Return the string """
            return result
        

class TestFIFA2018(unittest.TestCase):

    def setUp(self):
        self.rank = Rank(FIFA2018)

    def tearDown(self):
        return super().tearDown()

    def test_part1_test_01(self):
        self.assertEqual(self.rank("data/part1_test_01.csv"), "A:C:B:D")

    def test_part1_test_02(self):
        self.assertEqual(self.rank("data/part1_test_02.csv"), "B:A:C:D")

    def test_part1_test_03(self):
        self.assertEqual(self.rank("data/part1_test_03.csv"), "A:B:D:C")

    def test_part1_test_04(self):
        self.assertEqual(self.rank("data/part1_test_04.csv"), "B:A:D:C")

    def test_part1_test_05(self):
        self.assertEqual(self.rank("data/part1_test_05.csv"), "")

    def test_part1_test_06(self):
        self.assertEqual(self.rank("data/part1_test_06.csv"), "B:C:D:A")

    def test_WorldCup2018_GroupA(self):
        self.assertEqual(self.rank("data/WorldCup2018_GroupA.csv"), 
                                   "Uruguay:Russia:Saudi Arabia:Egypt")

    def test_WorldCup2018_GroupB(self):
        self.assertEqual(self.rank("data/WorldCup2018_GroupB.csv"), 
                                   "Spain:Portugal:Iran:Morocco")

    def test_WorldCup2018_GroupC(self):
        self.assertEqual(self.rank("data/WorldCup2018_GroupC.csv"), 
                                   "France:Denmark:Peru:Australia")

    def test_WorldCup2018_GroupD(self):
        self.assertEqual(self.rank("data/WorldCup2018_GroupD.csv"), 
                                   "Crotia:Argentina:Nigeria:Iceland")

    def test_WorldCup2018_GroupE(self):
        self.assertEqual(self.rank("data/WorldCup2018_GroupE.csv"), 
                                   "Brazil:Switzerland:Serbia:Costa Rica")

    def test_WorldCup2018_GroupF(self):
        self.assertEqual(self.rank("data/WorldCup2018_GroupF.csv"), 
                                   "Sweden:Mexico:South Korea:Germany")

    def test_WorldCup2018_GroupG(self):
        self.assertEqual(self.rank("data/WorldCup2018_GroupG.csv"), 
                                   "Belgium:England:Tunisia:Panama")

    def test_WorldCup2018_GroupH(self):
        self.assertEqual(self.rank("data/WorldCup2018_GroupH.csv"), "")

    def test_WorldCup2014_GroupA(self):
        self.assertEqual(self.rank("data/WorldCup2014_GroupA.csv"), 
                                   "Brazil:Mexico:Croatia:Cameroon")
        
    def test_WorldCup2014_GroupB(self):
        self.assertEqual(self.rank("data/WorldCup2014_GroupB.csv"), 
                                   "Netherlands:Chile:Spain:Australia")
        
    def test_WorldCup2014_GroupC(self):
        self.assertEqual(self.rank("data/WorldCup2014_GroupC.csv"), 
                                   "Colombia:Greece:Ivory Coast:Japan")
        
    def test_WorldCup2014_GroupD(self):
        self.assertEqual(self.rank("data/WorldCup2014_GroupD.csv"), 
                                   "Costa Rica:Uruguay:Italy:England")
        
    def test_WorldCup2014_GroupE(self):
        self.assertEqual(self.rank("data/WorldCup2014_GroupE.csv"), 
                                   "France:Switzerland:Ecuador:Honduras")
        
    def test_WorldCup2014_GroupF(self):
        self.assertEqual(self.rank("data/WorldCup2014_GroupF.csv"), 
                                   "Argentina:Nigeria:Bosnia and Herzegovina:Iran")
        
    def test_WorldCup2014_GroupG(self):
        self.assertEqual(self.rank("data/WorldCup2014_GroupG.csv"), 
                                   "Germany:USA:Portugal:Ghana")

    def test_WorldCup2014_GroupH(self):
        self.assertEqual(self.rank("data/WorldCup2014_GroupH.csv"), 
                                   "Belgium:Algeria:Russia:South Korea")


if __name__ == "__main__":
    unittest.main()

    """ Run with a single data file """
    rank = Rank(FIFA2018)
    print(rank("data/part1_test_01.csv"))

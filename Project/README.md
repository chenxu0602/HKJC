
Both parts are done with python3.7. Please install numpy, scipy and pandas or do
$ pip3 install -r requirements

Structure of the folder:

Part1
   - README.md                              # Instruction document
   - part1.py                               # The python script that includes the function and unit test.
   - data                                   # The test samples.
      -- part1_test_0[12356].csv            # Samples I made up.
      -- WorldCup2014_Group[ABCDEFGH].csv   # 2014 World Cup group matches
      -- WorldCup2018_Group[ABCDEFGH].csv   # 2018 World Cup group matches
   - results                                # The test results.
      -- results_[Data File Name].csv       # Ranked team names as a string delimited by ':'. 
      -- stats_[Data File Name].csv         # Ranked (Pts, GD, GF).

Part2 
   - part2.py                               # Python script


The rule of ranking is from https://www.fifa.com/worldcup/news/tie-breakers-for-russia-2018-groups 
The item would be used in ranking in case the previous one results in a draw:
1. Pts
2. GD
3. GF
4. Pts of concerned teams
5. GD of concerned teams
6. GF of concerned teams

The following rules are not used because the red/yellow card information is not available.
* greater number of points obtained in the fair play conduct of the teams based on yellow and red cards received in all group matches.
* drawing of lots by the FIFA.

To run the script with all the unittest cases, please do:

$ cd Part1
$ python3 part1.py -v

To run the script with a single test case, please commnet line 276 "unittest.main()" and modify the last line for data file names.


The algorithm is in class Rank and function FIFA2018 in part1.py. A Rank object would be initiazlied with a rule (FIFA2018 in this case).
The input test file name is passed in the __call__ function, thus it could be used in this way:

   r = Rank()
   result = r("Test File")

Function FIFA2018 (line 25) implements the rules aformentioned. First the Pts dataframe is sorted by (Pts, GD, GF).
If there is any duplicates, it means at least two teams couldn't be distingushed by (Pts, GD, GF) in ranking.
Thus, those teams would be extracted from the original score dataframe and do the same operations as we did to all the teams.
The new dataframe that contains 2 or 3 teams should give the correct order among those teams. If there are still duplicates,
the algorithm would fail since we'd need the card information to further rank them.
There are cases that the algorithm would fail. For example, in data/part1_test_05.csv, three teams have the same (Pts, GD, GF)
and their relative performance is also a circle. In such a case, an empty string and an explanation would be dumped to file
data/result_part1_test_05.csv.


The 2nd part just run
$ python3 part2.py


from math import exp, factorial
from scipy.stats import skellam

def poisson(l, k):
    """ Poission function with interval: l """
    return pow(l, k) * exp(-l) / factorial(k)


print("Consider the game is the combination of the superposition of two independent poission processes N1 and N2.")
print("Assuming team i is the home team while team j is the away.")

mu1, mu2 = 1.55, 1.05
print(f"\nThe HAD pool can be modeled by N1 - N2, which is a skellam distribution with mu1 = {mu1} and mu2 = {mu2}.")
print("Alternatively, we can do Sum(N1 * N2) over all cases that have k_n1 > k_n2, k_n1 = k_n2 or k_n1 < k_n2 with a cutoff at some threshold.")

sk = skellam(mu1, mu2)
had_draw = sk.pmf(0)
had_away = sk.cdf(-1)
had_home = 1.0 - had_draw - had_away
print("The probablity of HAD HOME|AWAY|DRAW: {:.2f}%|{:.2f}%|{:.2f}%.".format(had_home*100, had_away*100, had_draw*100))

had_home_odds_true = 1.0 / had_home
had_away_odds_true = 1.0 / had_away
had_draw_odds_true = 1.0 / had_draw
print("The decimal odds of HAD HOME|AWAY|DRAW: {:.2f}|{:.2f}|{:.2f}.".format(\
        had_home_odds_true, had_away_odds_true, had_draw_odds_true))

had_margin = 0.123
had_home_odds_margin = 1.0 / had_home / (1 + had_margin)
had_away_odds_margin = 1.0 / had_away / (1 + had_margin)
had_draw_odds_margin = 1.0 / had_draw / (1 + had_margin)
print("\nFrom web https://bet.hkjc.com/football/default.aspx?lang=en the HAD pool has a margin roughly {:.2f}%.".format(had_margin*100))
print("I couldn't find any explicit margin from the web. So I took a few odds and calculated the margin as (1/HOME + 1/AWAY + 1/DRAW) - 1.")
print("I used the similar method to calculcate the margins in other cases.")
print("Apply the margin the odds of HAD HOME|AWAY|DRAW we get {:.2f}|{:.2f}|{:.2f}.".format(\
        had_home_odds_margin, had_away_odds_margin, had_draw_odds_margin))


print("\n\nThe HiLo 2.5 goal line pool can be modeled by N1 + N2, which is a poisson distribution with expectancy {:.2f}".format(mu1+mu2))

expect= mu1 + mu2
HiLo_25_under = poisson(expect, 0) + poisson(expect, 1) + poisson(expect, 2)
HiLo_25_over = 1.0 - HiLo_25_under
print("The probability of HiLo HIGH|LOW: {:.2f}%|{:.2f}%.".format(HiLo_25_over*100, HiLo_25_under*100))

HiLo_25_under_odds_true = 1.0 / HiLo_25_under
HiLo_25_over_odds_true = 1.0 / HiLo_25_over
print("The decimal odds of HiLo 2.5 HIGH|DRAW: {:.2f}|{:.2f}.".format(HiLo_25_over_odds_true, HiLo_25_under_odds_true))

HiLo_25_margin = 0.082
print("From web https://bet.hkjc.com/football/default.aspx?lang=en the HiLo pool has a margin roughly {:.2f}%.".format(HiLo_25_margin*100))

HiLo_25_under_odds_margin = 1.0 / HiLo_25_under / (1 + HiLo_25_margin)
HiLo_25_over_odds_margin = 1.0 / HiLo_25_over / (1 + HiLo_25_margin)
print("Apply the margin the odds of HiLo 2.5 HIGH|DRAW we get {:.2f}|{:.2f}.".format(HiLo_25_over_odds_margin, HiLo_25_under_odds_margin))

print("\n\nThe FHAD problem can be modelled by shortening the expectancy in the poisson model by half.")

sk_half = skellam(mu1/2.0, mu2/2.0)
fhad_draw = sk_half.pmf(0)
fhad_away = sk_half.cdf(-1)
fhad_home = 1.0 - fhad_draw - fhad_away
print("The probablity of FHAD first half HOME|AWAY|DRAW: {:.2f}%|{:.2f}%|{:.2f}%.".format(fhad_home*100, fhad_away*100, fhad_draw*100))

fhad_home_odds_true = 1.0 / fhad_home
fhad_away_odds_true = 1.0 / fhad_away
fhad_draw_odds_true = 1.0 / fhad_draw
print("The decimal odds of FHAD first half HOME|AWAY|DRAW: {:.2f}|{:.2f}|{:.2f}.".format(\
        fhad_home_odds_true, fhad_away_odds_true, fhad_draw_odds_true))

fhad_margin = 0.128
fhad_home_odds_margin = 1.0 / fhad_home / (1 + fhad_margin)
fhad_away_odds_margin = 1.0 / fhad_away / (1 + fhad_margin)
fhad_draw_odds_margin = 1.0 / fhad_draw / (1 + fhad_margin)
print("From web https://bet.hkjc.com/football/default.aspx?lang=en the FHAD pool has a margin roughly {:.2f}%.".format(fhad_margin*100))
print("Apply the margin the odds of FHAD first half HOME|AWAY|DRAW we get {:.2f}|{:.2f}|{:.2f}.".format(\
        fhad_home_odds_margin, fhad_away_odds_margin, fhad_draw_odds_margin))

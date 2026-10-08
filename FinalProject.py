from pathlib import Path 
 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
 
from scipy.stats import pearsonr 
from scipy.stats import f_oneway 

# Folder where this Python file is located
folder = Path(__file__).parent
 
# --------------------------------------------------------- 
# 1. LOAD THE DATA 
# --------------------------------------------------------- 
filename = "C:\\Users\\david\\Desktop\\MAT2007 programing\\Final Project\\tennis_matches_2014_2025.csv" 
 
try: 
    df = pd.read_csv(filename) 
    print("File loaded successfully!") 
 
except FileNotFoundError: 
    print("Error: the file was not found.") 
    exit() 
 
print("Number of matches:", len(df)) 
# --------------------------------------------------------- 
# 2. KEEP ONLY COMPLETED MATCHES 
# --------------------------------------------------------- 
df = df[df["completed"] == 1] 
 
# We also need odds and game scores 
df = df.dropna( 
    subset=[ 
        "total_games_a", 
        "total_games_b", 
        "bet365_odds_a", 
        "bet365_odds_b" 
    ] 
) 
 
print("Completed matches with useful data:", len(df)) 
# --------------------------------------------------------- 
# 3. CALCULATE THE AVERAGE BOOKMAKER ODDS 
# --------------------------------------------------------- 
 
bookmakers = ["bet365", "Betfair", "Ladbrokes", "Unibet"] 
 
odds_a_columns = [] 
odds_b_columns = [] 
 
i = 0 
 
while i < len(bookmakers): 
 
    bookmaker = bookmakers[i] 
 
    odds_a_columns.append(bookmaker + "_odds_a") 
    odds_b_columns.append(bookmaker + "_odds_b") 
 
    i += 1 
 
# Calculate the average odds available 
df["average_odds_a"] = df[odds_a_columns].mean(axis=1) 
df["average_odds_b"] = df[odds_b_columns].mean(axis=1) 
 
# Remove matches where we cannot calculate both averages 
df = df.dropna( 
    subset=["average_odds_a", "average_odds_b"] 
) 
# --------------------------------------------------------- 
# 4. PROTECT AGAINST INVALID ODDS 
# --------------------------------------------------------- 
 
df = df[ 
    (df["average_odds_a"] > 1) & 
    (df["average_odds_b"] > 1) 
] 
# --------------------------------------------------------- 
# 5. CALCULATE BOOKMAKER PREDICTION 
# --------------------------------------------------------- 
# Convert decimal odds into implied probabilities 
 
df["probability_a_raw"] = 1 / df["average_odds_a"] 
df["probability_b_raw"] = 1 / df["average_odds_b"] 
 
# Normalise the probabilities so they add up to 1 
 
df["probability_a"] = ( 
    df["probability_a_raw"] / 
    (df["probability_a_raw"] + df["probability_b_raw"]) 
) 
 
df["probability_b"] = ( 
    df["probability_b_raw"] / 
    (df["probability_a_raw"] + df["probability_b_raw"]) 
) 
# ------------------------------------------------------- 
# 6. CALCULATE BOOKMAKER CONFIDENCE 
# --------------------------------------------------------- 
 
df["probability_difference"] = ( 
    df["probability_a"] - df["probability_b"] 
) 
# --------------------------------------------------------- 
# 7. CALCULATE MATCH DOMINANCE 
# --------------------------------------------------------- 
 
df["game_margin"] = ( 
    df["total_games_a"] - df["total_games_b"] 
) 
# --------------------------------------------------------- 
# 8. CREATE CATEGORIES 
# --------------------------------------------------------- 
 
def classify_prediction(probability_difference): 
 
    if probability_difference < 0: 
        return "Underdog winner" 
 
    elif probability_difference < 0.20: 
        return "Slight favourite" 
 
    elif probability_difference < 0.50: 
        return "Moderate favourite" 
 
    else: 
        return "Strong favourite" 
 
df["prediction_category"] = df["probability_difference"].apply( 
    classify_prediction 
) 
# --------------------------------------------------------- 
# 9. BASIC STATISTICS 
# ------------------------------------------------------------- 
 
print("\n---------------------------------------------") 
print("BASIC STATISTICS") 
print("---------------------------------------------") 
 
print( 
    df[ 
        [ 
            "average_odds_a", 
            "average_odds_b", 
            "probability_difference", 
            "game_margin" 
        ] 
    ].describe() 
) 
# --------------------------------------------------------- 
# 10. MATCH DOMINANCE BY BOOKMAKER CATEGORY 
# --------------------------------------------------------- 
print("\n---------------------------------------------") 
print("MATCH DOMINANCE BY BOOKMAKER CATEGORY") 
print("---------------------------------------------") 
 
statistics = df.groupby( 
    "prediction_category")["game_margin"].agg( 
    ["mean", "std", "count"]) 
 
print(statistics) 
# --------------------------------------------------------- 
# 11. CORRELATION 
# --------------------------------------------------------- 
correlation, p_value = pearsonr( 
    df["probability_difference"], 
    df["game_margin"]) 
 
print("\n---------------------------------------------") 
print("CORRELATION") 
print("---------------------------------------------") 
 
print("Pearson correlation =", correlation) 
print("p-value =", p_value) 
 
# --------------------------------------------------------- 
# 12. ONE-WAY ANOVA 
# --------------------------------------------------------- 
 
underdog = df[ 
    df["prediction_category"] == "Underdog winner" 
]["game_margin"] 
 
slight = df[ 
    df["prediction_category"] == "Slight favourite" 
]["game_margin"] 
 
moderate = df[ 
    df["prediction_category"] == "Moderate favourite" 
]["game_margin"] 
 
strong = df[ 
    df["prediction_category"] == "Strong favourite" 
]["game_margin"] 
 
 
F, anova_p = f_oneway( 
    underdog, 
    slight, 
    moderate, 
    strong) 
 
print("\n---------------------------------------------") 
print("ONE-WAY ANOVA") 
print("---------------------------------------------") 
 
print("F =", F) 
print("p-value =", anova_p) 
# --------------------------------------------------------- 
# 13. BOXPLOT 
# ------------------------------------------------------------- 
 
plt.figure(figsize=(9, 6)) 
df.boxplot( 
    column="game_margin", 
    by="prediction_category") 
plt.xlabel("Bookmaker prediction") 
plt.ylabel("Winner - loser game difference") 
plt.title( 
    "Match dominance according to bookmaker prediction") 
plt.suptitle("") 

plt.savefig(folder / "boxplot.png", dpi=300, bbox_inches="tight")

plt.show() 
# --------------------------------------------------------- 
# 14. SCATTER PLOT 
# --------------------------------------------------------- 
 
plt.figure(figsize=(9, 6)) 
plt.scatter( 
    df["probability_difference"], 
    df["game_margin"], 
    alpha=0.15) 
plt.xlabel("Difference in implied probability") 
plt.ylabel("Winner - loser game difference") 
plt.title("Bookmaker prediction vs match dominance") 

plt.savefig(folder / "scatterplot.png", dpi=300, bbox_inches="tight")

plt.show() 
 
# --------------------------------------------------------- 
# 15. FINAL CHECK 
# --------------------------------------------------------- 
 
print("\n---------------------------------------------") 
print("FINAL DATASET") 
print("---------------------------------------------") 
 
print("Number of analysed matches:", len(df)) 
 
print( 
    "Average game margin:", 
    df["game_margin"].mean()) 
 
print( 
    "Average bookmaker probability difference:", 
    df["probability_difference"].mean())

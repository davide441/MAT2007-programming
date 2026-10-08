# Tennis Project – Bookmaker Confidence and Match Dominance

## 1. Description

This project investigates whether bookmaker confidence in the predicted winner of a tennis match is related to how dominant the player's victory is.

The analysis uses tennis match results and betting odds from 2014 to 2025. The Python program calculates variables such as the difference in bookmaker odds/probabilities and the difference in games won between the two players. It then uses statistical analysis and visualisations to investigate the relationship between bookmaker confidence and match dominance to see if any evident correlation can be found.

---

## 2. What the Script Does

The python script performs the following:

1. Loads the tennis dataset from a CSV file.
2. Checks that the required file can be found.
3. Cleans/Filters the data by removing rows with missing or unusable values (criterias for discarding data are later explained)
4. Identifies the winner and loser of each match.
5. Calculates the bookmaker's implied probability for each player from their betting odds.
6. Calculates the difference in bookmaker probability between the winner and loser.
7. Calculates the difference in games won between the winner and loser as a measure of match dominance.
8. Separates matches into groups according to bookmaker confidence, including favourites and underdogs.
9. Calculates statistics for the variables.
10. Performs statistical analysis using ANOVA one way test to compare game margins between groups.
11. Creates plots to visualise the relationship between bookmaker confidence and match dominance.
12. Prints the main statistical results to the terminal.

The final results have then been used to answer the following research question:

**Can bookmaker odds tell us something about how dominant a player will be during a tennis match?**

---
## 3. Requirements and Installation

The program needs to be have Python 3 (latest version)

The following Python libraries are used:

* `pandas`
* `numpy`
* `matplotlib`
* `scipy`

If these libraries are not already installed, they can be installed using:

```bash
pip install pandas numpy matplotlib scipy
```

The program was developed and tested using Python 3.

---

## 4. How to Run the Code

### Step 1 – Download the dataset

Download the dataset from Kaggle (open-source access):

https://www.kaggle.com/datasets/alimoh89/tennis-results-and-betting-odds-20142025

The used CSV file (in this case tennis match file) should be placed in the **same folder as the Python program**.

The program expects the dataset file to be named:

```text
tennis_matches_2014_2025.csv
```

### Step 2 – Open the Python file

Open the project in **VS Code**.

Make sure that the Python interpreter is correctly selected (can be done by selecting the programming language at the top right-bottom of the interface).

### Step 3 – Install the dependencies

Open the terminal and run:

```bash
pip install pandas numpy matplotlib scipy
```

### Step 4 – Run the program

Run the Python file from VS Code or from the terminal:

```bash
python FinalProject.py
```

If the CSV file is in the same folder as the Python file, the program should be able to load it directly.

---

## 5. Dataset

The dataset contains tennis match results and betting odds for matches played between 2014 and 2025 of men's and women's division (ATP and WTA)

The original dataset is available on Kaggle:

https://www.kaggle.com/datasets/alimoh89/tennis-results-and-betting-odds-20142025

The dataset contains information about the two players, the match winner and loser, betting odds, and match results.

For this project:

* `player_a` is treated as the **winner**
* `player_b` is treated as the **loser**
* The bookmaker odds are used to estimate bookmaker confidence.
* The game scores are used to calculate the dominance of the victory.

---

## 6. Data Cleaning

The original dataset does not need to be manually modified before running the program.

However, the Python code performs data cleaning during execution. Rows containing missing or invalid values required for the analysis are removed before the calculations are performed.

Therefore, to reproduce the results, the **original Kaggle dataset should be used without manually editing it**.

The cleaning and filtering steps are performed automatically by the Python program, so make sure to not edit the dataset before running the code.

---

## 7. Step-by-Step Explanation of the Code

### Step 1 – Import the libraries

The first step of the script is done by importing the Python libraries required for the analysis:

```python
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f_oneway
```

* `pandas` is used to load and manipulate the dataset.
* `numpy` is used for numerical calculations.
* `matplotlib` is used to create graphs.
* `scipy.stats` provides the statistical tests.
* `Path` is used to work with the dataset file path.

---

### Step 2 – Load the dataset

The CSV file is loaded into a pandas DataFrame.

The script first checks whether the file exists. If the file cannot be found, an error message is displayed (file not found).

The data is then stored so that it can be filtered and analysed.

---

### Step 3 – Clean the data

The script checks the columns needed for the analysis and removes observations where the required information is missing, such as unfinished games or unavailable odd's.

This ensures that calculations involving betting odds and match scores can be performed correctly.

---

### Step 4 – Identify the winner and loser

For each match, the dataset provides the players and the match result.

The analysis treats:

```text
player_a = winner
player_b = loser
```

This allows the script to compare the bookmaker's prediction with the actual match result.

---

### Step 5 – Calculate bookmaker probabilities

The betting odds are converted into implied probabilities.

For decimal betting odds, the implied probability is calculated using:

```text
Probability = 1 / Odds
```

The script then compares the probabilities for the two players.

A larger difference means that the bookmaker had greater confidence in one player being the winner.

---

### Step 6 – Calculate bookmaker confidence

The difference between the bookmaker probabilities is used as the measure of **bookmaker confidence**.

For example, if the winner has an implied probability of 0.65 and the loser has an implied probability of 0.35:

```text
Probability difference = 0.65 - 0.35
                       = 0.30
```

A larger probability difference therefore represents a stronger bookmaker favourite as the player is expected to win by a more dominant victory

---

### Step 7 – Calculate match dominance

The script calculates the number of games won by each player from the match score.

The difference in games is then calculated:

```text
Game margin = games won by winner - games won by loser
```

For example, if the final score corresponds to:

```text
Winner: 6 + 6 + 6 = 18 games
Loser:  3 + 4 + 2 = 9 games
```

then:

```text
Game margin = 18 - 9 = 9
```

A larger game margin represents a more dominant victory.

---

### Step 8 – Create the analysis variables

After calculating the bookmaker probability difference and game margin, the script creates a cleaned dataset containing the variables required for the statistical analysis.

The two main variables are:

* **Probability difference** → bookmaker confidence
* **Game margin** → match dominance

These variables are then later used for the plots and statistical tests.

---

### Step 9 – Separate matches by bookmaker confidence

The script also separates matches into different groups according to bookmaker confidence.

This allows the analysis to compare matches where the bookmaker strongly favoured the eventual winner with matches where the bookmaker was less confident.

The analysis can therefore investigate whether stronger bookmaker favourites tend to win by larger margins.

---

### Step 10 – Calculate descriptive statistics

The script calculates summary statistics such as the mean values of the main variables.

For example, it calculates the average game margin for different bookmaker-confidence groups.

These values provide an overview of the data before performing statistical tests.

---

### Step 11 – Perform statistical testing

The script uses an **ANOVA (Analysis of Variance)** test to compare the game margins between the different bookmaker-confidence groups.

The purpose is to determine whether the differences in average game margin between groups are statistically significant, by comparing the means.

The resulting p-value is used to evaluate the statistical significance of the observed differences.

---

### Step 12 – Create the plots

The script creates visualisations to make the results easier to interpret.

The main plots include:

* A **boxplot**, which compares the distribution of game margins between different bookmaker-confidence groups.
* A **scatterplot**, which shows the relationship between bookmaker probability difference and game margin.

The scatterplot helps determine whether greater bookmaker confidence is associated with more dominant victories.

---

### Step 13 – Display the results

Finally, the script prints the calculated statistics and test results to the terminal.

The graphs are also displayed so that the relationship between bookmaker confidence and match dominance can be visually evaluated.

---

## 8. Main Variables

The main variables used in the analysis are:

| Variable               | Description                                               |
| ---------------------- | --------------------------------------------------------- |
| `player_a`             | Winner of the match                                       |
| `player_b`             | Loser of the match                                        |
| Betting odds           | Bookmaker odds for each player                            |
| Implied probability    | Probability calculated from betting odds                  |
| Probability difference | Difference between winner and loser implied probabilities |
| Game margin            | Difference in games won by the winner and loser           |

---

## 9. Reproducing the Results

To reproduce the results:

1. Download the original Kaggle dataset.
2. Keep the CSV file named `tennis_matches_2014_2025.csv`.
3. Place the CSV file in the same folder as `FinalProject.py`.
4. Install Python 3 and the required libraries.
5. Run `FinalProject.py`.
6. The data cleaning, calculations, statistical tests, and plots will be performed automatically.

As mentionned before, no manual modification of the dataset is required.

The results should be reproducible as long as the same dataset and the same version of the Python script are used.

---

## 10. Dataset Source

The dataset used in this project is:

**Tennis Results and Betting Odds 2014–2025**

Kaggle:
https://www.kaggle.com/datasets/alimoh89/tennis-results-and-betting-odds-20142025

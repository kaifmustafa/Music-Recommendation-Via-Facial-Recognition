import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("data/election_data.csv")

# Party-wise wins
party_wins = data[data['Winner'] == 1]['Party'].value_counts()

party_wins.plot(kind='bar')
plt.title("Party-wise Winning Count")
plt.xlabel("Party")
plt.ylabel("Wins")
plt.show()
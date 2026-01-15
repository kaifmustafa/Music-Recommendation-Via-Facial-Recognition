import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

data = pd.read_csv("data/election_data.csv")

le_state = LabelEncoder()
le_party = LabelEncoder()

data['State'] = le_state.fit_transform(data['State'])
data['Party'] = le_party.fit_transform(data['Party'])

X = data[['State', 'Party', 'Votes', 'Turnout']]
y = data['Winner']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

pickle.dump(model, open("election_model.pkl", "wb"))
pickle.dump(le_state, open("state_encoder.pkl", "wb"))
pickle.dump(le_party, open("party_encoder.pkl", "wb"))

print("Advanced model trained successfully")
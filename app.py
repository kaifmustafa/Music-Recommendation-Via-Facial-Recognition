from flask import Flask, request, render_template_string
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

model = pickle.load(open("election_model.pkl", "rb"))
state_encoder = pickle.load(open("state_encoder.pkl", "rb"))
party_encoder = pickle.load(open("party_encoder.pkl", "rb"))

data = pd.read_csv("data/election_data.csv")

html = """
<!DOCTYPE html>
<html>
<head>
<title>Election Prediction</title>
<style>
body {
    background: linear-gradient(to right, #141e30, #243b55);
    font-family: Arial;
}
.container {
    width: 420px;
    margin: 50px auto;
    background: white;
    padding: 25px;
    border-radius: 12px;
}
h2 { text-align:center; }
input, button {
    width:100%; padding:10px; margin-top:10px;
}
button {
    background:#243b55; color:white; border:none;
}
.result {
    margin-top:15px; padding:12px; text-align:center;
}
.win { background:#d4edda; }
.lose { background:#f8d7da; }
img {
    margin-top:20px;
    width:100%;
    border-radius:10px;
}
</style>
</head>

<body>
<div class="container">
<h2>🗳️ Election Prediction</h2>

<form method="post">
<input name="state" placeholder="State (Bihar)" required>
<input name="party" placeholder="Party (BJP)" required>
<input type="number" name="votes" placeholder="Votes" required>
<input type="number" name="voter_percentage" placeholder="Voter Percentage" required>
<button type="submit">Predict</button>
</form>

{% if result %}
<div class="result {{ css }}">{{ result }}</div>
<img src="data:image/png;base64,{{ graph }}">
{% endif %}

</div>
</body>
</html>
"""

def generate_graph():
    wins = data[data['Winner'] == 1]['Party'].value_counts()

    plt.figure()
    wins.plot(kind='bar')
    plt.title("Party-wise Winning Count")
    plt.xlabel("Party")
    plt.ylabel("Wins")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    img = base64.b64encode(buf.read()).decode("utf-8")
    return img

@app.route("/", methods=["GET", "POST"])
def predict():
    result = None
    css = ""
    graph = None

    if request.method == "POST":
        state = request.form["state"]
        party = request.form["party"]
        votes = int(request.form["votes"])
        voter_percentage = int(request.form["voter_percentage"])

        state_val = state_encoder.transform([state])[0]
        party_val = party_encoder.transform([party])[0]

        pred = model.predict([[state_val, party_val, votes, voter_percentage]])

        if pred[0] == 1:
            result = f"{party} party will WIN in {state} 🟢"
            css = "win"
        else:
            result = f"{party} party will LOSE in {state} 🔴"
            css = "lose"

        graph = generate_graph()

    return render_template_string(html, result=result, css=css, graph=graph)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

def recommend_songs(emotion):
    # Simple example with CSV
    songs_df = pd.read_csv("songs.csv")
    return songs_df[songs_df['emotion']==emotion].to_dict('records')

@app.route("/")
def index():
    # Read captured emotion
    try:
        with open("current_emotion.txt", "r") as f:
            emotion = f.read()
    except:
        emotion = "neutral"

    songs = recommend_songs(emotion)
    return render_template("index.html", emotion=emotion, songs=songs)

if __name__ == "__main__":
    app.run(debug=False)
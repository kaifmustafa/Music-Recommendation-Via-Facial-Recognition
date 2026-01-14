import pandas as pd

def recommend_songs(emotion):
    df = pd.read_csv("songs.csv")
    emotion = emotion.lower()

    result = df[df['emotion'] == emotion]

    if result.empty:
        return []

    return result[['song_name', 'artist', 'link']].to_dict(orient='records')
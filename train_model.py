from pathlib import Path
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

BASE = Path(__file__).parent
data_path = BASE / "data" / "messages.csv"
model_path = BASE / "models" / "message_model.pkl"

df = pd.read_csv(data_path)
df["text"] = df["text"].astype(str)
df["label"] = df["label"].astype(int)

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=1)),
    ("classifier", LogisticRegression(max_iter=1000))
])

pipeline.fit(df["text"], df["label"])

model_path.parent.mkdir(exist_ok=True)
with open(model_path, "wb") as f:
    pickle.dump(pipeline, f)

print(f"Model trained on {len(df)} examples.")
print(f"Saved to: {model_path}")

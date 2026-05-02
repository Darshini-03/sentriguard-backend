import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Sample dataset (you can expand later)
data = {
    "text": [
        "Earn money fast",
        "Pay registration fee",
        "No experience required job",
        "Click here to apply",
        "Interview scheduled tomorrow",
        "We reviewed your resume",
        "Join meeting for interview",
        "Job opportunity with salary"
    ],
    "label": [1,1,1,1,0,0,0,0]  # 1 = Fraud, 0 = Genuine
}

df = pd.DataFrame(data)

# Convert text → numbers
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["text"])
y = df["label"]

# Train model
model = MultinomialNB()
model.fit(X, y)

# Save model + vectorizer
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model trained and saved!")

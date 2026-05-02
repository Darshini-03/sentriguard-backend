from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Sample training data
texts = [
    "You got selected for job",
    "Congratulations, job offer",
    "Earn money fast",
    "Click here to win money",
    "Limited time offer",
    "We are hiring you",
    "Join our company job role",
    "Free money now"
]

labels = [1, 1, 0, 0, 0, 1, 1, 0]  # 1 = Genuine, 0 = Fraud

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)

def predict_message(message):
    X_test = vectorizer.transform([message])
    prediction = model.predict(X_test)[0]

    if prediction == 1:
        return "Genuine", 0.80
    else:
        return "Fraud", 0.90
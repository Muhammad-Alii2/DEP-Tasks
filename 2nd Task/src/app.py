from flask import Flask, request, render_template
import joblib
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# Initialize Flask app
app = Flask(__name__)

# Load pre-trained models
nb_pipeline = pd.read_pickle('../Output_files/nb_model.pkl')
svm_pipeline = pd.read_pickle('../Output_files/svm_model.pkl')

# Download stopwords and wordnet from NLTK
nltk.download('stopwords')
nltk.download('wordnet')


# Function to preprocess text data
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = "".join([char for char in text if char not in string.punctuation])  # Remove punctuation
    words = text.split()  # Split text into words
    words = [word for word in words if word not in stopwords.words('english')]  # Remove stopwords
    words = [nltk.stem.WordNetLemmatizer().lemmatize(word) for word in words]  # Apply lemmatizing
    return " ".join(words)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email_content = request.form['email_content']
        preprocessed_text = preprocess_text(email_content)

        # Predict using Naive Bayes model
        nb_prediction = nb_pipeline.predict([preprocessed_text])[0]
        nb_result = "Spam" if nb_prediction == 1 else "Ham"

        # Predict using SVM model
        svm_prediction = svm_pipeline.predict([preprocessed_text])[0]
        svm_result = "Spam" if svm_prediction == 1 else "Ham"

        return render_template('index.html', nb_result=nb_result, svm_result=svm_result)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

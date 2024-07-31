from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load the trained model and vectorizer from disk
vectorizer = pd.read_pickle('../Output_files/vectorizer.pkl')
model = pd.read_pickle('../Output_files/model.pkl')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    review = request.form['review']
    transformed_review = vectorizer.transform([review])
    prediction = model.predict(transformed_review)[0]
    result = 'Positive' if prediction == 1 else 'Negative'
    result_class = 'positive' if prediction == 1 else 'negative'
    return render_template('index.html', prediction_text='Review is {}'.format(result), result_class=result_class)


if __name__ == '__main__':
    app.run(debug=True)

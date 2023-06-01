import re
import nltk
import numpy as np
import pandas as pd
import json
from youtube_comment_scraper import YouTubeCommentScraper

nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences


class Evaluator:

    # Making the appropriate initializations
    def __init__(self):
        self.model = load_model("BiLSTM.hdf5")
        self.stop_words = set(stopwords.words('english'))
        self.w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        self.max_words = 5000
        self.tokenizer = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, num_words=self.max_words)
        #self.scraper = YouTubeCommentScraper()

        df = pd.read_csv('IMDB Dataset.csv', sep=',')
        self.tokenizer.fit_on_texts(df['review'])

    # Cleaning the text
    def clean_text(self, text):
        text = re.sub('<br />', ' ', text)
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
        text = re.sub(r'[^\w\s]+', ' ', text)
        text = re.sub(r'\n', ' ', text)
        text = text.lower()
        return str(text)

    # Lemmatizing the words
    def lemmatize_text(self, text):
        lemmatized = [self.lemmatizer.lemmatize(w) for w in self.w_tokenizer.tokenize(text)]
        return [w for w in lemmatized if w not in self.stop_words]

    # Wrapper method to prepare the text
    def preprocess_text(self, text):
        cleaned = self.clean_text(text)
        lemmatized = self.lemmatize_text(cleaned)
        sequence = self.tokenizer.texts_to_sequences(lemmatized)
        padded = pad_sequences(sequence)
        final = padded.astype(np.float32)
        return final, lemmatized

    # Making the prediction
    def predict(self, string):
        processed, lemmatized = self.preprocess_text(string)
        prediction = self.model.predict(processed)
        return prediction, lemmatized

    # Evaluate the prediction using the mean value
    def mean_eval(self, prediction):
        avg = prediction.mean(axis=0)

        if avg[0] > avg[1]:
            sentiment = "negative"
        elif avg[0] < avg[1]:
            sentiment = "positive"
        else:
            sentiment = "neutral"

        return sentiment, avg

    # Evaluate the prediction by counting the individual sentiments
    def count_eval(self, prediction):
        classified = []

        for item in prediction:
            if item[0] > item[1]:
                classified.append(0)
            else:
                classified.append(1)

        positive = sum(classified)
        negative = len(classified) - positive

        # Replacing the values with labels
        for i in range(len(classified)):
            if classified[i] == 0:
                classified[i] = "negative"
            else:
                classified[i] = "positive"

        if positive > negative:
            sentiment = "positive"
        elif positive < negative:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return sentiment, classified, positive, negative

    # Evaluate the prediction by keeping only the values above a certain threshold
    def threshold_eval(self, prediction, lemmatized):
        threshold = 0.6
        sorted_values = []
        words = []

        for i in range(len(prediction)):
            if prediction[i, 0] >= threshold or prediction[i, 1] >= threshold:
                sorted_values.append(prediction[i])
                words.append(lemmatized[i])

        # for item in prediction:
        #    if item[0] >= threshold or item[1] >= threshold:
        #        sorted_values.append(item)

        sorted_values = np.array(sorted_values)

        classified = []

        for item in sorted_values:
            if item[0] > item[1]:
                classified.append(0)
            else:
                classified.append(1)

        positive = sum(classified)
        negative = len(classified) - positive

        if positive > negative:
            class_sentiment = "positive"
        elif positive < negative:
            class_sentiment = "negative"
        else:
            class_sentiment = "neutral"

        for i in range(len(classified)):
            if classified[i] == 0:
                classified[i] = "negative"
            else:
                classified[i] = "positive"

        return class_sentiment, sorted_values, classified, words, positive, negative

    # Generic evaluation method
    def evaluate(self, text):
        prediction, lemmatized = self.predict(text)

        mean_evaluation, mean = self.mean_eval(prediction)
        count_evaluation, classified, positives, negatives = self.count_eval(prediction)
        # threshold_class_evaluation, threshold_predictions, threshold_classified, threshold_words, threshold_positives, threshold_negatives = self.threshold_eval(prediction, lemmatized)

        mean_response = {
            "words": lemmatized,
            "values": prediction.tolist(),
            "sentiment": mean_evaluation,
            "mean": mean.tolist()
        }

        count_response = {
            "words": lemmatized,
            "labels": classified,
            "positives": positives,
            "negatives": negatives,
            "sentiment": count_evaluation
        }

        """
        threshold_response = {
            "words": threshold_words,
            "values": threshold_predictions.tolist(),
            "labels": threshold_classified,
            "mean_sentiment": threshold_class_evaluation,
            "positives": threshold_positives,
            "negatives": threshold_negatives
        }
        """

        return [mean_response, count_response]

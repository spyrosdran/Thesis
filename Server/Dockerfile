FROM python:3.9

COPY ./requirements.txt requirements.txt
RUN pip install tensorflow
RUN pip install --upgrade -r ./requirements.txt

COPY app.py .
COPY evaluator.py .
COPY IMDB_Dataset.csv .
COPY LSTM.hdf5 .
COPY BiLSTM.hdf5 .

CMD ["flask", "run", "--host=0.0.0.0", "--port", "5000"]

# To run the container: docker run -p 5000:5000 sentiment-analysis

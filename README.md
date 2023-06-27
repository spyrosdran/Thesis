
## Sentiment Analysis with Neural Networks and Efficient and Distributed Training of Neural Networks

👉 This is my thesis about Sentiment Analysis models and distributed training with Tensorflow. In Thesis.pdf, *which is written in Greek*, you may also find how hardware accelerates the training of a model.

🤖 I have also created a server application, which you can use to play and experiment with the model. The client's folder contains an HTML file, that you can use to interact with the server.

👉 Follow the steps below, in order to build a docker container of the server. Use the container to easily start the server. Instructions below:

### Docker Container

To build a Docker Container for the server:

 - Open the server folder in your terminal
 - ```docker build -t sentiment-analysis .```
 - ```docker run -p 5000:5000 sentiment-analysis```
 - Open client's ```index.html``` and you' re ready


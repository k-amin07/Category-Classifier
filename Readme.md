# Chatbot
Uses NLP and machine learning to determine the service category required by the user.

## Requirements:
Install the following paackages from pip:

- numpy

- pandas

- sklearn

- stanza

## Usage:
Run `python3 ./http-server.py` to run the server. To initialize service for the first time, send a GET request to `localhost:4000/init`. This needs to be done once after the server has been started. It will automatically train the model with the available data. To retrain the model, send a GET request to `localhost:4000/train`.

After the service has been initialized, to classify a sentence, pass it as a query parameter to `localhost:4000/classify`. For example, `localhost:4000/classify?q="I need my grass cut"`. This will return the category in the response body.

## To Do:
- (Frontend) Input Sanitation: remove commas from input.
- (Frontend) Input sanitation: change input to lower case.

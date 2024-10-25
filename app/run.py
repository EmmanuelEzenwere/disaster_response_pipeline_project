import sys
import os


import json
import plotly
import joblib

import pandas as pd

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar, Scatter, Pie
from sqlalchemy import create_engine


# Set up project path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from models.train_classifier import StartingVerbExtractor


app = Flask(__name__)

def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

# load data
engine = create_engine('sqlite:///data/DisasterResponse.db')
df = pd.read_sql_table('cleandata', engine)

# load model
model = joblib.load("./models/classifier.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)
    print(df.groupby('genre'))
    print("\n")
    print(genre_counts)
    print("\n")
    print(df.groupby('genre').count())
    print("3\n")
    print("genre:", genre_counts, genre_names)
    
    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
        {
            'data': [
                Pie(
                    labels=genre_names,
                    values=genre_counts,
                    hoverinfo='label+percent',  # Display labels and percentages on hover
                    textinfo='label+percent',  # Display labels and percentages on the pie chart
                    marker=dict(colors=['gray', 'lightgreen', 'darkgreen']),  # Customize colors
                )
            ],
            'layout': {
                'title': 'Message Genre Distribution (Pie Chart)',
                'showlegend': True  # Show legend for the pie chart
            }
        },
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts,
                    marker=dict(
                    color='gray',  # Default color
                    line=dict(color='blue', width=2)  # Optional line around bars
                ),
                hoverinfo='text',
                hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>',  # Customize hover text
            )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre",
                    'tickangle': -80  # Rotate x-axis labels by 80 degrees
                }
            }
        },
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts,
                    marker=dict(color='gray')
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre",
                    'tickangle': -80  # Rotate x-axis labels by 80 degrees
                }
            }
        },
        {
            'data': [
                Scatter(
                    x=genre_names,
                    y=genre_counts,
                    marker=dict(color='gray')
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre",
                    'tickangle': -80  # Rotate x-axis labels by 80 degrees
                }
            }
        }
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 
    print(query)
    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()
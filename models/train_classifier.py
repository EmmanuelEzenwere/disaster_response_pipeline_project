import sys
import re
import sklearn

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

import nltk

# Download the stopwords
nltk.download('stopwords')

# Download the Punkt tokenizer model
nltk.download('punkt')

# Download the WordNet model
nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
stop_words = set(stopwords.words("english"))

from sqlalchemy import create_engine

print(stop_words)

def load_data(database_filepath):
    """
    Fetch cleaned data from an sqlite database and return as 
    pandas data frame.

    Args:
        database_filepath (string): relative filepath to the sqlite
        database file
    
    Returns:
        X (Pandas Data Frame): A pandas dataframe of the cleaned data 
        from the sqlite database.
        Y ():
        category_names ():
    """
    # Create a database connection using SQLAlchemy
    engine = create_engine("sqlite:///"+database_filepath)
    # Read the table into a data frame
    data_frame = pd.read_sql_table(table_name="CleanData", con=engine)
    # print("\n",list(data_frame.columns),"\n")
    x = data_frame["message"]
    y = data_frame.iloc[:, 4:]
    category_names = data_frame.columns[4:]
    return x, y, category_names


def tokenize(text, stop_words=None):
    """tokenize a text by normalizing, lemmatizing and removing stop words.
    Args:
        text (list): list of strings
        stop_words (set): a set of word strings for stop words.

    Returns:
        list: list of token strings.
    """
    if stop_words is None:
        stop_words = set(stopwords.words("english"))
    
    lemmatizer = WordNetLemmatizer()    
    
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    # Replace URLs with a placeholder and normalize case.
    normalized_text = re.sub(url_regex, ' ', text.lower())

    # Replace non-alphanumeric characters with spaces.
    normalized_text = re.sub(r'[^a-zA-Z0-9]', ' ', normalized_text)
    
    tokens = word_tokenize(normalized_text)
    
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    
    return tokens


def build_model():
    """_summary_
    """
    # Define the pipeline steps.
    pipe = Pipeline()
    return pipeline

    # Fit the pipeline to the training data.
    
    
    # Predict using the pipeline.

def evaluate_model(model, X_test, Y_test, category_names):
    """_summary_

    Args:
        model (_type_): _description_
        X_test (_type_): _description_
        Y_test (_type_): _description_
        category_names (_type_): _description_
    """
    train_test_split
    return None


def save_model(model, model_filepath):
    """_summary_

    Args:
        model (_type_): _description_
        model_filepath (_type_): _description_
    """
    return None


def main():
    """_summary_
    """
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()



from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
def display_results(y_test, y_pred):
    labels = np.unique(y_pred)
    confusion_mat = confusion_matrix(y_test, y_pred, labels=labels)
    accuracy = (y_pred == y_test).mean()
    print("Labels:", labels)
    print("Confusion Matrix:\n", confusion_mat)
    print("Accuracy:", accuracy)


# def load_data():
#     """ 
#     """
#     df = pd.read_csv('corporate_messaging.csv', encoding='latin-1')
#     df = df[(df["category:confidence"] == 1) & (df['category'] != 'Exclude')]
#     X = df.text.values
#     y = df.category.values
#     return X, y


# def tokenize(text):
#     """_summary_

#     Args:
#         text (_type_): _description_

#     Returns:
#         _type_: _description_
#     """
#     detected_urls = re.findall(url_regex, text)
#     for url in detected_urls:
#         text = text.replace(url, "urlplaceholder")

#     tokens = word_tokenize(text)
#     lemmatizer = WordNetLemmatizer()

#     clean_tokens = []
#     for tok in tokens:
#         clean_tok = lemmatizer.lemmatize(tok).lower().strip()
#         clean_tokens.append(clean_tok)

#     return clean_tokens


# def model_pipeline():
#     """
#     creates a pipleline which contains a feature union (text_verb_union) of 
#     a transformer and the output of another pipeline.
#     by appending a boolean of if the text is a verb or not to the last column
#     of the tfidf matrix of the text.


#     """
    
#     text_processing_pipeline = Pipeline([
#                 ('vect', CountVectorizer(tokenizer=tokenize)),
#                 ('tfidf', TfidfTransformer())
#             ])
    
    
#     text_verb_union = FeatureUnion([

#             ('text_pipeline', text_processing_pipeline),
#             ('starting_verb', StartingVerbExtractor())
#         ])
    
    
#     pipeline = Pipeline([
#         ('features', text_verb_union),
#         ('clf', RandomForestClassifier())
#     ])

#     return pipeline


# def display_results(y_test, y_pred):
#     """_summary_

#     Args:
#         y_test (_type_): _description_
#         y_pred (_type_): _description_
#     """
#     labels = np.unique(y_pred)
#     confusion_mat = confusion_matrix(y_test, y_pred, labels=labels)
#     accuracy = (y_pred == y_test).mean()

#     print("Labels:", labels)
#     print("Confusion Matrix:\n", confusion_mat)
#     print("Accuracy:", accuracy)


# def main():
#     """_summary_
#     """
#     X, y = load_data()
#     X_train, X_test, y_train, y_test = train_test_split(X, y)

#     model = model_pipeline()
#     model.fit(X_train, y_train)
#     y_pred = model.predict(X_test)

#     display_results(y_test, y_pred)

# main()
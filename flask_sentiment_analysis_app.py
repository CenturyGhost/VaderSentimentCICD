import pandas as pd
from flask import Flask, render_template, request, session
from pandas.io.json import json_normalize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# We use vader for sentiment analysis
def vaderAnalysis(dataframe):
    # we use Vader's sentiment analyzer
    SentimentIntensityObject = SentimentIntensityAnalyzer()

    # We then calculate polarity that gives a sentiment dictionary
    # It contains pos, neg, neu, compound score
    sentiment_list = []
    for row_num in range(len(dataframe)):
        sentenceAnalysis = dataframe['Text'][row_num]

        polarity_dict = SentimentIntensityObject.polarity_scores(sentenceAnalysis)

        # Calculate overall sentiment by compound score
        if polarity_dict['compound'] >= 0.05:
            sentiment_list.append("Positive")

        elif polarity_dict['compound'] <= - 0.05:
            sentiment_list.append("Negative")

        else:
            sentiment_list.append("Neutral")

    dataframe['Sentiment'] = sentiment_list

    return dataframe


# We then provide the template name

app = Flask(__name__, template_folder='templateFiles')

#the secret key
app.secret_key = 'You Will Never Guess'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        uploaded_file = request.files['uploaded-file']
        df = pd.read_csv(uploaded_file)
        session['uploaded_csv_file'] = df.to_json()
        return render_template('index2.html')


@app.route('/show_data')
def showData():
    # A json value gets uploaded as a session
    uploaded_json = session.get('uploaded_csv_file', None)
    # Convert json to data frame
    uploaded_df = pd.DataFrame.from_dict(eval(uploaded_json))
    # We finally convert DF to HTML format in order to show a beautiful website :)
    UploadedDfToHTML = uploaded_df.to_html()
    return render_template('show_data.html', data=UploadedDfToHTML)


@app.route('/sentiment')
def SentimentAnalysis():
    # Get uploaded csv file from session as a json value
    uploaded_json = session.get('uploaded_csv_file', None)
    # Convert json to data frame
    uploaded_df = pd.DataFrame.from_dict(eval(uploaded_json))
    # Apply sentiment function to get sentiment score
    uploaded_df_sentiment = vaderAnalysis(uploaded_df)
    #transform it in html form
    UploadedDfToHTML = uploaded_df_sentiment.to_html()
    return render_template('show_data.html', data=UploadedDfToHTML)

#r"ngreognrognaer??nig
if __name__ == '__main__':
    app.run(debug=True)

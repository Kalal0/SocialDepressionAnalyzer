import snscrape.modules.twitter as sntwitter
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import pickle
from pickle import load
import plotly.express as px
from jupyter_dash import JupyterDash
from dash import html
from dash import dcc
#import dash
from dash.dependencies import Input, Output
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


# Created a list to append all tweet attributes(data)
attributes_container = []
# Using TwitterSearchScraper to scrape data and append tweets to list
for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:elonmusk').get_items()):
    if i >= 1000:
        break
    attributes_container.append(
        [tweet.user, tweet.date, tweet.likeCount, tweet.content])

# Creating a dataframe from the tweets list above
tweets_df = pd.DataFrame(attributes_container, columns=[
                         "User", "Date_Created", "Number_of_Likes", "Tweets"])


model = tf.keras.models.load_model('model.h5')
vectorizer = load(open('tokenizer.pkl', 'rb'))


TweetsToProcess = tweets_df['Tweets']

 #Apply scaler to data
x_test = pad_sequences(vectorizer.texts_to_sequences(TweetsToProcess), maxlen=300)

score = model.predict(x_test)

tweets_df["Predictions_Percentange"]=score

tweets_df["Predictions"] = np.where(
    tweets_df["Predictions_Percentange"] >= 0.5, "Depression", "Non-Depression")


tweets_df['year'] = tweets_df['Date_Created'].dt.year


# Creating the month column form date time stamp.

tweets_df['month'] = tweets_df['Date_Created'].dt.month


# Creating the day column form date time stamp.

tweets_df['day'] = tweets_df['Date_Created'].dt.day


# Creating the hour column form date time stamp.

tweets_df['hour'] = tweets_df['Date_Created'].dt.hour


midnight_df = tweets_df.query("hour <= 5")


########################### DASH #############################

#################### Figure 1 ###########################
# Create figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(x=list(tweets_df.Date_Created), y=list(tweets_df.Predictions)))


# Set title
fig.update_layout(
    title_text="Depression Tweets by Time"
)

# Add range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7,
                     label="1w",
                     step="day",
                     stepmode="backward"),
                dict(count=14,
                     label="2w",
                     step="day",
                     stepmode="backward"),
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=3,
                     label="3m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

#################### Figure 2 ###########################


fig2 = px.bar(tweets_df, x="Predictions",
              color='month', title="Depression count")


#################### Figure 3 ###########################

fig3 = go.Figure()

fig3 = px.scatter(tweets_df, x="day", y="hour",
                  size="Predictions_Percentange", color="Predictions",
                  hover_name="Tweets", log_x=True, size_max=60)


#################### Figure 4 ###########################

fig4 = px.pie(tweets_df, values='Number_of_Likes',
              names='Predictions', title='The tweets behavior')

###################### End of Figures ##################

app = JupyterDash(__name__)
app.layout = html.Div([
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4)
])

if __name__ == '__main__':
    app.run_server(debug=True)

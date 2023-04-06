# Food-Sentiment
Web app that tells you what people are feeling about certain food items from the YelpAPI.

While reading reviews from the business, you might notice that the ratings don't match with the sentiment analysis. That's because an rating number tells one side of the story, but the sentiments of users tell another.

## How it works

Type inputs for the food item and location you want to search and the app will return a table showing the information about each business (specially the sentiment analysis). User can click on the name of the business and it will take them to a page showing the analyzed reviews with the sentiment score of each.

## Video Walkthrough/Example

![Walkthrough](walkthrough.gif)

## Built With

* [Yelp Fusion API](https://www.yelp.com/developers/documentation/v3) - Used to collect data
* [Flask](http://flask.pocoo.org/) - Web development framework for Python
* [Pygal](https://www.pygal.org/en/stable/) - "Sexy" Python Charting
* [TextBlob](https://textblob.readthedocs.io/en/dev/) - Text processing/Sentiment Analysis


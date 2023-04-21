import os
import json
from flask import Flask, render_template, request, session
from modules.Business import GatherBusinesses, Business
from modules.Graphs import Graph


app = Flask(__name__)
app.secret_key = os.urandom(24)

SEARCH = {'term': None, 'location': None}
BUSINESSES = []
GRAPHS = None
LOAD_FROM_CACHE = False
CACHE_FILE = 'cache.json'
CACHE = {}


@app.before_request
def setup():
    global BUSINESSES, SEARCH
    if 'user' not in session:
        SEARCH = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    global BUSINESSES, CACHE
    # Store session of user
    session['user'] = 'user'

    if request.method == 'POST' and \
            request.form['term'] != '' and \
            request.form['location'] != '':

        # Get search inputs
        SEARCH['term'] = request.form['term']
        SEARCH['location'] = request.form['location']
        # Get businesses
        analyze_businesses()

    if BUSINESSES != [] and SEARCH != {}:
        top = get_top()
        return render_template('index.html', search=True,
                               topsent=top[0],
                               toprating=top[1],
                               businesses=BUSINESSES,
                               rchart=GRAPHS.rating_bar,
                               schart=GRAPHS.sentiment_bar,
                               srchart=GRAPHS.comparison_bar,
                               location=SEARCH['location'], term=SEARCH['term'],
                               cache=LOAD_FROM_CACHE)
    else:
        return render_template('index.html')


@app.route('/reviews/<bid>')
def business(bid):
    print('\n\nBusinesses:', BUSINESSES)
    for b in BUSINESSES:
        if bid == b.id:
            return render_template('routing/business.html',
                                   business=b)


def analyze_businesses():
    global BUSINESSES, LOAD_FROM_CACHE
    term, location = SEARCH['term'], SEARCH['location']
    cache_key = f'{term.lower()}+{location.lower()}'

    if cache_key in CACHE:
        BUSINESSES = load_businesses_from_cache(cache_key)
        LOAD_FROM_CACHE = True
    else:
        businesses = GatherBusinesses(term, location)
        save_to_cache(cache_key, businesses.business_list)
        BUSINESSES = load_businesses_from_cache(cache_key)
        LOAD_FROM_CACHE = False

    get_charts(BUSINESSES)


def save_to_cache(cache_key, businesses):
    global CACHE
    CACHE[cache_key] = businesses
    for key, bs in CACHE.items():
        for i in range(len(bs)):
            business = bs[i]
            if isinstance(business, Business):
                business.reviews = [r.__dict__ for r in business.reviews]
                bs[i] = business.__dict__
    with open(CACHE_FILE, 'w') as f:
        json.dump(CACHE, f, indent=4)


def get_top():
    global BUSINESSES
    tops, topr = None, None
    s, r = 0, 0
    for b in BUSINESSES:
        if float(b.sentiment_score) > s:
            s = float(b.sentiment_score)
            tops = b
        if float(b.rating) > r:
            r = float(b.rating)
            topr = b
    return [tops, topr]


def get_charts(businesses):
    global GRAPHS
    GRAPHS = Graph(businesses)


def load_businesses_from_cache(cache_key):
    global CACHE
    businesses = CACHE[cache_key]
    for i in range(len(businesses)):
        business = businesses[i]
        if isinstance(business, dict):
            businesses[i] = Business(business)
    return businesses


def load_cache():
    global CACHE
    try:
        with open(CACHE_FILE, 'r') as f:
            cache_data = f.read()
            if not cache_data:
                CACHE = {}
            else:
                CACHE = json.loads(cache_data)
    except FileNotFoundError:
        CACHE = {}


if __name__ == '__main__':
    load_cache()
    app.run(debug=True)

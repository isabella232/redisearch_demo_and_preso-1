from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from redisearch import AutoCompleter, Suggestion
import json
import redis
import csv

app = Flask(__name__)
bootstrap = Bootstrap()


nav = Nav()
topbar = Navbar('',
    View('Home', 'index'),
)
nav.register_element('top', topbar)

def load_data():
   ac = AutoCompleter('ac')
   with open('./fortune500.csv') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
      line_count = 0
      for row in csv_reader:
         if line_count > 0:
            ac.add_suggestions(Suggestion(row[1].replace('"', ''),  1.0))
         line_count += 1

@app.route('/')
def index():
   r = redis.Redis()
   print(len(r.keys('ac')))
   if len(r.keys('ac')) < 1:
       load_data()
   return render_template('search.html')

@app.route('/autocomplete')
def auto_complete():
    ac = AutoCompleter('ac')
    name = request.args.get('term')
    suggest = ac.get_suggestions(name, fuzzy = True)
    return(json.dumps([{'value': item.string, 'label': item.string, 'id': item.string, 'score': item.score} for item in suggest]))


if __name__ == '__main__':
   bootstrap.init_app(app)
   nav.init_app(app)
   app.run()

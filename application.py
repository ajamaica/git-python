from flask import Flask
import requests
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
	search_term = request.args.get('search_term')
	url = 'https://api.github.com/search/repositories?sort=updated&q=%s' % (search_term)
	r = requests.get(url)
	return '%s' % r.json()

if __name__ == '__main__':
    app.run(host='localhost', port=9876)
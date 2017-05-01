from flask import Flask
import requests
app = Flask(__name__)


@app.route('/')
def hello_world():
	url = 'https://api.github.com/search/repositories?q=%s' % ("")
	r = requests.get(url)
	return '%s' % r.json()

if __name__ == '__main__':
    app.run(host='localhost', port=9876)
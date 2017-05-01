from flask import Flask,request,render_template
import requests
from dateutil.parser import parse
app = Flask(__name__)

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = parse(date)
    native = date.replace(tzinfo=None)
    format='%b %d, %Y %H:%m'
    return native.strftime(format)

@app.route('/')
def hello_world():
	search_term = request.args.get('search_term')
	url = 'https://api.github.com/search/repositories?sort=updated&q=%s' % (search_term)
	r = requests.get(url)
	response = r.json()
	items = response["items"]
	return render_template('template.html', search_term=search_term, items = items)

if __name__ == '__main__':
    app.run(host='localhost', port=9876)
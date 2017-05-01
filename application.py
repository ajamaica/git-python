from flask import Flask,request,render_template
import requests
import grequests
from dateutil.parser import parse
app = Flask(__name__)

GIT_APP_ID = "8026cd45f19bb07baa4b"
GIT_APP_SECRET = "a6adcb6bfede3e5750a2cb5717eb91359d025cba"

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = parse(date)
    native = date.replace(tzinfo=None)
    format='%b %d, %Y %H:%m'
    return native.strftime(format)

@app.route('/navigator')
def hello_world():
	search_term = request.args.get('search_term')
	url_git = 'https://api.github.com/search/repositories'
	
	payload_git = {"sort" : "updated", "order" : "desc",
	 			"q" : search_term,"client_id": GIT_APP_ID, 
				"client_secret": GIT_APP_SECRET }
	
	r = requests.get(url_git,payload_git)
	response = r.json()
	items = response["items"]
	
	urls_commits = []
	for repo in items:
		urls_commits.append("https://api.github.com/repos/%s/commits?client_id=%s&client_secret=%s" % (repo["full_name"],GIT_APP_ID ,GIT_APP_SECRET))
		
	rs = [grequests.get(u) for u in urls_commits]
	all_res = grequests.map(rs)
	all_commits = [{"sha" : u.json()[0]["sha"], "commit" : u.json()[0]["commit"] } for u in all_res]
		
	return render_template('template.html', search_term=search_term, items = items,all_commits = all_commits)

if __name__ == '__main__':
    app.run(host='localhost', port=9876)
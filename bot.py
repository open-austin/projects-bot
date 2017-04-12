import requests
import json
from datetime import datetime

# Build lists of issues with no updates for more than 14 and 30 days
dateformat = '%Y-%m-%dT%H:%M:%S'
now = datetime.strptime(datetime.utcnow().strftime(dateformat), dateformat)
url = 'https://api.github.com/repos/open-austin/project-ideas/issues'
request = requests.get(url)
issues14 = {}
issues30 = {}
lastPage = request.links['last']['url']
numPages = int(lastPage[len(lastPage) - 1])
for i in range(numPages):
    pageNum = str(i+1)
    issues = requests.get(url + '?page=' + pageNum).json()
    for i in range(len(issues)):
        issue = issues[i]
        updated_at = issue['updated_at'].replace('Z', '')
        then = datetime.strptime(updated_at, dateformat)
        daysSince = (now - then).days
        number = issue['number']
        if daysSince > 30:
            issues30[number] = issue
        elif daysSince > 14:
            issues14[number] = issue

# TODO: set actions here
print len(issues30)
print len(issues14)

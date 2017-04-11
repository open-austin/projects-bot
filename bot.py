import requests
import json
from datetime import datetime

dateformat = '%Y-%m-%dT%H:%M:%S'
now = datetime.strptime(datetime.utcnow().strftime(dateformat), dateformat)
url = 'https://api.github.com/repos/open-austin/project-ideas/issues'
issues = requests.get(url).json()
issues14 = {}
issues30 = {}

# Build arrays of older issues
for i in range(len(issues)):
    issue = issues[i]
    then = datetime.strptime(issue['updated_at'].replace('Z', ''), dateformat)
    daysSince = (now - then).days
    if daysSince > 30:
        issues30.append(issue)
    elif daysSince > 14:
        issues14.append(issue)

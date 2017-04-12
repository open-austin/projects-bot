import requests
import json
from datetime import datetime

# Build lists of non-abandoned issues with no updates for > 14 days
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
        abandoned = False
        for i in range(len(issue['labels'])):
            label = issue['labels'][i]
            if 'Abandoned and needs love' == label['name']:
                abandoned = True
                break
        if abandoned:
            continue
        updated_at = issue['updated_at'].replace('Z', '')
        then = datetime.strptime(updated_at, dateformat)
        daysSince = (now - then).days
        number = issue['number']
        if daysSince > 30:
            issues30[number] = issue
        elif daysSince > 14:
            issues14[number] = issue

# TODO: set actions here
reply = 'Hi, could someone please post an update (even if it\'s just \'still working\') on this project idea? If we don\'t hear back in two weeks we will assume this project has been abandoned.'
for issueNum in issues14.keys():
    print 'reply to issue #' + str(issueNum)

for issueNum in issues30.keys():
    print 'add abandon label to issue #' + str(issueNum)

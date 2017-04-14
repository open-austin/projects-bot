import requests
import json
import os
import sys
from datetime import datetime

# Important stuff
test = 'test' in sys.argv
abandonedLabel = 'Abandoned and needs love'
url = 'https://api.github.com/repos/open-austin/project-ideas/issues'
headers = {'Authorization': 'token ' + os.environ['GITHUB_TOKEN']}
issues14 = {}
issues30 = {}
updateComment = 'Hello, we\'re the Open Austin Project Team. We\'ve noticed there hasn\'t been any activity on this thread for the past two weeks. Can you post an update, however small, on any recent activity or if help is needed in any way? If more time passes without an update, we will label this idea as "Abandoned and needs love".'

# Build lists of non-abandoned issues with no updates
dateformat = '%Y-%m-%dT%H:%M:%S'
now = datetime.strptime(datetime.utcnow().strftime(dateformat), dateformat)
request = requests.get(url, headers = headers)
lastPage = request.links['last']['url']
numPages = int(lastPage[len(lastPage) - 1])
for i in range(numPages):
    pageNum = str(i+1)
    issues = requests.get(url + '?page=' + pageNum, headers = headers).json()
    for i in range(len(issues)):
        issue = issues[i]
        abandoned = False
        labels = []
        for i in range(len(issue['labels'])):
            label = issue['labels'][i]
            labels.append(label['name'])
            if abandonedLabel == label['name']:
                abandoned = True
                break
        if not abandoned:
            commentsUrl = issue['comments_url']
            comments = requests.get(commentsUrl, headers = headers).json()
            numComments = len(comments)
            lastUpdated = issue['updated_at'].replace('Z', '')
            if numComments > 0:
                lastComment = comments[numComments-1]['body']
                if lastComment == updateComment:
                    if numComments > 1:
                        nextToLastComment = comments[numComments-2]
                        lastUpdated = nextToLastComment['updated_at'].replace('Z', '')
                    else:
                        lastUpdated = issue['created_at'].replace('Z', '')
            then = datetime.strptime(lastUpdated, dateformat)
            daysSince = (now - then).days
            number = issue['number']
            if daysSince > 30:
                issues30[number] = {'number': number, 'labels': labels}
            elif daysSince > 14:
                issues14[number] = {'number': number, 'labels': labels}


# Reply to 14-day old issues asking for updates
for issueNum in issues14.keys():
    if test:
        print ('reply to issue #' + str(issueNum))
    else:
        endpoint = url + '/' + str(issueNum) + '/comments'
        r = requests.post(endpoint, json = {'body': updateComment}, headers = headers)

# Add abandoned label to 30-day old isues
for issueNum in issues30.keys():
    if test:
        print ('add abandon label to issue #' + str(issueNum))
    else:
        endpoint = url + '/' + str(issueNum)
        newLabels = issues30[issueNum]['labels'][:]
        newLabels.append(abandonedLabel)
        r = requests.post(endpoint, json = {'labels': newLabels}, headers = headers)

# An Example of Calling the API
List=['i was feeling as heartbroken ','i am feeling outraged ','aweome']

import requests
for i in range(len(List)):
	query = {'text':str(List[i])}
	response = requests.get('https://detect-emotionapi.herokuapp.com/sentiment_analysis/', params=query)
	print(response.json())




import sys
import requests
import json

username = sys.argv[1]

url = 'https://api.discogs.com/users/%s/collection/folders/0/releases' % username
queue = [url]

while len(queue):
	url = queue.pop(0)
	response = requests.get(url, headers={'user-agent': 'pomle/discogs-uris'})
	releases = json.loads(response.text)

	if 'next' in releases['pagination']['urls']:
		queue.append(releases['pagination']['urls']['next'])

	for release in releases['releases']:
		title = release['basic_information']['title']
		artists = []
		for artist in release['basic_information']['artists']:
			 artists.append(artist['name'])
		lookup = title + " " + " ".join(artists)

		response = requests.get('https://api.spotify.com/v1/search', params={'q': lookup, 'type': 'album'})
		results = json.loads(response.text)

		if len(results['albums']['items']):
			print results['albums']['items'][0]['uri'], release['instance_id'], lookup
		else:
			print >> sys.stderr, "%s not found :(" % lookup

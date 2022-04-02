from googleapiclient.discovery import build
from bisect import bisect_left
import time
import sys


if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <playlist_url_1> <playlist_url_2>")
    sys.exit()

start_time = time.time()

api_key = ''
youtube = build('youtube', 'v3', developerKey=api_key)

playlist1 = sys.argv[1]
playlist2 = sys.argv[2]
# Are there videos in playlist1 that are not in playlist2?

p1_list = []
p2_list = []

nextPageToken = None
while True:
    p1_request = youtube.playlistItems().list(part='snippet',
                                              playlistId=playlist1,
                                              maxResults=50,
                                              pageToken=nextPageToken)
    p1_response = p1_request.execute()

    for item in p1_response['items']:
        url = item['snippet']['resourceId']['videoId']
        title = item['snippet']['title']
        position = item['snippet']['position']
        p1_list.append([url, title, position])

    nextPageToken = p1_response.get('nextPageToken')
    if not nextPageToken:
        break

nextPageToken = None
while True:
    p2_request = youtube.playlistItems().list(part='snippet',
                                              playlistId=playlist2,
                                              maxResults=50,
                                              pageToken=nextPageToken)
    p2_response = p2_request.execute()

    p1_title = p2_response
    for item in p2_response['items']:
        url = item['snippet']['resourceId']['videoId']
        # title = item['snippet']['title']
        # position = item['snippet']['position']
        # p2_list.append([url, title, position])
        p2_list.append(url)

    nextPageToken = p2_response.get('nextPageToken')
    if not nextPageToken:
        break

# p2_list.sort(key=lambda vid: vid[0])
# p2_list.sort()
missing = []


# Binary search
"""def binarySearch(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        return -1


for vid in p1_list:
    if -1 == binarySearch(p2_list, vid[0]):
        missing.append(vid)"""

# Linear search
for vid in p1_list:
    found = False
    for i in p2_list:
        if vid[0] == i:
            found = True
            break
    if not found:
        missing.append(vid)

for vid in missing:
    print(vid)

playlist_request = youtube.playlists().list(part='snippet', id=f"{playlist1}, {playlist2}")
playlist_response = playlist_request.execute()
playlist1_title = playlist_response['items'][0]['snippet']['title']
playlist2_title = playlist_response['items'][1]['snippet']['title']
print(f"There are {len(missing)} videos in {playlist1_title} that are not in {playlist2_title}")

youtube.close()

print("time elapsed: {:.2f}s".format(time.time() - start_time))

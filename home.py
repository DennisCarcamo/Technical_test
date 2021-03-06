import webapp2

import os
import urllib

import jinja2

from apiclient.discovery import build
from optparse import OptionParser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

# Set DEVELOPER_KEY to the "API key" value from the Google Developers Console:
# https://console.developers.google.com/project/_/apiui/credential
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBTMxrCShVl5iJgN1YBZ76ScdZM9u8sUl0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class MainHandler(webapp2.RequestHandler):
   
   def get(self):
      youtube = build(
        YOUTUBE_API_SERVICE_NAME, 
        YOUTUBE_API_VERSION, 
        developerKey=DEVELOPER_KEY)
      search_response = youtube.search().list(
        q="Hello",
        part="id,snippet",
        maxResults=5
      ).execute()
        
      videos = []
      channels = []
      playlists = []

      for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"], 
              search_result["id"]["videoId"]))
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"], 
              search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"], 
              search_result["id"]["playlistId"]))

      template_values = {
       'videos': videos,
       'channels': channels,
       'playlists': playlists
      }
    
      print(template_values)

      self.response.headers['Content-type'] = 'text/plain' 
      template = JINJA_ENVIRONMENT.get_template('index.html')
      self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
  ('/.*', MainHandler),
], debug=True)
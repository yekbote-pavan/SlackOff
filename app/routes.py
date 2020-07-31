from slack import WebClient
from slack.errors import SlackApiError
from flask import Flask, jsonify, request, render_template
from app import app
import uuid
from string import Template

HTML_TEMPLATE = Template("""
      <h2>
        YouTube video link: 
        <a href="{youtube_link}">
        </a>
      </h2>
      <iframe src="${youtube_link}" width="853" height="480" frameborder="0" allowfullscreen></iframe>""")

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

UI_URL = "http://ee9f283d3026.ngrok.io/"


@app.route('/', methods=['GET', 'POST', 'PUT'])
def index():
    if request.method == 'GET':
        return index_get()
    if request.method == 'POST':
        print("request form: " + str(request.form))
        print(str(request.view_args))
        print(request.__dict__.keys())
        return index_post(request.data)


@app.route('/interaction', methods=['POST'])
def interaction_api():
    return interaction()


def index_get():
    return HTML_TEMPLATE.substitute(youtube_link='https://www.youtube.com/embed/dQw4w9WgXcQ')


def index_post(data):
    print('data: ' + str(data))
    new_id = uuid.uuid4()
    url = "https://www.youtube.com/watch?v=n4OerfEyTJ4"
    youtube_id = get_youtube_id_from_url(url)
    if not youtube_id[0]:
        return youtube_id[1]
    url_main = UI_URL + "yt=" + youtube_id[1] + "?room=" + str(new_id)
    return {
        "text": "You have created a room at " + url_main
    }


def interaction():
    return None


def youtube_to_embed_url(url):
    parts = url.split('v=')
    if len(parts) < 2:
        return "Invalid Link"
    return 'https://www.youtube.com/embed/' + url


def get_youtube_id_from_url(url):
    parts = url.split('v=')
    if len(parts) < 2:
        return False, "Invalid Link"
    return True, parts[1]
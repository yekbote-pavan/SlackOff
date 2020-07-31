import json

from slack import WebClient
from slack.errors import SlackApiError
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO

from app import app
import uuid
from string import Template
import requests
from datetime import datetime

HTML_TEMPLATE = Template("""
      <h2>
        YouTube video link: 
        <a href="{youtube_link}">
        </a>
      </h2>
      <iframe src="${youtube_link}" width="853" height="480" frameborder="0" allowfullscreen></iframe>""")

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

UI_URL = "http://648741fcb9fd.ngrok.io"


@app.route('/', methods=['GET', 'POST', 'PUT'])
def index():
    if request.method == 'GET':
        return index_get(request.args)
    if request.method == 'POST':
        return index_post(request.data)


@app.route('/interaction', methods=['POST'])
def interaction_api():
    return interaction()


def index_get(qps):
    yt = qps.get('yt')
    return HTML_TEMPLATE.substitute(youtube_link='https://www.youtube.com/embed/' + yt)


def index_post(data):
    # print('data: ' + str(data))
    new_id = uuid.uuid4()

    url = process_args(request.form.get('text'))
    youtube_id = get_youtube_id_from_url(url)
    if not youtube_id[0]:
        return youtube_id[1]

    thumnail_url = get_thumbnail_for_link(youtube_id[1])
    url_main = UI_URL + "?yt=" + youtube_id[1] + "&room=" + str(new_id)
    print(url_main)
    payload = {
        "attachments": [
            {
              "fallback": "Hello there!",
              "color": "#FF0000",
              "author_name": "Bored?",
              "title": "Watch a youtube video together",
              "title_link": url_main,
              "thumb_url": thumnail_url,
              "footer": "A hevothon product",
              "footer_icon": "https://media-exp1.licdn.com/dms/image/C510BAQF1N15Og6uyRA/company-logo_200_200/0?e=2159024400&v=beta&t=P-OsHCRn6K_hgidBEZIiMNrmusSUnLalM4O2MXJR8P4",
               "ts": datetime.now().timestamp()
            }
        ]
    }
    headers = {
        'Content-type': 'application/json'
    }

    requests.request("POST", SLACK_WEBHOOK_URL, headers=headers, data=str(payload))
    return {
        "text": "You have created a room at " + url_main
    }


def process_args(args):
    return args


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


def get_thumbnail_for_link(yid):
    # https: // img.youtube.com / vi / oHg5SJYRHA0 / default.jpg
    return "https://img.youtube.com/vi/" + yid + "/default.jpg"

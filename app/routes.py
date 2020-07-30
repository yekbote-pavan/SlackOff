from flask import Flask, request, render_template
from app import app


SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return index_get()
    if request.method == 'POST':
        print(request)
        return index_post(request.data)


def index_get():
    return "<b>Hello, World!</b>"


def index_post(data):
    return str(data)

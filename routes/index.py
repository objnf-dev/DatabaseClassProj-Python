from flask import Flask, session, request, render_template
from app import app

@app.route('/')
def index():
    dom = render_template('index.html')
    return dom
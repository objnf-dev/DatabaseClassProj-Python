from flask import Flask, session, request, render_template, redirect
from . import routes
from utils import database


@routes.route('/')
def index():
    dom = render_template('index.html')
    return dom

@routes.route('/login')
def login():
    dom = render_template('login.html')
    return dom


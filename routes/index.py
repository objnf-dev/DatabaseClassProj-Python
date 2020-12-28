from flask import Flask, session, request, render_template, redirect
from . import routes
import os

@routes.route('/')
def index():
    if not os.path.exists('install.lock'):
        return redirect('/install')
    else:
        dom = render_template('index.html')
        return dom

@routes.route('/install')
def installSystem():
    return render_template('install.html')

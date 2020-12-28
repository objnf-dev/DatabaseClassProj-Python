from flask import Flask, session, request, render_template, redirect
from . import routes
import os

@routes.route('/')
def index():
    dom = render_template('index.html')
    return dom


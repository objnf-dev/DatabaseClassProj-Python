from flask import Flask, session, request, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = b'Fzr2lfT#I^x%2NgD80S!fK&oxvf@rU3R'


@app.route('/')
def index():
    dom = render_template('index.html')
    return dom



if __name__ == '__main__':
    app.run(port = 9999)
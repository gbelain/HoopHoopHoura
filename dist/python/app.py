# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, redirect, url_for
from ball_tracking import processVideo

# Initialize the Flask application
app = Flask(__name__)
videoName = ""
# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation


@app.route('/')
def index():
    return render_template('index.html')

# Route that will process the AJAX request, sum up two
# integer numbers (defaulted to zero) and return the
# result as a proper JSON response (Content-Type, etc.)


@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


@app.route('/_process_video')
def process_video():
    a, b = processVideo(videoName)
    return jsonify(result="le resultat final est " +
                   str(a) + " tirs effectués et " + str(b) + " tir reussis")

# sur requete AJAX _get_message on renvoie le texte
# je suis la réponse ajax du serveur à + le paramètre transmis


@app.route('/_get_message')
def get_message():
    param = request.args.get('param', 'pas de param', type=str)
    return jsonify(result='je suis la réponse ajax du serveur à ' + param)


@app.route('/', methods=['POST'])
def upload_file():
    global videoName
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        videoName = str(uploaded_file.filename)
        uploaded_file.save(uploaded_file.filename)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(
        debug=True
    )

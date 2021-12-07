from flask import Flask, jsonify, request, g, redirect, url_for, Response
import logging
from application_services import PostUserService
import uuid

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

# -------------------- authentication --------------------
import requests
from flask_cors import CORS
from context import API_GATEWAY_URL
CORS(app)

@app.before_request
def before_request():

    # verify id_token
    id_token = request.headers.get('id_token')
    url = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
    response = requests.get(url)
    user_data = response.json()
    email = user_data.get('email')

    # if not verified, return message
    if not email:
        response = Response("Please provide a valid google id_token!", status=200)
        return response

    # if verified
    url = f"{API_GATEWAY_URL}/api/users?email={email}"
    headers = {'id_token': id_token}
    response = requests.get(url, headers=headers)
    result = response.json()

    # check if user exist
    if len(result) == 0:
        url = f"{API_GATEWAY_URL}/api/users"
        user_id = str(uuid.uuid4())
        template = {
            'user_id': user_id,
            'first_name': user_data['given_name'],
            'last_name': user_data['family_name'],
            'nickname': user_data['email'],
            'email': user_data['email'],
        }
        response = requests.post(url, data=template, headers=headers)
    else:
        user_id = result[0]['user_id']

    g.user_id = user_id
    g.email = email

@app.route('/')
def home():
    return '<u>composite micro service for E6156 project!</u>'


@app.route('/api/postinfo', methods=['GET'])
def get_all_posts():
    id_token = request.headers.get('id_token')
    params = request.args
    sort_by = params.get('sortby', None)
    offset = params.get('offset', None)
    limit = params.get('limit', None)
    headers = {'id_token': id_token}
    res = PostUserService.get_all_posts(headers, offset, limit, sort_by)
    return jsonify(res), res['code']


# data includes title and content
@app.route('/api/postinfo', methods=['POST'])
def create_post():
    data = request.get_json()
    user_id = g.user_id
    id_token = request.headers.get('id_token')
    headers = {'id_token': id_token}
    res = PostUserService.create_post(user_id, data, headers=headers)
    post_id = data['post_id']
    response = jsonify(res)
    response.headers.set('Location', f"/api/postinfo/{post_id}")
    response.headers.add('Access-Control-Expose-Headers', 'Location')
    return response, res['code']


@app.route('/api/postinfo/<post_id>', methods=['GET'])
def get_post(post_id):
    user_id = g.user_id
    id_token = request.headers.get('id_token')
    headers = {'id_token': id_token}
    res = PostUserService.get_post_detail(user_id, post_id, headers=headers)
    return jsonify(res), res['code']


@app.route('/api/postinfo/<post_id>', methods=['PUT'])
def put_post(post_id):
    data = request.get_json()
    user_id = g.user_id
    id_token = request.headers.get('id_token')
    headers = {'id_token': id_token}
    res = PostUserService.update_post_detail(user_id, post_id, data, headers=headers)
    return jsonify(res), res['code']


@app.route('/api/userprofile/<user_id>', methods=['GET'])
def get_user(user_id):
    id_token = request.headers.get('id_token')
    headers = {'id_token': id_token}
    res = PostUserService.get_user_profile(user_id, headers)
    return jsonify(res), res['code']


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, jsonify, request, g
from flask_cors import CORS
import logging
from application_services import PostUserService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return '<u>composite micro service for E6156 project!</u>'


@app.route('/api/postinfo', methods=['GET'])
def get_all_posts():
    res = PostUserService.get_all_posts(cookies=request.cookies)
    return jsonify(res), res['code']


# data includes title and content
@app.route('/api/postinfo', methods=['POST'])
def create_post():
    # TODO: get from session cookie
    # user_id = g.user_id
    data = request.get_json()
    user_id = '1f6e0895-3899-42d7-a738-6a9fd72cc6a0'
    res = PostUserService.create_post(user_id, data, cookies=request.cookies)
    return jsonify(res), res['code']


@app.route('/api/postinfo/<post_id>', methods=['GET'])
def get_post(post_id):
    # TODO: get from session cookie
    # user_id = g.user_id
    user_id = 123
    res = PostUserService.get_post_detail(user_id, post_id, cookies=request.cookies)
    return jsonify(res), res['code']


@app.route('/api/postinfo/<post_id>', methods=['PUT'])
def put_post(post_id):
    data = request.get_json()
    # TODO: get from session cookie
    # user_id = g.user_id
    user_id = '1f6e0895-3899-42d7-a738-6a9fd72cc6a0'
    res = PostUserService.update_post_detail(user_id, post_id, data, cookies=request.cookies)
    return jsonify(res), res['code']


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

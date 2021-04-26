import flask
from flask import jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from . import encoding_args

class Ceasar(Resource):
    def get(self):
        pass

    def post(self):
        args = encoding_args.parser.parse_args()

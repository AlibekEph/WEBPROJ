from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('text', required=True)
parser.add_argument('key', required=True)


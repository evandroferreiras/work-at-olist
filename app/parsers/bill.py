from flask_restplus import reqparse

bill_get_parser = reqparse.RequestParser()
bill_get_parser.add_argument('subscriber', type=str)
bill_get_parser.add_argument('period', type=str)

from flask_restful import reqparse

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username",
                          type=str,
                          required=False,
                          help="This field can not be blank!"
                          )
_user_parser.add_argument("password",
                          type=str,
                          required=True,
                          help="This field can not be blank!"
                          )
_user_parser.add_argument("userrole",
                          type=int,
                          required=False,
                          help="This field must be 0 for simple user or more for admin!"
                          )

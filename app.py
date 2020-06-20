from flask import Flask
# from flask_restful import Resource, Api
import redis

app = Flask(__name__)
# api = Api(app)

r = redis.Redis(host='localhost', db=2, encoding="utf-8", decode_responses=True)

@app.route('/')
def index():
    # if r.keys():
    #     return r.keys()
    return "hello world!"

# class Proxy(Resource):
#     def get(self):
#         return r.keys("*")

# api.add_resource(Proxy, '/proxy.json')

if __name__ == '__main__':
    app.run()

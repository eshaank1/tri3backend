from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from __init__ import db
from model.datascholarsearch import Data

data_bp = Blueprint("data", __name__)
data_api = Api(data_bp)

class DataAPI(Resource):
    def get(self):
        id = request.args.get("id")
        data = db.session.query(Data).get(id)
        if data:
            return data.to_dict()
        return {"message": "not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("city", type=str)
        parser.add_argument("state", type=str)
        parser.add_argument("zip", type=str)
        parser.add_argument("school_url", type=str)
        parser.add_argument("admission_rate", type=str)
        parser.add_argument("average_sat", type=str)
        parser.add_argument("address", type=str)
        parser.add_argument("tuition_in_state", type=str)
        parser.add_argument("tuition_out_of_state", type=str)
        args = parser.parse_args()
        data = Data(args["name"], args["city"], args["state"], args["zip"],
                    args["school_url"], args["admission_rate"],
                    args["average_sat"], args["address"],
                    args["tuition_in_state"], args["tuition_out_of_state"])

        try:
            db.session.add(data)
            db.session.commit()
            return data.to_dict(), 201
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        parser.add_argument("name", type=str)
        parser.add_argument("city", type=str)
        parser.add_argument("state", type=str)
        parser.add_argument("zip", type=str)
        parser.add_argument("school_url", type=str)
        parser.add_argument("admission_rate", type=str)
        parser.add_argument("average_sat", type=str)
        parser.add_argument("address", type=str)
        parser.add_argument("tuition_in_state", type=str)
        parser.add_argument("tuition_out_of_state", type=str)
        args = parser.parse_args()

        try:
            data = db.session.query(Data).get(args["id"])
            if data:
                if args["name"] is not None:
                    data.name = args["name"]
                if args["city"] is not None:
                    data.city = args["city"]
                if args["state"] is not None:
                    data.state = args["state"]
                if args["zip"] is not None:
                    data.zip = args["zip"]
                if args["school_url"] is not None:
                    data.school_url = args["school_url"]
                if args["admission_rate"] is not None:
                    data.admission_rate = args["admission_rate"]
                if args["average_sat"] is not None:
                    data.average_sat = args["average_sat"]
                if args["address"] is not None:
                    data.address = args["address"]
                if args["tuition_in_state"] is not None:
                    data.tuition_in_state = args["tuition_in_state"]
                if args["tuition_out_of_state"] is not None:
                    data.tuition_out_of_state = args["tuition_out_of_state"]
                db.session.commit()
                return data.to_dict(), 200
            else:
                return {"message": "not found"}, 404
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        args = parser.parse_args()

        try:
            data = db.session.query(Data).get(args["id"])
            if data:
                db.session.delete(data)
                db.session.commit()
                return data.to_dict()
            else:
                return {"message": "not found"}, 404
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500


class DataListAPI(Resource):
    def get(self):
        data = db.session.query(Data).all()
        return [d.to_dict() for d in data]


data_api.add_resource(DataAPI, "/data")
data_api.add_resource(DataListAPI, "/dataList")

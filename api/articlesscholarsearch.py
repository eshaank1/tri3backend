from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from model.articlesscholarsearch import db
from model.articlesscholarsearch import Article

Article_bp = Blueprint("Article", __name__, url_prefix='/articles')
Article_api = Api(Article_bp)


class ArticleAPI(Resource):
    def get(self):
        id = request.args.get("id")
        data = db.session.query(Article).get(id)
        if data:
            return data.to_dict()
        return {"message": "not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str)
        parser.add_argument("author", type=str)
        parser.add_argument("link", type=str)
        args = parser.parse_args()
        data = Article(args["title"], args["author"], args["link"])

        try:
            db.session.add(data)  # Fix: Use `data` instead of `Article`
            db.session.commit()
            return data.to_dict(), 201
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        args = parser.parse_args()

        try:
            data = db.session.query(Article).get(args["id"])
            if data:
                db.session.delete(data)
                db.session.commit()
                return data.to_dict()
            else:
                return {"message": "not found"}, 404
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500


class ArticleListAPI(Resource):
    def get(self):
        articles = db.session.query(Article).all()
        return [article.to_dict() for article in articles]
        # Fix: Use `articles` instead of `article`


Article_api.add_resource(ArticleAPI, "/articles")
# Fix: Add a leading slash ("/articles")
Article_api.add_resource(ArticleListAPI, "/articlesList")

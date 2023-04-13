#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Research, Author, ResearchAuthors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)


class Index(Resource):
    def get(self):
        response = make_response({
            'message': "Welcome Authors"
        }, 200)
        return response


api.add_resource(Index, '/')

class AllResearch(Resource):
    def get(self):
        all_research = Research.query.all()
        dict_researches = []
        for research in all_research:
            dict_researches.append(research.to_dict())
        return make_response(dict_researches,200)
api.add_resource(AllResearch, '/research')

class ResearchById(Resource):
    def get(self, id):
        single_research = Research.query.filter_by(id=id).first()
        if single_research:
            return make_response(single_research.to_dict(), 200)
        else:
            return make_response({"error":"Research paper not found"}, 404)
    def delete(self, id):
        research = Research.query.filter_by(id=id).first()
        if research:
            all_research_authors = ResearchAuthors.query.filter_by(id = id).all()
            db.session.delete(research)
            for research in all_research_authors:
                db.session.delete(research)
            db.session.commit()
            return make_response({},200)
        else:
            return make_response({"error": "Research paper not found"},400)

api.add_resource(ResearchById, '/research/<int:id>')

# class 
class AllAuthor(Resource):
    def get(self):
        all_Author = Author.query.all()
        dict_Author = []
        for author in all_Author:
            dict_Author.append(author.to_dict(only=('id','name','field_of_study')))
        return make_response(dict_Author,200)
    def post(self):
        input = request.get_json()
        new_author = Author(name = input["name"], field_of_study = input["field_of_study"])
        db.session.add(new_author)
        db.session.commit()
api.add_resource(AllAuthor, '/author')

class AddRA(Resource):
    def post(self):
        try:
            input = request.get_json()
            new_researchauthor = ResearchAuthors(research_id = input["research_id"], author_id = input["author_id"])
            db.session.add(new_researchauthor)
            db.session.commit()
            return make_response(new_researchauthor.authors.to_dict(only=('id','name','field_of_study')),201)
        except:
            return make_response({
                "errors": ["validation errors"]
            },400)
api.add_resource(AddRA, '/researchauthors')

if __name__ == '__main__':
    app.run(port=5554, debug=True)

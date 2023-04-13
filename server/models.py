from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Research(db.Model,SerializerMixin):
    __tablename__ = 'researches'
    id = db.Column(db.Integer, primary_key = True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    research_Authors = db.relationship("ResearchAuthors", backref="research_paper")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    serialize_rules = ('-research_Authors.research_paper','-created_at','-updated_at')

    @validates('year')
    def year_validate(self,key,year):
        if len(str(year)) == 4:
            return year
        else:
            raise Exception("Not valid year")
    
class Author(db.Model,SerializerMixin):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    research_Authors = db.relationship("ResearchAuthors", backref="authors")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    serialize_rules = ('-research_Authors.authors','-created_at','-updated_at',)

    @validates('field_of_study')
    def in_list(self,key,fos):
        all = ["AI", "Robotics", "Machine Learning", "Vision", "Cybersecurity"]
        if fos in all:
            return fos
        else:
            raise Exception("Not valid field")
    
class ResearchAuthors(db.Model,SerializerMixin):
    __tablename__ = "research_Authors"
    id = db.Column(db.Integer, primary_key = True)
    research_id = db.Column(db.Integer, db.ForeignKey('researches.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    serialize_rules = ('-authors.research_Authors','-research_paper.research_Authors','-created_at','-updated_at',)
# Add models here
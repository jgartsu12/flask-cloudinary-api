from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import marshmallow_sqlalchemy
import cloudinary as Cloud
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    public_id = db.Column(db.String(200), nullable=False)

    def __init__(self, title, image_url, public_id):
        self.title = title
        self.image_url = image_url
        self.public_id = public_id

class ImageSchema(ma.Schema):
    class Meta: 
        fields = ("id", "title", "image_url", "public_id")

image_schema = ImageSchema()
images_schema = ImageSchema(many=True)

@app.route('/')
def phlog_uploader():
    return "Upload Your Images"

if __name__ == "__main__":
    app.debug = True
    app.run()
    
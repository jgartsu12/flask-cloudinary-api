from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
# import marshmallow_sqlalchemy
import cloudinary as Cloud
import os

Cloud.config.update = ({
    'cloud_name': os.environ.get('CLOUNDINARY_CLOUD_NAME'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUNDINARY_API_SECRET')
})

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

# CRUD methods
@app.route('/')
def phlog_uploader():
    return "Upload Your Images"

# add image to api
@app.route("/api/v1/image", methods=["POST"])
def add_image():
    title = request.json["title"]
    image_url = request.json["image_url"]
    public_id = request.json["public_id"]

    new_image = Image(title, image_url, public_id)

    db.session.add(new_image)
    db.session.commit()

    image = Image.query.get(new_image.id)
    return image_schema.jsonify(image)

@app.route("/api/v1/images", methods=["GET"])
def get_images():
    all_images = Image.query.all()
    result = images_schema.dump(all_images)

    return jsonify(result)

@app.route("/api/v1/image/<id>", methods=["DELETE"])
def delete_image(id):
    image = Image.query.get(id)
    db.session.delete(image)
    db.session.commit()
    Cloud.api.delete_resources([image.public_id])

    return jsonify("Phlog deleted!")

if __name__ == "__main__":
    app.debug = True
    app.run()
    
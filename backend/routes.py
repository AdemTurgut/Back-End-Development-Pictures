from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200
            
    return jsonify({"message": "picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # İstek gövdesinden (request body) gelen JSON verisini alıyoruz
    picture_in = request.json
    
    # Gönderilen id'nin data listesinde olup olmadığını kontrol ediyoruz
    for picture in data:
        if picture["id"] == picture_in["id"]:
            # Eğer id zaten varsa 302 durumuyla birlikte hata mesajını döndürüyoruz
            return jsonify({"Message": f"picture with id {picture_in['id']} already present"}), 302
            
    # Eğer id listede yoksa, yeni resmi veri listesine ekliyoruz
    data.append(picture_in)
    
    # Başarıyla eklendiğini belirtmek için 201 koduyla resmi geri döndürüyoruz
    return jsonify(picture_in), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture_in = request.json
    
    for picture in data:
        if picture["id"] == id:
            picture.update(picture_in)
            
            return jsonify(picture), 200
            
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # data listesindeki resimleri ve indekslerini (sıra numaralarını) alıyoruz
    for i, picture in enumerate(data):
        if picture["id"] == id:
            # Resim bulunduysa, o indeksteki resmi listeden siliyoruz
            del data[i]
            
            # Başarılı silme işlemi için boş bir içerik ("") ve 204 kodunu döndürüyoruz
            return "", 204
            
    # Eğer döngü biter ve resim bulunamazsa 404 hata mesajı döndürüyoruz
    return jsonify({"message": "picture not found"}), 404

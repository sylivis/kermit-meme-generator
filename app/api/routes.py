
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import da_meme, da_memes, db, User, Empty_Template, da_templates, da_template, Meme

api = Blueprint('apy', __name__, url_prefix='/api')

@api.route('/newtemplate', methods = ['post'])
@token_required
def add_template(current_user_token):
    filename = request.json['filename']
    user_token = current_user_token.token

    new_template = Empty_Template(filename, user_token)

    db.session.add(new_template)
    db.session.commit()

    response = da_meme.dump(new_template)
    return jsonify(response)


@api.route('/newmeme', methods = ['post'])
@token_required
def new_meme(current_user_token):
    caption = request.json['caption']
    image_id = request.json['image_id']
    user_token = current_user_token.token

    meme = Meme(image_id, caption, user_token)

    db.session.add(meme)
    db.session.commit()

    response = da_meme.dump(meme)
    return jsonify(response)

@api.route('/seealltemplates', methods = ['GET'])
@token_required
def see_templates(current_user_tokern):
    u = current_user_tokern.token
    data = Empty_Template.query.filter_by(user_token = u).all()
    response = da_templates.dump(data)
    return jsonify(response)
    
@api.route('/seemymemes', methods = ['GET'])
@token_required
def see_my_memes(current_user_tokern):
    u = current_user_tokern.token
    data = Meme.query.filter_by(user_token = u).all()
    response = da_memes.dump(data)
    return jsonify(response)

@api.route('/seemymeme/<id>', methods = ['GET'])
@token_required
def see_meme(current_user_token, id):
    meme = Meme.query.get(id)
    response = da_meme.dump(meme)
    return jsonify(response)

@api.route('/deletememe/<id>', methods = ['DELETE'])
@token_required
def delete_meme(current_user_token, id):
    meme = Meme.query.get(id)
    db.session.delete(meme)
    db.session.commit()
    response = da_meme.dump(meme)
    return jsonify(response)


@api.route('/deletetemplate/<id>', methods = ['delete'])
@token_required
def delete_contact(current_user_token, id):
    template = Empty_Template.query.get(id)
    db.session.delete(template)
    db.session.commit()
    response = da_template.dump(template)
    return jsonify(response)


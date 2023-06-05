from ..model import Url_link
from flask_restx import Resource,abort
from ..schema import url_namespace,url_short
from ..helper import url
import random
from ..model import Url_link,User
from flask_jwt_extended import jwt_required,get_jwt_identity
from sqlalchemy import and_
from flask import redirect

@url_namespace.route("/shorten")
class Url_Shorten(Resource):
    @url_namespace.marshal_with(url_short)
    @url_namespace.expect(url_short)
    @jwt_required()
    def post(self):
        data=url_namespace.payload
        user_id=get_jwt_identity()
        
        if url.is_valid_url(data.get("long_url")):
            if Url_link.query.filter(Url_link.long_url==data.get("long_url"),Url_link.user_id==user_id).first():
                abort(400,message='this url has been shortened by you ')

            number_suffix=random.randint(100,999)
            letter_suffix=random.sample(url.alphabet,3)
            string_letter_suffix="".join(letter_suffix)
            custom_backhalf=data.get("custom_backhalf")
            if custom_backhalf  is None:
                 short_url=f"dar.zy/{number_suffix}{string_letter_suffix}"
                 new_url=Url_link(short_url=short_url,long_url=data.get("long_url"),user_id=user_id)
            if  Url_link.query.filter(Url_link.custom_backhalf==custom_backhalf,Url_link.user_id==user_id).first():
                abort(400,message='this custom backhalf has been used by you ')
            else:
                short_url=f"dar.zy/{custom_backhalf}"
                new_url=Url_link(short_url=short_url,long_url=data.get("long_url"),user_id=user_id,custom_backhalf=custom_backhalf)

           
            
            new_url.save()
            return new_url,201            
        abort(400,message='The url link is not valid')
@url_namespace.route("")
class Url_short(Resource):
     @url_namespace.marshal_with(url_short)
     @jwt_required()
     def get(self):
         user_id=get_jwt_identity()
         user=User.query.get_or_404(user_id)
         links=Url_link.query.filter(Url_link.user_id==user_id).all()
         return links,200


        
@url_namespace.route("/remove/<id>")
class Url_shortDel(Resource):
    def delete(self,id):
        url=Url_link.query.get_or_404(id)
        url.delete()
        return {"message":"url has been successfully deleted"}
    

@url_namespace.route("/<short-url>")
class Url_Shortened(Resource):
    def get(self,short_url):
        url=Url_link.query.filter(Url_link.short_url==short_url).first()
        if url:
         return redirect(url.long_url, code=302)
        else:
            return "Short URL not found", 404



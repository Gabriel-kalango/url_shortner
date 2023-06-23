from ..model import Url_link
from flask_restx import Resource,abort
from ..schema import url_namespace,url_short
from ..helper import url
import random
from ..model import Url_link,User
from flask_jwt_extended import jwt_required,get_jwt_identity
from sqlalchemy import and_
from flask import redirect,send_file
import qrcode
from ..utils import cache,db
import os

import uuid


@url_namespace.route("/shorten")
class Url_Shorten(Resource):
    @url_namespace.marshal_with(url_short)
    @url_namespace.expect(url_short)
    @jwt_required()
    def post(self):
        '''endpoint for shortening of url'''
        data=url_namespace.payload
        user_id=get_jwt_identity()
        #check if the long url has already be shortened 
        if url.is_valid_url(data.get("long_url")):
            if Url_link.query.filter(Url_link.long_url==data.get("long_url"),Url_link.user_id==user_id).first():
                abort(400,message='this url has been shortened by you ')

            number_suffix=random.randint(100,999)
            letter_suffix=random.sample(url.alphabet,3)
            string_letter_suffix="".join(letter_suffix)
            custom_backhalf=data.get("custom_backhalf")
            if custom_backhalf is not None:
                if Url_link.query.filter(Url_link.custom_backhalf==custom_backhalf,Url_link.user_id==user_id).first():
                
                    abort(400,message='this custom backhalf has been used by you ')
                short_url=f"{custom_backhalf}"
                new_url=Url_link(short_url=short_url,long_url=data.get("long_url"),user_id=user_id,custom_backhalf=custom_backhalf)
                 
                 
          
            else:
                short_url=f"{number_suffix}{string_letter_suffix}"
                new_url=Url_link(short_url=short_url,long_url=data.get("long_url"),user_id=user_id)
               

           
            
            new_url.save()
            return new_url,201            
        abort(400,message='The url link is not valid')
@url_namespace.route("")
class Url_short(Resource):
     @url_namespace.marshal_with(url_short)
     @jwt_required()
     @cache.cached(timeout=3600)
     def get(self):
         '''get all the links shortened by a particular user'''
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
    

@url_namespace.route("/<short_url>")
class Url_Shortened(Resource):
    @cache.memoize(timeout=3600)
    def get(self,short_url):
        url=Url_link.query.filter(Url_link.short_url==short_url).first()

        if url:
            url.click+=1
            db.session.commit()
            return redirect(url.long_url, code=302)
        else:
            return "Short URL not found", 404

@url_namespace.route("/<short_url>/qrcode")
class Url_qrcode(Resource):
    @jwt_required()
    def post(self,short_url):
        """Get the QR code for a long url"""
        link = Url_link.query.filter(Url_link.short_url==short_url).first_or_404()
        if not link.qrcode_filename:
            # If the QR code hasn't been generated yet, generate it now
            # Generate a unique filename
            filename = str(uuid.uuid4()) + '.png'

            # Generate the QR code image
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(link.long_url)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            current_dir = os.getcwd()
            save_directory = os.path.join(current_dir, 'API', 'static', 'qr_codes')
            os.makedirs(save_directory, exist_ok=True)

            
            
            
            save_path = os.path.join(save_directory, filename)
            
        
            
            qr_img.save(save_path)
            link.qrcode_filename=filename
            
            db.session.commit()
            return {"message":"your qrcode has been uploaded"}
        abort(400,message="the qrcode filename is  saved in the database")   
        
    @jwt_required()
    def get(self, short_url):
        """Get the QR code image for a long URL"""
        link = Url_link.query.filter(Url_link.short_url == short_url).first_or_404()
        try:
            # get the current working directory
            current_dir = os.getcwd()


            
            
            qr_file_path=f"API\static\qr_codes\{link.qrcode_filename}"
            file_path_=os.path.join(current_dir,qr_file_path)
            absolute_path=os.path.abspath(file_path_)
            print(absolute_path)
        
            return send_file(absolute_path)

   

        except FileNotFoundError:
            abort(404,message=f"file not found ")
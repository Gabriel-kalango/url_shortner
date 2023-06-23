from ..utils import db
from datetime import datetime
class Url_link(db.Model):
        __tablename__="url_links"
        id=db.Column(db.Integer,primary_key=True)
        short_url=db.Column(db.String(50),nullable=False,unique=True)
        long_url=db.Column(db.String(250),nullable=False)
        custom_backhalf=db.Column(db.String(250),default="")
        qrcode_filename=db.Column(db.String(250))
        click=db.Column(db.Integer,default=0)
        date_posted=db.Column(db.DateTime,default=datetime.utcnow)
        user_id=db.Column(db.Integer,db.ForeignKey("users.id"))

        def save(self):
                db.session.add(self)
                db.session.commit()
    
        def update(self):
                db.session.commit() 

        def delete(self):
                db.session.delete(self)
                db.session.commit()

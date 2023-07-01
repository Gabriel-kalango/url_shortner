from flask_restx import fields,Namespace
url_namespace=Namespace("link",description="operations on the url")
url_short=url_namespace.model("url_short",{
    "id":fields.Integer(dump_only=True),
    "short_url":fields.String(),
    "long_url":fields.String(required=True),
    "custom_backhalf":fields.String(),
    "click":fields.Integer(),
    "date_posted":fields.DateTime(description="time it was posted",dt_format='rfc822'),
    "qrcode_filename":fields.String(description="the filename for the qrcode")
})
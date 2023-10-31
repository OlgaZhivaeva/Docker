import flask
import pydantic
from flask import jsonify, request
from flask.views import MethodView

import schema
from models import Session, Advertisement

app = flask.Flask("app")

def validate(validation_schema, validation_data):
    try:
        model = validation_schema(**validation_data)
        return model.dict(exclude_none=True)
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())

class HttpError(Exception):
    def __init__(self, status_code: int, message: str | dict | list):
        self.status_code = status_code
        self.message = message

@app.errorhandler(HttpError)
def error_handler(er: HttpError):
    response = jsonify({"status": "error", "description": er.message})
    response.status_code = er.status_code
    return response

def get_adv(session, adv_id):
    adv = session.get(Advertisement, adv_id)
    if adv is None:
        raise HttpError(404, f"Объявления с идентификатором {adv_id} не существует")
    return adv

class AdvView(MethodView):
    def get(self, adv_id):
        with Session() as session:
            adv = get_adv(session, adv_id)
            return jsonify(
                {
                    "id": adv.id,
                    "heading": adv.heading,
                    "description": adv.description,
                    "creator": adv.creator,
                    "creation_time": adv.creation_time.isoformat()
                }
            )

    def post(self):
        validated_json = validate(schema.CreateAdv, request.json)
        with Session() as session:
            adv = Advertisement(**validated_json)
            session.add(adv)
            session.commit()
            return jsonify(
                {
                    "id": adv.id,
                    "heading": adv.heading,
                    "description": adv.description,
                    "creator": adv.creator,
                    "creation_time": adv.creation_time.isoformat()
                }
            )

    def patch(self, adv_id):
        validated_json = validate(schema.UpdateAdv, request.json)
        with Session() as session:
            adv = get_adv(session, adv_id)
            for field, value in validated_json.items():
                setattr(adv, field, value)
            session.add(adv)
            session.commit()
            return jsonify(
                {
                    "id": adv.id,
                    "heading": adv.heading,
                    "description": adv.description,
                    "creator": adv.creator,
                    "creation_time": adv.creation_time.isoformat()
                }
            )

    def delete(self, adv_id):
        with Session() as session:
            adv = get_adv(session, adv_id)
            session.delete(adv)
            session.commit()
            return jsonify({"status": "Объявление удалено"})


adv_view = AdvView.as_view('adv')
app.add_url_rule(rule='/adv/<int:adv_id>',
                 view_func=adv_view,
                 methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule(rule='/adv/',
                 view_func=adv_view,
                 methods=['POST'])
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
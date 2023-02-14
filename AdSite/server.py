from datetime import datetime
from errors import HttpException
from flask import Flask, request, jsonify
from flask.views import MethodView
from db import Advertisement, Session, Owner
from schema import validate_create_ad, validate_create_owner

app = Flask('app')


@app.errorhandler(HttpException)
def error_handler(error: HttpException):
    http_response = jsonify({
        'status': 'error',
        'description': error.message
    })
    http_response.status_code = error.status_code
    return http_response


def get_owner(owner_id: int, session: Session):
    owner = session.query(Owner).get(owner_id)
    if owner is None:
        raise HttpException(status_code=404, message='Owner not found')
    return owner


def get_ad(ad_id: int, session: Session):
    ad = session.query(Advertisement).get(ad_id)
    if ad is None:
        raise HttpException(status_code=404, message='Advertisement not found')
    return ad


class OwnerView(MethodView):
    def get(self, owner_id: int):
        with Session() as session:
            owner = get_owner(owner_id, session)
            return jsonify({
                 'id': owner.id,
                 'name': owner.name
                })

    def post(self):
        json_data = validate_create_owner(request.json)
        with Session() as session:
            new_owner = Owner(**json_data)
            session.add(new_owner)
            session.commit()
            return jsonify(
                {'id': new_owner.id,
                 'name': new_owner.name
                 }
            )


class AdSiteView(MethodView):

    def get(self, ad_id: int):
        with Session() as session:
            ad = get_ad(ad_id, session)
            return jsonify({
                'id': ad.id,
                'title': ad.title,
                'description': ad.description,
                'owner_id': ad.id
            })

    def post(self):
        json_data = validate_create_ad(request.json)
        query_string_data = request.args
        print(query_string_data)
        with Session() as session:
            new_ad = Advertisement(**json_data)
            session.add(new_ad)
            session.commit()
            date = datetime.utcfromtimestamp(new_ad.creation_date.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
            return jsonify(
                {'id': new_ad.id,
                 'title': new_ad.title,
                 'description': new_ad.description,
                 'creation_date': date,
                 'owner_id': new_ad.id
                 }
            )

    def patch(self, ad_id: int):
        adv_data = request.json
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with Session() as session:
            adv = session.query(Advertisement).get(ad_id)
            for field, value in adv_data.items():
                setattr(adv, field, value)
            session.add(adv)
            session.commit()
            return jsonify({
                'id': adv.id,
                'title': adv.title,
                'description': adv.description,
                'creation_date': date,
                'owner_id': adv.id,
            })

    def delete(self, ad_id: int):
        with Session() as session:
            adv = session.query(Advertisement).get(ad_id)
            session.delete(adv)
            session.commit()
            return jsonify({
                'advertisements': 'deleted'
            })


app.add_url_rule('/advertisements/<int:ad_id>',
                 view_func=AdSiteView.as_view('advertisement'),
                 methods=['GET', 'PATCH', 'DELETE']
                 )

app.add_url_rule('/advertisements',
                 view_func=AdSiteView.as_view('new_advertisement'),
                 methods=['POST']
                 )

app.add_url_rule('/owners/<int:owner_id>',
                 view_func=OwnerView.as_view('owner'),
                 methods=['GET', 'PATCH', 'DELETE']
                 )

app.add_url_rule('/owners',
                 view_func=OwnerView.as_view('new_owner'),
                 methods=['POST']
                 )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

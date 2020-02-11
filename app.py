from flask import Flask
from flask_restful import Api, Resource, reqparse
import service.db

# g.db = service.db.DataBase(user='debian-sys-maint',
#                            password='PggWbsvEVgDZUYar',
#                            host='127.0.0.1',
#                            database='ordtick')
app = Flask(__name__)
api = Api(app)
HOST = 'http://127.0.0.1:5000'


parser = reqparse.RequestParser()
parser.add_argument('event_id')
parser.add_argument('event_name')
parser.add_argument('event_date')
parser.add_argument('event_place')
parser.add_argument('event_ta')
parser.add_argument('ticket_owner')


class Events(Resource):
    def get(self):
        """Return list of events"""
        db = service.db.DataBase(user='debian-sys-maint',
                                 password='PggWbsvEVgDZUYar',
                                 host='127.0.0.1',
                                 database='ordtick')
        events = db.get_events()
        db.close()

        return [{'id': i[0],
                 'Name': i[1],
                 'Date': str(i[2]),
                 'Place': i[3],
                 'Total Available': i[4]} for i in events]

    def post(self):
        args = parser.parse_args()
        db = service.db.DataBase(user='debian-sys-maint',
                                 password='PggWbsvEVgDZUYar',
                                 host='127.0.0.1',
                                 database='ordtick')
        db.add_event(args['event_name'],
                     args['event_date'],
                     args['event_place'],
                     args['event_ta'])
        db.close()
        return '', 412


class Event(Resource):
    def get(self, event_id):
        db = service.db.DataBase(user='debian-sys-maint',
                                 password='PggWbsvEVgDZUYar',
                                 host='127.0.0.1',
                                 database='ordtick')
        data = list(db.get_event_by_id(event_id))
        db.close()
        return {'id': data[0],
                'Name': data[1],
                'Date': str(data[2]),
                'Place': data[3],
                'Total Available': data[4],
                }

    def delete(self, event_id):
        db = service.db.DataBase(user='debian-sys-maint',
                                 password='PggWbsvEVgDZUYar',
                                 host='127.0.0.1',
                                 database='ordtick')
        db.remove_event(event_id)
        db.close()
        return '', 204

    def put(self, event_id):
        args = parser.parse_args()
        db = service.db.DataBase(user='debian-sys-maint',
                                 password='PggWbsvEVgDZUYar',
                                 host='127.0.0.1',
                                 database='ordtick')
        db.edit_event(event_id,
                      args['event_name'],
                      args['event_date'],
                      args['event_place'],
                      args['event_ta'])
        db.close()
        return '', 200


class Tickets(Resource):
    def get(self):
        db = service.db.DataBase(user='debian-sys-maint',
                                 password='PggWbsvEVgDZUYar',
                                 host='127.0.0.1',
                                 database='ordtick')
        tickets = db.get_tickets()
        db.close()

        return [{'id': i[0],
                 'event_id': i[1],
                 'owner': i[2]} for i in tickets]

    def post(self):
        args = parser.parse_args()
        db = service.db.DataBase(user='debian-sys-maint',
                                 password='PggWbsvEVgDZUYar',
                                 host='127.0.0.1',
                                 database='ordtick')
        db.add_ticket(args['event_id'], args['ticket_owner'])
        db.close()
        return '', 412


class Ticket(Resource):
    def get(self, ticket_id):
        db = service.db.DataBase(user='debian-sys-maint',
                                 password='PggWbsvEVgDZUYar',
                                 host='127.0.0.1',
                                 database='ordtick')
        data = list(db.get_ticket(ticket_id))
        db.close()
        return {'id': data[0],
                'event_id': data[1],
                'owner': data[2]}

    def delete(self, ticket_id):
        db = service.db.DataBase(user='debian-sys-maint',
                                 password='PggWbsvEVgDZUYar',
                                 host='127.0.0.1',
                                 database='ordtick')
        db.remove_ticket(ticket_id)
        db.close()
        return '', 204

    def put(self, ticket_id):
        args = parser.parse_args()
        db = service.db.DataBase(user='debian-sys-maint',
                                 password='PggWbsvEVgDZUYar',
                                 host='127.0.0.1',
                                 database='ordtick')
        db.edit_ticket(ticket_id,
                      args['event_id'],
                      args['ticket_owner'])
        db.close()
        return '', 200


api.add_resource(Events, '/events')
api.add_resource(Event, '/events/<int:event_id>')
api.add_resource(Tickets, '/tickets')
api.add_resource(Ticket, '/tickets/<int:ticket_id>')


if __name__ == '__main__':
    app.run(debug=True)

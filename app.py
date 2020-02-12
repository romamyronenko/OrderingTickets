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

# database
USER = 'debian-sys-maint'
PASS = 'PggWbsvEVgDZUYar'
DB_HOST = '127.0.0.1'
DATABASE = 'ordtick'


def wrapper(f):
    """Decorator that create connection to database and close it after usage."""
    def connect_db(*args, **kwargs):
        sentinel = object()

        g = f.__globals__
        old_value = dict()
        old_value['db'] = g.get('db', sentinel)

        g['db'] = service.db.DataBase(user=USER,
                                      password=PASS,
                                      host=DB_HOST,
                                      database=DATABASE)

        res = f(*args, **kwargs)
        g['db'].close()

        if old_value is sentinel:
            del g['db']
        else:
            g['db'] = old_value
        return res

    return connect_db


parser = reqparse.RequestParser()
parser.add_argument('event_id')
parser.add_argument('event_name')
parser.add_argument('event_date')
parser.add_argument('event_place')
parser.add_argument('event_ta')
parser.add_argument('event_price')
parser.add_argument('ticket_owner')


class Events(Resource):
    @wrapper
    def get(self):
        """Return list of events"""
        events = db.get_events()

        return [{'id': i[0],
                 'Name': i[1],
                 'Date': str(i[2]),
                 'Place': i[3],
                 'Total Available': i[4],
                 'Price': i[5]} for i in events]

    @wrapper
    def post(self):
        """Create new event"""
        args = parser.parse_args()
        db.add_event(args['event_name'],
                     args['event_date'],
                     args['event_place'],
                     args['event_ta'],
                     args['event_price'])
        return '', 412


class Event(Resource):
    @wrapper
    def get(self, event_id):
        """Return info about event"""
        data = list(db.get_event_by_id(event_id))
        return {'id': data[0],
                'Name': data[1],
                'Date': str(data[2]),
                'Place': data[3],
                'Total Available': data[4],
                'Price': data[5],
                }

    @wrapper
    def delete(self, event_id):
        """Remove event from database"""
        db.remove_event(event_id)
        return '', 204

    @wrapper
    def put(self, event_id):
        """Change event data"""
        args = parser.parse_args()
        db.edit_event(event_id,
                      args['event_name'],
                      args['event_date'],
                      args['event_place'],
                      args['event_ta'],
                      args['event_price'])
        return '', 200


class Tickets(Resource):
    @wrapper
    def get(self):
        """Return list of tickets"""
        tickets = db.get_tickets()
        return [{'id': i[0],
                 'event_id': i[1],
                 'owner': i[2]} for i in tickets]

    @wrapper
    def post(self):
        """Create new ticket"""
        args = parser.parse_args()
        db.add_ticket(args['event_id'], args['ticket_owner'])
        return '', 412


class Ticket(Resource):
    @wrapper
    def get(self, ticket_id):
        """Return info about ticket"""
        data = list(db.get_ticket(ticket_id))
        return {'id': data[0],
                'event_id': data[1],
                'owner': data[2]}

    @wrapper
    def delete(self, ticket_id):
        """Remove ticket from database"""
        db.remove_ticket(ticket_id)
        return '', 204

    @wrapper
    def put(self, ticket_id):
        """Change ticket data"""
        args = parser.parse_args()
        db.edit_ticket(ticket_id,
                      args['event_id'],
                      args['ticket_owner'])
        return '', 200


api.add_resource(Events, '/events')
api.add_resource(Event, '/events/<int:event_id>')
api.add_resource(Tickets, '/tickets')
api.add_resource(Ticket, '/tickets/<int:ticket_id>')


if __name__ == '__main__':
    app.run(debug=True)

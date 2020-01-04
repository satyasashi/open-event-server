import unittest

from app.factories.attendee import AttendeeFactory
from app.models.ticket_holder import TicketHolder
from tests.all.integration.utils import OpenEventTestCase
from app.factories.event import EventFactoryBasic
from app.api.helpers.db import save_to_db, safe_query, get_or_create, get_count
from flask_rest_jsonapi.exceptions import ObjectNotFound
from app.models import db
from app.models.event import Event


class TestDBHelperValidation(OpenEventTestCase):

    def test_save_to_db(self):
        """Method to test the function save_to_db"""

        with self.app.test_request_context():
            obj = EventFactoryBasic()
            save_to_db(obj)
            event = db.session.query(Event).filter(Event.id == obj.id).first()
            self.assertEqual(obj.name, event.name)

    def test_safe_query(self):
        """Method to test the function safe_query"""

        with self.app.test_request_context():
            event = EventFactoryBasic()
            save_to_db(event)
            obj = safe_query(db, Event, 'id', event.id, 'event_id')
            self.assertEqual(obj.name, event.name)

    def test_safe_query_exception(self):
        """Method to test the exception in function safe_query"""

        with self.app.test_request_context():
            self.assertRaises(ObjectNotFound, lambda: safe_query(db, Event, 'id', 1, 'event_id'))

    def test_get_or_create(self):
        """Method to test the function get_or_create"""

        with self.app.test_request_context():
            event = EventFactoryBasic()
            save_to_db(event)
            obj, is_created = get_or_create(Event, name=event.name)
            self.assertEqual(event.id, obj.id)
            self.assertFalse(is_created)

            obj, is_created = get_or_create(Event, name="new event", starts_at=event.starts_at, ends_at=event.ends_at)
            self.assertNotEqual(event.id, obj.id)
            self.assertTrue(is_created)

    def test_get_count(self):
        """Method to test the number of queries concerning a Model"""

        with self.app.test_request_context():
            attendee = AttendeeFactory()
            save_to_db(attendee)
            self.assertEqual(get_count(TicketHolder.query), 1)


if __name__ == '__main__':
    unittest.main()

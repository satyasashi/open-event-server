import unittest
from datetime import datetime
from pytz import timezone
from unittest import TestCase

from app.api.helpers.exceptions import UnprocessableEntity
from app.api.schema.sessions import SessionSchema


class TestSessionValidation(TestCase):

    def test_date_pass(self):
        """
        Sessions Validate Date - Tests if the function runs without an exception
        :return:
        """
        schema = SessionSchema()
        original_data = {
            'data': {}
        }
        data = {
            'starts_at': datetime(2099, 8, 4, 12, 30, 45).replace(tzinfo=timezone('UTC')),
            'ends_at': datetime(2099, 9, 4, 12, 30, 45).replace(tzinfo=timezone('UTC'))
        }
        SessionSchema.validate_fields(schema, data, original_data)

    def test_date_start_gt_end(self):
        """
        Sessions Validate Date - Tests if exception is raised when ends_at is before starts_at
        :return:
        """
        schema = SessionSchema()
        original_data = {
            'data': {}
        }
        data = {
            'starts_at': datetime(2099, 9, 4, 12, 30, 45).replace(tzinfo=timezone('UTC')),
            'ends_at': datetime(2099, 8, 4, 12, 30, 45).replace(tzinfo=timezone('UTC'))
        }
        with self.assertRaises(UnprocessableEntity):
            SessionSchema.validate_fields(schema, data, original_data)


if __name__ == '__main__':
    unittest.main()

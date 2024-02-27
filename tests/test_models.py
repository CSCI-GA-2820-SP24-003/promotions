"""
Test cases for Pet Model
"""

import os
import logging
from unittest import TestCase
from datetime import date
from wsgi import app
from service.models import Promotion, DataValidationError, db

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  P R O M O T I O N   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotion(TestCase):
    """Test Cases for Promotion Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Promotion).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_example_replace_this(self):
        """It should always be true"""
        # Todo: Remove this test case example
        self.assertTrue(True)

    # Todo: Add your test cases here...
    def test_create_a_promotion(self):
        """It should Create a promotion and assert that it exists"""
        promotion = Promotion(
            name="Happy_New_Year",
            start_date=date.fromisoformat("2023-12-29"),
            duration=5,
            rule="30'%'discount",
            products_id=1,
        )
        self.assertEqual(str(promotion), "<Promotion Happy_New_Year id=[None]>")
        self.assertTrue(promotion is not None)
        self.assertEqual(promotion.id, None)
        self.assertEqual(promotion.start_date, date.today())
        self.assertEqual(promotion.start_date, date.fromisoformat("2023-12-29"))
        self.assertEqual(promotion.duration, 5)
        self.assertEqual(promotion.rule, "30'%'discount")
        self.assertEqual(promotion.products_id, 1)

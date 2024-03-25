"""
TestPromotion API Service Test Suite
"""

import os
import logging
from unittest import TestCase
from datetime import date
from wsgi import app
from service.common import status
from service.models import db, Promotion
from .factories import PromotionFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/promotions"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotionService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Promotion).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def _create_promotions(self, count):
        """Factory method to create promotions in bulk"""
        promotions = []
        for _ in range(count):
            test_promotion = PromotionFactory()
            response = self.client.post(BASE_URL, json=test_promotion.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test promotion",
            )
            new_promotion = response.get_json()
            test_promotion.id = new_promotion["id"]
            promotions.append(test_promotion)
        return promotions

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_promotion(self):
        """It should Create a new Promotion"""
        test_promotion = PromotionFactory()
        logging.debug("Test Promotion: %s", test_promotion.serialize())
        response = self.client.post(BASE_URL, json=test_promotion.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_promotion = response.get_json()
        self.assertEqual(new_promotion["name"], test_promotion.name)
        self.assertEqual(
            date.fromisoformat(new_promotion["start_date"]), test_promotion.start_date
        )
        self.assertEqual(new_promotion["duration"], test_promotion.duration)
        self.assertEqual(new_promotion["rule"], test_promotion.rule)
        self.assertEqual(new_promotion["product_id"], test_promotion.product_id)

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_promotion = response.get_json()
        self.assertEqual(new_promotion["name"], test_promotion.name)
        self.assertEqual(
            date.fromisoformat(new_promotion["start_date"]), test_promotion.start_date
        )
        self.assertEqual(new_promotion["duration"], test_promotion.duration)
        self.assertEqual(new_promotion["rule"], test_promotion.rule)
        self.assertEqual(new_promotion["product_id"], test_promotion.product_id)

    def test_get_promotion(self):
        """It should Get a single Promotion"""
        # get the id of a promotion
        test_promotion = self._create_promotions(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_promotion.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_promotion.name)

    def test_delete_promotion(self):
        """This should delete a single Promotion"""
        # get the id of a promotion
        test_db = self._create_promotions(5)
        test_promotion_id = test_db[0].id
        response = self.client.delete(f"{BASE_URL}/{test_promotion_id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_promotion(self):  # maybe we dont need an input for the call
        """It should list all Promotions"""
        self._create_promotions(2)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        promotions = response.get_json()
        self.assertEqual(len(promotions), 2)

    def test_get_promotion_not_found(self):
        """It should not Get a Promotion thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_update_promotion(self):
        """It should Update an existing Promotion"""
        # Step 1: Create a promotion to update
        test_promotion = self._create_promotions(1)[0]

        # Step 2: Define the data for updating the promotion
        update_data = {
            "name": "Updated Promotion Name",
            "start_date": str(
                test_promotion.start_date
            ),  # Keeping the original start_date for completeness
            "duration": test_promotion.duration + 5,  # Updating the duration
            "rule": "Updated Rule",  # Updating the rule
            "product_id": test_promotion.product_id,  # Keeping the original product_id for completeness
        }

        # Step 3: Send a PUT request to update the promotion
        response = self.client.put(f"{BASE_URL}/{test_promotion.id}", json=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Step 4: Fetch the updated promotion and verify the updates
        response = self.client.get(f"{BASE_URL}/{test_promotion.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_promotion = response.get_json()

        self.assertEqual(updated_promotion["name"], update_data["name"])
        self.assertEqual(updated_promotion["duration"], update_data["duration"])
        self.assertEqual(updated_promotion["rule"], update_data["rule"])
        self.assertEqual(updated_promotion["product_id"], update_data["product_id"])


######################################################################
#  T E S T   S A D   P A T H S
######################################################################
class TestSadPaths(TestCase):
    """Test REST Exception Handling"""

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()

    def test_method_not_allowed(self):
        """It should not allow update without a promotion id"""
        response = self.client.put(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_promotion_no_data(self):
        """It should not Create a Promotion with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_promotion_no_content_type(self):
        """It should not Create a Promotion with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_promotion_wrong_content_type(self):
        """It should not Create a Promotion with the wrong content type"""
        response = self.client.post(BASE_URL, data="hello", content_type="text/html")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

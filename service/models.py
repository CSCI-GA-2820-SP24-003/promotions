"""
Models for Promotion

All of the models are stored in this module
"""

import logging
from enum import Enum
from datetime import date
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DatabaseConnectionError(Exception):
    """Custom Exception when database connection fails"""


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class PromotionType(Enum):
    """Enumeration of valid PromotionTypes"""

    AMOUNT_DISCOUNT = 0  # e.g. 30$ off
    PERCENTAGE_DISCOUNT = 1  # e.g. 20% OFF
    BXGY = 2  # Buy X get Y free
    UNKNOWN = 3


class Promotion(db.Model):
    """
    Class that represents a Promotion
    """

    # pylint: disable=too-many-instance-attributes
    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    start_date = db.Column(db.Date(), nullable=False, default=date.today())
    duration = db.Column(db.Integer, nullable=False)
    promotion_type = db.Column(
        db.Enum(PromotionType),
        nullable=False,
        server_default=(PromotionType.UNKNOWN.name),
    )
    rule = db.Column(db.String(63), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Promotion {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Promotion to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """
        Updates a Promotion to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:  # it should not update a promotion with no id
            raise DataValidationError("Update called with empty ID field")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a Promotion from the data store"""
        logger.info("Deleting %s", self.name)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def activate(self):
        """Activates a Promotion by setting status to True"""
        logger.info("Activate Promotion with Promotion Id %d", self.id)
        self.status = True
        db.session.commit()

    def deactivate(self):
        """Deactivates a Promotion by setting status to False"""
        logger.info("Deactivate Promotion with Promotion Id %d", self.id)
        self.status = False
        db.session.commit()

    def serialize(self):
        """Serializes a Promotion into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "duration": self.duration,
            "promotion_type": self.promotion_type.name,  # convert enum to string
            "rule": self.rule,
            "product_id": self.product_id,
            "status": self.status,
        }

    def deserialize(self, data):
        """
        Deserializes a Promotion from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.start_date = date.fromisoformat(data["start_date"])
            if isinstance(data["duration"], int):
                self.duration = data["duration"]
            else:
                raise DataValidationError(
                    "Invalid type for integer [duration]: "
                    + str(type(data["duration"]))
                )
            self.promotion_type = getattr(
                PromotionType, data["promotion_type"]
            )  # create enum from string
            self.rule = data["rule"]
            if isinstance(data["product_id"], int):
                self.product_id = data["product_id"]
            else:
                raise DataValidationError(
                    "Invalid type for integer [product_id]: "
                    + str(type(data["product_id"]))
                )
            self.status = data.get("status", True)
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Promotion: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Promotion: body of request contained bad or no data "
                + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls) -> list:
        """Returns all of the Promotions in the database"""
        logger.info("Processing all Promotions")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Promotion by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.session.get(cls, by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Promotions with the given name

        Args:
            name (string): the name of the Promotions you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_promotion_type(
        cls, promotion_type: PromotionType = PromotionType.UNKNOWN
    ) -> list:
        """Returns all Promotions by their PromotionType

        :param promotion_type: values are ['AMOUNT_DISCOUNT', 'PERCENTAGE_DISCOUNT', 'BXGY', 'UNKNOWN']
        :type available: enum

        :return: a collection of Promotions that are available
        :rtype: list

        """
        logger.info("Processing promotion_type query for %s ...", promotion_type.name)
        return cls.query.filter(cls.promotion_type == promotion_type)

    @classmethod
    def find_by_product_id(cls, product_id):
        """Returns all Promotions with the given product_id

        Args:
            product_id (string): the product_id of the Promotions you want to match
        """
        logger.info("Processing product_id query for %d ...", product_id)
        return cls.query.filter(cls.product_id == product_id)

    @classmethod
    def find_by_start_date(cls, start_date):
        """Returns all Promotions with the given start_date

        Args:
            start_date (string): the start_date of the Promotions you want to match
        """
        logger.info("Processing start_date query for %s ...", start_date)
        return cls.query.filter(cls.start_date == date.fromisoformat(start_date))

    @classmethod
    def find_by_promotion_status(cls, promotion_status: bool = True) -> list:
        """Returns all Promotions by their status

        :param available: True for promotions that are activated
        :type available: str

        :return: a collection of Promotions that are activated
        :rtype: list

        """
        logger.info("Processing promotion status query for %s ...", promotion_status)
        return cls.query.filter(cls.status == promotion_status)

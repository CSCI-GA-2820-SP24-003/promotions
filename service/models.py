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

    def list_all():
        """Retrieve all promotions. Returns: List[Promotion]: A list of all promotions."""
        logger.info("Listing all Promotions")
        try:
            promotions = Promotion.all()
            db.session.commit()
            return promotions
        except Exception as e:
            logger.error("Error listing records")
            raise DataValidationError(e) from e

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

        # Todo: uncomment this code when tests can cover this
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
    def all(cls):
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
    def delete_by_id(cls, by_id):
        """Delete a Promotion by its ID"""
        logger.info("Processing delete with id %s ...", by_id)
        cls.query.filter(cls.id == by_id).delete()

    @classmethod
    def find_by_promotion_type(
        cls, promotion_type: PromotionType = PromotionType.UNKNOWN
    ) -> list:
        """Returns all Pets by their PromotionType

        :param promotion_type: values are ['AMOUNT_DISCOUNT', 'PERCENTAGE_DISCOUNT', 'BXGY', 'UNKNOWN']
        :type available: enum

        :return: a collection of Pets that are available
        :rtype: list

        """
        logger.info("Processing promotion_type query for %s ...", promotion_type.name)
        return cls.query.filter(cls.promotion_type == promotion_type)

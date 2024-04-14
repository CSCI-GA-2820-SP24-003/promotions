"""
Test Factory to make fake objects for testing
"""

from datetime import date

import factory
from factory.fuzzy import FuzzyDate, FuzzyChoice, FuzzyInteger, FuzzyText
from service.models import Promotion, PromotionType


class PromotionFactory(factory.Factory):
    """Creates fake promotions that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Promotion

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    start_date = FuzzyDate(date(2023, 1, 1))
    duration = FuzzyInteger(0, 101)
    promotion_type = FuzzyChoice(
        choices=[
            PromotionType.AMOUNT_DISCOUNT,
            PromotionType.PERCENTAGE_DISCOUNT,
            PromotionType.BXGY,
            PromotionType.UNKNOWN,
        ]
    )
    rule = FuzzyText(length=63)
    product_id = FuzzyInteger(0, 100)
    status = FuzzyChoice(choices=[True, False])

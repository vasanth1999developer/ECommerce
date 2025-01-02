from django.db import models

from apps.common.models import BaseIdentityModel


class Country(BaseIdentityModel):
    """
    Model to store country details.

    Model Fields -
        PK          - id,
        Fields      - uuid, name
        Datetime    - created_at, modified_at

    App QuerySet Manager Methods -
        get_or_none
    """

    class Meta(BaseIdentityModel.Meta):
        default_related_name = "related_countries"


class State(BaseIdentityModel):
    """
    Model to store state details.

    Model Fields -
        PK          - id,
        FK          - country
        Fields      - uuid, name
        Datetime    - created_at, modified_at

    App QuerySet Manager Methods -
        get_or_none
    """

    class Meta(BaseIdentityModel.Meta):
        default_related_name = "related_states"

    country = models.ForeignKey(to=Country, on_delete=models.CASCADE)


class City(BaseIdentityModel):
    """
    Model to store city details.

    Model Fields -
        PK          - id,
        FK          - state
        Fields      - uuid, identity
        Datetime    - created_at, modified_at

    App QuerySet Manager Methods -
        get_or_none
    """

    class Meta(BaseIdentityModel.Meta):
        default_related_name = "related_cities"

    state = models.ForeignKey(to=State, on_delete=models.CASCADE)

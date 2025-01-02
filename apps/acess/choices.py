from djchoices import ChoiceItem, DjangoChoices


class GenderChoices(DjangoChoices):
    """Holds the choices of genders."""

    male = ChoiceItem("male", "Male")
    female = ChoiceItem("female", "Female")
    others = ChoiceItem("others", "Others")


class RoleTypeChoices(DjangoChoices):
    """Choices for user roles."""

    admin = ChoiceItem("admin", "Admin")
    member = ChoiceItem("buyers", "Buyers")


class TagTypeChoices(DjangoChoices):
    """Choices for tag types."""

    home = ChoiceItem("home", "Home")
    work = ChoiceItem("work", "Work")
    others = ChoiceItem("others", "Others")


class OfferChoice(DjangoChoices):
    """Choices for offers."""

    no_offers = ChoiceItem("no offer", "No offer")
    coupon = ChoiceItem("coupon", "Coupon")
    bankOffer = ChoiceItem("bank offer", "Bank offer")
    SpecialOffer = ChoiceItem("special offer", "Special offer")

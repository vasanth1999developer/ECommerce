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
    bank_offer = ChoiceItem("bank offer", "Bank offer")
    special_offer = ChoiceItem("special offer", "Special offer")


class RatingChoice(DjangoChoices):
    """Choices for ratings."""

    one_star = ChoiceItem(1, "1 Star")
    two_star = ChoiceItem(2, "2 Stars")
    three_star = ChoiceItem(3, "3 Stars")
    four_star = ChoiceItem(4, "4 Stars")
    five_star = ChoiceItem(5, "5 Stars")


class OrderStatusChoice(DjangoChoices):
    """Choices for order status."""

    placed = ChoiceItem("placed", "Placed")
    shipped = ChoiceItem("shipped", "Shipped")
    delivered = ChoiceItem("delivered", "Delivered")


class PaymentStatusChoice(DjangoChoices):
    """Choices for payment status."""

    pending = ChoiceItem("PENDING", "Pending")
    success = ChoiceItem("SUCCESS", "Success")
    failed = ChoiceItem("FAILED", "Failed")

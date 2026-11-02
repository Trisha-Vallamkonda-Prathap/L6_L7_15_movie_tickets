import pytest

from movie_tickets import group_discount, snack_combo, ticket_price


@pytest.mark.parametrize(
    ("seat", "expected_price"),
    [
        ("regular", 150),
        ("premium", 250),
        ("recliner", 400),
    ],
)
def test_ticket_price_uses_price_for_each_valid_seat(seat, expected_price):
    assert ticket_price(seat, 25, 12, False) == expected_price


def test_ticket_price_rejects_unknown_seat():
    with pytest.raises(ValueError, match="^unknown seat$"):
        ticket_price("vip", 25, 12, False)


@pytest.mark.parametrize(
    ("show_hour", "expected_price"),
    [
        (0, 100),
        (11, 100),
        (12, 150),
        (17, 150),
        (18, 180),
        (23, 180),
    ],
)
def test_ticket_price_applies_time_adjustment_at_valid_hours(
    show_hour, expected_price
):
    assert ticket_price("regular", 25, show_hour, False) == expected_price


@pytest.mark.parametrize("show_hour", [-1, 24])
def test_ticket_price_rejects_hours_outside_valid_range(show_hour):
    with pytest.raises(ValueError, match="^invalid show time$"):
        ticket_price("regular", 25, show_hour, False)


@pytest.mark.parametrize(
    ("is_weekend", "expected_price"),
    [
        (False, 150),
        (True, 190),
    ],
)
def test_ticket_price_applies_weekend_surcharge(is_weekend, expected_price):
    assert ticket_price("regular", 25, 12, is_weekend) == expected_price


@pytest.mark.parametrize(
    ("age", "expected_price"),
    [
        (2, 0),
        (3, 75),
        (12, 75),
        (13, 150),
        (59, 150),
        (60, 75),
    ],
)
def test_ticket_price_applies_age_rules_at_boundaries(age, expected_price):
    assert ticket_price("regular", age, 12, False) == expected_price


@pytest.mark.parametrize(
    ("tickets", "is_student_group", "expected_discount"),
    [
        (1, False, 0),
        (1, True, 0),
        (4, False, 0),
        (4, True, 0),
        (5, False, 10),
        (5, True, 15),
        (9, False, 10),
        (9, True, 15),
        (10, False, 15),
        (10, True, 20),
    ],
)
def test_group_discount_by_quantity_and_student_status(
    tickets, is_student_group, expected_discount
):
    assert group_discount(tickets, is_student_group) == expected_discount


def test_group_discount_rejects_zero_tickets():
    with pytest.raises(ValueError, match="^no tickets$"):
        group_discount(0, False)


@pytest.mark.parametrize(
    ("size", "has_coupon", "expected_cost"),
    [
        ("small", False, 120),
        ("small", True, 70),
        ("medium", False, 180),
        ("medium", True, 130),
        ("large", False, 250),
        ("large", True, 200),
    ],
)
def test_snack_combo_prices_each_size_with_and_without_coupon(
    size, has_coupon, expected_cost
):
    assert snack_combo(size, has_coupon) == expected_cost

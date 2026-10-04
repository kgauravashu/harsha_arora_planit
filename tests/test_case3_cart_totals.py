from decimal import Decimal

from pages.cart_page import CartPage
from pages.shop_page import ShopPage
from tests.expected_data import CART_PRODUCTS


def test_cart_totals_and_prices(driver):
    shop = ShopPage(driver).load()
    for product, quantity in CART_PRODUCTS.items():
        shop.buy_product(product, quantity)

    cart = CartPage(driver)
    rows = cart.load().get_rows()

    assert {r["product"]: r["quantity"] for r in rows} == CART_PRODUCTS, \
        f"Cart contents differ from what was bought. Rows: {rows}"

    for row in rows:
        assert row["price"] > 0, f"{row['product']}: price must be positive"
        # Decimal comparison is exact, so no tolerance is needed.
        assert row["subtotal"] == row["price"] * row["quantity"], \
            f"{row['product']}: subtotal {row['subtotal']} != " \
            f"{row['price']} x {row['quantity']}"

    expected_total = sum((r["subtotal"] for r in rows), Decimal("0"))
    assert cart.get_total() == expected_total

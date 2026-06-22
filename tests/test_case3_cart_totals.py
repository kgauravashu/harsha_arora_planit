from pages.shop_page import ShopPage
from pages.cart_page import CartPage

# Product name exactly as shown on the Jupiter shop page
PRODUCTS = {
    "Stuffed Frog":  2,
    "Fluffy Bunny":  5,
    "Valentine Bear": 3,
}


def test_cart_totals_and_prices(driver):
    shop = ShopPage(driver)
    cart = CartPage(driver)

    # 1. Add each product the required number of times
    shop.load()
    for product, qty in PRODUCTS.items():
        shop.buy_product(product, qty)

    # 2. Navigate to cart
    cart.load()
    rows = cart.get_rows()

    assert len(rows) == len(PRODUCTS), \
        f"Expected {len(PRODUCTS)} cart rows, got {len(rows)}. Rows: {rows}"

    calculated_total = 0.0

    for row in rows:
        product  = row["product"]
        price    = float(row["price"])
        quantity = int(row["quantity"])
        subtotal = float(row["subtotal"])

        # Verify product is one we added
        assert product in PRODUCTS, f"Unexpected product in cart: '{product}'"

        # Verify quantity
        expected_qty = PRODUCTS[product]
        assert quantity == expected_qty, \
            f"{product}: expected qty {expected_qty}, got {quantity}"

        # Verify subtotal = price × quantity
        expected_subtotal = round(price * quantity, 2)
        assert abs(subtotal - expected_subtotal) < 0.01, \
            f"{product}: expected subtotal ${expected_subtotal}, got ${subtotal}"

        # Verify price is positive
        assert price > 0, f"{product}: price must be > 0, got {price}"

        calculated_total += subtotal

    # Verify grand total = sum of subtotals
    actual_total = float(cart.get_total())
    assert abs(actual_total - round(calculated_total, 2)) < 0.01, \
        f"Expected grand total ${round(calculated_total, 2)}, got ${actual_total}"

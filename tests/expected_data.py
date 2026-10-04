"""Expected UI copy and test inputs, kept out of the tests so a wording change
in the app is a one-line edit here rather than a hunt through assertions."""

CONTACT_ERRORS = {
    "forename": "Forename is required",
    "email": "Email is required",
    "message": "Message is required",
}

# Includes the forename, so the assertion also proves the app echoed the
# right user's input back, not just that *a* banner appeared.
CONTACT_SUCCESS_TEMPLATE = "Thanks {forename}, we appreciate your feedback."

CART_PRODUCTS = {
    "Stuffed Frog": 2,
    "Fluffy Bunny": 5,
    "Valentine Bear": 3,
}

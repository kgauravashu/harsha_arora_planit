# harsha_arora_planit

# Jupiter Toys UI Test Automation

Selenium + pytest, Page Object Model.

## Structure
```
harsha_arora_planit
├── pages/
│   ├── base_page.py
│   ├── home_page.py
│   ├── contact_page.py
│   ├── shop_page.py
│   └── cart_page.py
├── tests/
│   ├── conftest.py
│   ├── test_case1_contact_validation.py
│   ├── test_case2_contact_success.py   (parametrized x5)
│   └── test_case3_cart_totals.py
├── pytest.ini
├── requirements.txt
└── .github/workflows/testui.yml
```

## Run locally
```bash
pip install -r requirements.txt
# Requires Chrome + chromedriver on PATH
pytest
```

Set `HEADLESS=false` to watch the browser.

## Test cases
- **Case 1**: Contact page mandatory field validation — empty submit shows errors, filling fields removes them.
- **Case 2**: Contact page successful submission, run 5x via pytest parametrize for 100% pass-rate verification.
- **Case 3**: Buy 2 Stuffed Frog, 5 Fluffy Bunny, 3 Valentine Bear; validate cart subtotals, prices, and grand total.

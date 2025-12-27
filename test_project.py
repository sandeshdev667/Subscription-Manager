from project import parse_price

def test_parse_price():
    assert parse_price("Your total is $14.99") == "14.99"
    assert parse_price("No price here") == None
    assert parse_price("Cost: $5.00") == "5.00"
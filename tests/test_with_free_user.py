import datetime
import time

import pytest
import requests

import config
from utils.utils import format_date
from utils.validators import validate_success_response, validate_error_response


@pytest.mark.parametrize("symbols_values", ["INR,USD,GBP", "INR", ""])
def test_get_latest_rates(get_latest_endpoint, symbols_values):
    response = requests.get(get_latest_endpoint, params={"access_key": config.FREE_USER_ACCESS_KEY, "base": "EUR",
                                                         "symbols": symbols_values})
    actual_response_json = response.json()
    validate_success_response(response, 200)

    assert "base" in actual_response_json and actual_response_json[
        "base"] == "EUR", "Either Base not exists in response or value is not correct"
    assert "timestamp" in actual_response_json and actual_response_json[
        "timestamp"] != [], "Either Timestamp not exists in response or value not displayed"
    assert actual_response_json["date"] == format_date(datetime.date.today()), "Date is not correct"
    assert actual_response_json["rates"], "Response doesn't returns rates"

    if symbols_values:
        expected_symbols = {symbol for symbol in symbols_values.split(',')}

        actual_symbols = set(actual_response_json["rates"].keys())
        missing_codes = expected_symbols - actual_symbols
        assert not missing_codes, f"Missed rates: {missing_codes}"
        for actual_symbol in actual_response_json["rates"]:
            assert actual_response_json["rates"][actual_symbol] is not None, f"No value present for {actual_symbol}"

    time.sleep(config.DELAY_BETWEEN_REQUESTS_SECONDS)


def test_base_currency_error(get_latest_endpoint):
    response = requests.get(get_latest_endpoint,
                            params={"access_key": config.FREE_USER_ACCESS_KEY, "base": "USD", "symbols": "INR"})
    validate_error_response(response, 105, "base_currency_access_restricted")
    time.sleep(config.DELAY_BETWEEN_REQUESTS_SECONDS)


@pytest.mark.parametrize("endpoint, parameters, expected_code, expected_type", [
    ("get_convert_endpoint", {"access_key": config.FREE_USER_ACCESS_KEY, "from": "EUR", "to": "INR", "amount": 100},
     105, "function_access_restricted"),
    ("get_latest_endpoint", {"access_key": config.FREE_USER_ACCESS_KEY, "base": "USD"}, 106, "rate_limit_reached"),
    ("get_currencies_endpoint", {"access_key": ""}, 101, "missing_access_key"),
    ("get_currencies_endpoint", {"access_key": None}, 101, "missing_access_key"),
    ("get_currencies_endpoint", {"access_key": " "}, 101, "invalid_access_key"),
    ("get_currencies_endpoint", {"access_key": "123"}, 101, "invalid_access_key")
])
def test_errors(request, endpoint, parameters, expected_code, expected_type):
    resource = request.getfixturevalue(endpoint)
    response = requests.get(resource, parameters)
    validate_error_response(response, expected_code, expected_type)


def test_get_currencies_list(get_currencies_endpoint):
    response = requests.get(get_currencies_endpoint, params={"access_key": config.FREE_USER_ACCESS_KEY})

    validate_success_response(response, 200)
    actual_json_response = response.json()
    assert "symbols" in actual_json_response, "Symbols is empty"
    symbols_returned_data = actual_json_response["symbols"]
    assert symbols_returned_data[
               "AED"] == "United Arab Emirates Dirham", "Response doesn't contain the AED Currency"
    assert symbols_returned_data[
               "BAM"] == "Bosnia-Herzegovina Convertible Mark", "Response doesn't contain the BAM Currency"

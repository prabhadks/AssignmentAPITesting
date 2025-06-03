def validate_error_response(response, expected_code, expected_type):
    body = response.json()
    assert body.get("success") is False
    assert body["error"]["code"] == expected_code
    assert body["error"]["type"] == expected_type

def validate_success_response(response, expected_status):
    assert response.status_code == expected_status
    body = response.json()
    assert body.get("success") is True
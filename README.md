# API Endpoint Validation Framework

---

## 🚀 Overview

This project provides a robust framework for validating critical API endpoints. Designed with **Pytest** and its powerful **parameterization** feature, it focuses on ensuring the correctness, accessibility, and reliability of API responses.

## ✨ Key Features

* **Endpoint Validation:** Comprehensive testing of various API endpoints.
* **User-Specific Access Control:** Tests API accessibility based on unique user subscription keys.
* **Rate Limit Handling:** Implements strategic delays to gracefully manage API rate limits.
* **Parameterized Testing:** Efficiently validates multiple scenarios (success and error) across various endpoints and test data.
* **Modular Architecture:** Clear separation of concerns for configuration, fixtures, and assertion logic.
* **Centralized Configuration:** Easy management of API base URLs, paths, and user access keys.

---

## 📺 Visual Demonstration

Below is a short GIF demonstrating a test run or a key API interaction validated by this framework.

![Demo of API Test Execution](https://github.com/prabhadks/AssignmentAPITesting/blob/master/testresults/APITestingAssignment.gif)

## 📊 Example Test Cases

Here's a breakdown of the key test scenarios and their validation strategies within this framework:

| Test in Framework    | Test Description                                                                                                                                                                                                                                                            | Validation Used                                                                                                                                                                                                                                                                                                         | Why it is Used                                                                                                                                                                                                |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `test_get_currencies_list` | Validates **successful data retrieval** for the Currencies List API.                                                                                                                                                                                                        | Asserts a `200` HTTP status code. Verifies `success: true` and the presence of the `symbols` attribute, which contains expected currency data.                                                                                                                                          | Ensures the API correctly processes valid requests and returns the expected data, confirming core functionality.                                                                                          |
| `test_get_latest_rates`  | Validates **successful data retrieval** for the Get Latest Rates API. This **parameterized** test covers input variations for multiple currencies, a single currency, and an empty symbols list. **A key consideration for this testing environment is that the free trial account used restricts the base currency to `EUR`.** | Asserts a `200` HTTP status code. Verifies `success: true`, `base` as `EUR`, `timestamp` as today's date. Crucially, asserts that `rates` contains all requested keys with valid values, **and specifically, that `rates` is not empty when `symbols` is empty in the request.** | Ensures the API correctly processes valid requests with diverse input data and returns the expected data, confirming core functionality and adherence to the free trial limitations for this account.      |
| `test_base_currency_error` | Validates that the Latest Rates API **restricts free trial users** from executing requests with a different base currency country code.                                                                                                                                  | Asserts `success: false`, `error_code: 105`, and `error_type: base_currency_access_restricted`.                                                                                                                                                         | Confirms accurate client-side error handling and validates a core access restriction, ensuring users cannot perform unauthorized actions.                                                                 |
| `test_errors` (Convert API) | Validates that the **Convert API is restricted** for free trial users.                                                                                                                                                                                                      | Asserts `success: false`, `error_code: 105`, and `error_type: function_access_restricted`.                                                                                                                                                              | Confirms accurate client-side error handling and validates a core access restriction, ensuring users cannot perform unauthorized actions.                                                                 |
| `test_errors` (Invalid Parameters) | Verifies **error responses for invalid parameters** when calling the Currencies List API. This test is **parameterized** for scenarios such as an invalid access key, `None`, empty, or whitespace values.                                                      | Asserts `success: false`, and specifically checks for `error_code: 101` with appropriate `error_type` (either `missing_access_key` or `invalid_access_key`).                                                                                          | Confirms the API handles invalid inputs gracefully and provides clear, consistent error messages, which is crucial for debugging and proper client-side error handling.                                   |

**Note:**

* The `test_errors` function is a **single, parameterized test** designed to cover various error scenarios across different endpoints. It takes the endpoint, request parameters, expected error code, and error type as parameters.
* Similarly, `test_get_latest_rates` is a **parameterized test** covering multiple valid input data sets for the Latest Rates API.---

## 📁 Project Structure

Your project is organized as follows:

```
AssignmentAPITesting
    config.py
    README.md
    requirements.txt
    testresults\
        APITestingAssignment.gif
    tests\
        conftest.py
        test_with_free_user.py
        __init__.py
    utils\
        utils.py
        validators.py
        __init__.py

```

## ⚠️ Problem Statement & Solutions

### **Access Key Subscription**
API access in this framework is predicated on **user-specific access keys**. The testing approach is tailored to validate API behavior and data access based on these distinct user subscriptions, ensuring proper authorization and data segmentation.

### **Rate Limiting**
A common challenge with external APIs is **rate limiting**, where an excessive number of requests in a short period leads to `rate_limit_exceeded` responses. To mitigate this intermittent error and ensure stable test execution, the framework incorporates a **nominal, configurable delay** between API requests.

## 🏗️ Framework Architecture & Design

The framework is meticulously designed for efficiency, clarity, and maintainability, leveraging Pytest's ecosystem.

### **Pytest & Parameterization**
* The core of the framework utilizes **Pytest** for test execution, providing a flexible and extensible testing environment.
* **Parameterization** is heavily employed to allow a single test function to validate multiple input scenarios (e.g., different valid parameters for success, or various combinations leading to errors) without duplicating code.

### **Centralized Configuration (`config.py`)**
A dedicated `config.py` file serves as the single source of truth for all environment-specific and configurable parameters:
* `BASE_URL`: The root URL for all API endpoints.
* `APIEndpoints`: Defines distinct paths for each API endpoint.
* `ACCESS_KEYS`: Stores different user-specific access keys for varied testing scenarios.
* `DELAY_BETWEEN_REQUESTS_SECONDS`: A configurable delay introduced between API requests to prevent rate limit issues.

### **Fixture Management (`conftest.py`)**
The `conftest.py` file plays a crucial role in setting up the test environment:
* It contains **Pytest fixtures** responsible for constructing specific API endpoint URLs, building them dynamically from the `BASE_URL` and `API_PATHS` defined in `config.py`.
* These fixtures ensure that test functions can easily obtain the correct API endpoint without needing to manually construct URLs.

### **Centralized Assertions (`validators.py`)**
A dedicated `validators.py` module houses common assertion logic, promoting code reusability and consistency across tests:
* By default, tests validate the presence of a `success` field in the API response (true/false).
* If `success` is `false`, it further validates the `error_code` and `error_type` returned in the response.
* This approach ensures uniform error handling and validation across all API tests.

### **Utility Functions (`utils.py`)**
The `utils.py` file serves as a repository for generic utility functions that can be reused across the framework. For instance, it currently includes a date formatting function.

### **Test Organization**
Tests are organized based on user roles and endpoint functionality:
* **User Role Specific Files:** For each distinct user role (identified by an access key), a separate test file is created (e.g., `test_admin_api.py`, `test_basic_user_api.py`).
* **Success Endpoint Validation:** Within these files, dedicated test functions are designed to validate successful API responses for specific endpoints, leveraging parameterization for various valid inputs.
* **Error Response Validation:** A single, parameterized test function is created to cover error responses across multiple endpoints. It's parameterized by the endpoint, input parameters, expected `error_code`, and `error_type`.

## 🚀 Getting Started

To set up and run this API validation framework on your local machine, follow these steps:

### **Prerequisites**
* **Python:** Ensure Python is installed on your system.
* **Git:** For cloning the repository.

### **Installation**
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/prabhadks/AssignmentAPITesting.git]
    cd AssignmentAPITesting
    ```
2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows:
    .\.venv\Scripts\activate
    # On macOS/Linux:
    source ./.venv/bin/activate
    ```
3.  **Install project dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure you have a `requirements.txt` file containing `pytest`, `requests`, etc. You can generate one with `pip freeze > requirements.txt`)*

## ▶️ How to Run Tests

Ensure your virtual environment is active and you're in the project root directory.

To execute the full API test suite:

```bash
pytest
```

For more verbose output during test execution (including print statements and detailed test names):

```bash
pytest -s -v
```
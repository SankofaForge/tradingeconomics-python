"""
Pytest configuration for integration tests.

These tests make REAL API calls to Trading Economics API.
- They are SLOW (network latency + API processing)
- They consume API quota
- They require valid API credentials

Usage:
    # Run all integration tests (API key via CLI flag)
    pytest tests/integration/ -v --apikey=YOUR_KEY

    # Run all integration tests (API key via env var)
    set apikey=YOUR_KEY && pytest tests/integration/ -v

    # Run specific module
    pytest tests/integration/calendar/ -v --apikey=YOUR_KEY

    # Run with markers
    pytest tests/integration/ -m "slow" -v --apikey=YOUR_KEY
"""

import pytest
import os
import time
import tradingeconomics as te
from tradingeconomics.functions import AuthenticationError


def pytest_addoption(parser):
    parser.addoption(
        "--apikey",
        action="store",
        default=None,
        help="Trading Economics API key (overrides the 'apikey' environment variable)",
    )


def _resolve_api_key(config):
    """Return CLI --apikey flag if set, otherwise fall back to the env var."""
    return config.getoption("--apikey") or os.environ.get("apikey", "")


@pytest.fixture(scope="session", autouse=True)
def setup_api_credentials(request):
    """
    Configure API credentials for integration tests.

    Resolution order:
      1. --apikey CLI flag  (pytest ... --apikey=YOUR_KEY)
      2. 'apikey' environment variable

    If neither is set, tests that call skip_if_no_api_key will be skipped,
    and AuthenticationError responses are caught and skipped automatically.
    """
    api_key = _resolve_api_key(request.config)
    te.login(api_key)
    print(f"\nAPI key: {'configured' if api_key else 'not set (integration tests will be skipped)'}")
    yield


@pytest.fixture
def skip_if_no_api_key(request):
    """Skip the test when no API key is available."""
    api_key = _resolve_api_key(request.config)
    if not api_key:
        pytest.skip(
            "No API key provided. Pass --apikey=YOUR_KEY or set the 'apikey' env var. "
            "Subscribe at https://tradingeconomics.com/api/pricing.aspx"
        )


@pytest.fixture(autouse=True)
def throttle_api_requests():
    """
    Add a 1-second delay after every test to respect API rate limits.
    Prevents HTTP 429 errors and temporary IP blocks.
    """
    yield
    time.sleep(1)


@pytest.fixture(autouse=True)
def skip_auth_failures_without_api_key(request):
    """
    Automatically skip tests that raise AuthenticationError when no API key is set.
    When a key IS set, the error is re-raised so it surfaces as a real failure.
    """
    try:
        yield
    except AuthenticationError as exc:
        api_key = _resolve_api_key(request.config)
        if not api_key:
            pytest.skip(f"Skipping endpoint requiring paid API access: {exc}")
        raise


# Pytest markers for organizing tests
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line(
        "markers", "requires_paid_api: marks tests that require paid API access"
    )

"""
Integration tests for tradingeconomics.calendar -- all public functions.

Each test requires a valid API key.  Run with:
    pytest tests/integration/calendar/test_calendar_basic.py -v --apikey=YOUR_KEY

Tests are skipped automatically when no key is available.
"""

import pytest
import tradingeconomics as te


@pytest.mark.integration
class TestGetCalendarData:
    """getCalendarData() -- basic parameter variations"""

    def test_no_params(self, skip_if_no_api_key):
        result = te.getCalendarData()
        assert isinstance(result, list) and len(result) > 0
        first = result[0]
        assert "Date" in first
        assert "Country" in first
        assert "Event" in first

    def test_single_country(self, skip_if_no_api_key):
        result = te.getCalendarData(country="united states")
        assert isinstance(result, list) and len(result) > 0
        countries = {e.get("Country", "") for e in result}
        assert any("United States" in c or "USA" in c for c in countries)

    def test_country_list(self, skip_if_no_api_key):
        result = te.getCalendarData(country=["united states", "china"])
        assert isinstance(result, list) and len(result) > 0

    def test_category(self, skip_if_no_api_key):
        result = te.getCalendarData(category="inflation rate")
        assert isinstance(result, list)

    def test_country_and_category(self, skip_if_no_api_key):
        result = te.getCalendarData(country="united states", category="inflation rate")
        assert isinstance(result, list)

    def test_date_range(self, skip_if_no_api_key):
        result = te.getCalendarData(initDate="2016-12-01", endDate="2016-12-03")
        assert isinstance(result, list)

    def test_country_with_date_range(self, skip_if_no_api_key):
        result = te.getCalendarData(
            country="united states",
            initDate="2016-12-01",
            endDate="2016-12-03",
        )
        assert isinstance(result, list)

    def test_importance_filter(self, skip_if_no_api_key):
        result = te.getCalendarData(importance="3")
        assert isinstance(result, list)

    def test_ticker(self, skip_if_no_api_key):
        result = te.getCalendarData(ticker="IJCUSA")
        assert isinstance(result, list)


@pytest.mark.integration
class TestGetCalendarId:
    """getCalendarId() -- fetch events by calendar ID"""

    def test_no_id(self, skip_if_no_api_key):
        result = te.getCalendarId()
        assert isinstance(result, list) and len(result) > 0


@pytest.mark.integration
class TestGetCalendarUpdates:
    """getCalendarUpdates() -- latest calendar updates"""

    def test_basic(self, skip_if_no_api_key):
        result = te.getCalendarUpdates()
        assert isinstance(result, list) and len(result) > 0
        assert isinstance(result[0], dict)


@pytest.mark.integration
class TestGetCalendarEvents:
    """getCalendarEvents() -- all events or by country"""

    def test_no_country(self, skip_if_no_api_key):
        result = te.getCalendarEvents()
        assert isinstance(result, list) and len(result) > 0

    def test_single_country(self, skip_if_no_api_key):
        result = te.getCalendarEvents(country="china")
        assert isinstance(result, list) and len(result) > 0

    def test_country_list(self, skip_if_no_api_key):
        result = te.getCalendarEvents(country=["china", "canada"])
        assert isinstance(result, list) and len(result) > 0


@pytest.mark.integration
class TestGetCalendarEventsByGroup:
    """getCalendarEventsByGroup() -- events filtered by group"""

    def test_group_only(self, skip_if_no_api_key):
        result = te.getCalendarEventsByGroup(group="inflation")
        assert isinstance(result, list) and len(result) > 0

    def test_country_and_group(self, skip_if_no_api_key):
        result = te.getCalendarEventsByGroup(country="china", group="inflation")
        assert isinstance(result, list)

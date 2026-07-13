"""
Integration tests for tradingeconomics.calendar -- filter combinations.

Covers multi-parameter combinations not tested in test_calendar_basic.py.

Run with:
    pytest tests/integration/calendar/test_calendar_filters.py -v --apikey=YOUR_KEY
"""

import pytest
import tradingeconomics as te


@pytest.mark.integration
class TestCalendarCombinedFilters:
    """getCalendarData() with multiple parameters combined"""

    def test_country_importance_date_range(self, skip_if_no_api_key):
        result = te.getCalendarData(
            country="united states",
            importance="3",
            initDate="2016-12-01",
            endDate="2016-12-31",
        )
        assert isinstance(result, list)

    def test_category_importance(self, skip_if_no_api_key):
        result = te.getCalendarData(category="inflation rate", importance="2")
        assert isinstance(result, list)

    def test_country_category_date_range(self, skip_if_no_api_key):
        result = te.getCalendarData(
            country="united states",
            category="initial jobless claims",
            initDate="2016-01-01",
            endDate="2016-06-01",
        )
        assert isinstance(result, list)

    def test_multiple_tickers(self, skip_if_no_api_key):
        result = te.getCalendarData(ticker=["IJCUSA", "SPAINFACORD"])
        assert isinstance(result, list)

    def test_values_flag(self, skip_if_no_api_key):
        result = te.getCalendarData(country="united states", values=True)
        assert isinstance(result, list)


@pytest.mark.integration
class TestCalendarEventsByGroupFilters:
    """getCalendarEventsByGroup() with date range"""

    def test_group_with_dates(self, skip_if_no_api_key):
        result = te.getCalendarEventsByGroup(
            group="inflation",
            initDate="2023-01-01",
            endDate="2023-02-01",
        )
        assert isinstance(result, list)

    def test_country_group_with_dates(self, skip_if_no_api_key):
        result = te.getCalendarEventsByGroup(
            country="china",
            group="inflation",
            initDate="2023-01-01",
            endDate="2023-02-01",
        )
        assert isinstance(result, list)

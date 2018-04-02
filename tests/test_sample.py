import pytest
import smartdates as sd


def test_week_start():
        pass


@pytest.mark.parametrize("expected, date", [
    ('2018-03-01', '2018-03-28'),
    ('2017-03-01', '2017-03-28'),
    ('2017-08-01', '2017-08-28'),
])
def test_month_start(expected, date):
    assert expected == sd.get_month_start(date)


@pytest.mark.parametrize("expected, date", [
    ('2018-01-01', '2018-03-28'),
    ('2017-01-01', '2017-03-28'),
    ('2017-07-01', '2017-08-28'),
])
def test_get_quarter_start(expected, date):
    assert expected == sd.get_quarter_start(date)


@pytest.mark.parametrize("expected, date", [
    ('2018-01-01', '2018-03-28'),
    ('2017-01-01', '2017-03-28'),
    ('2016-01-01', '2016-08-28'),
])
def test_year_start(expected, date):
    assert expected == sd.get_year_start(date)


@pytest.mark.parametrize("expected, date, years, months, days", [
    ('2018-04-05', '2018-03-30', 0, 0, 6),
    ('2018-02-28', '2018-03-31', 0, -1, 0),
])
def test_delta_date(expected, date, years, months, days):
    assert expected == sd.delta_date(date, years=years, months=months, days=days)


@pytest.mark.parametrize("expected, date, today", [
    (('2018-03-26', '2018-03-27'), 'this_week', '2018-03-28'),
    (('2018-03-19', '2018-03-25'), 'last_week', '2018-03-28'),
    (('2018-03-14', '2018-03-27'), 'last_14_days', '2018-03-28'),
    (('2018-02-26', '2018-03-27'), 'last_30_days', '2018-03-28'),
    (('2018-03-01', '2018-03-27'), 'this_month', '2018-03-28'),
    (('2018-02-01', '2018-02-28'), 'last_month', '2018-03-28'),
    (('2018-01-01', '2018-03-27'), 'this_quarter', '2018-03-28'),
    (('2017-10-01', '2017-12-31'), 'last_quarter', '2018-03-28'),
    (('2018-01-01', '2018-03-27'), 'this_year', '2018-03-28'),
    (('2017-01-01', '2017-12-31'), 'last_year', '2018-03-28'),
    (('2017-10-28', '2018-02-22'), ('2017-10-28', '2018-02-22'), '2018-03-28'),
])
def test_parse_query_dates(expected, date, today):
    assert expected == sd.parse_query_dates(date, today=today)


@pytest.mark.parametrize("current_date, previous_date", [
    ('this_week', 'same_period_last_month'),
    ('this_week', 'same_period_last_year'),
    ('this_week', 'same_period_last_quarter'),
    ('last_week', 'same_period_last_month'),
    ('last_week', 'same_period_last_year'),
    ('last_week', 'same_period_last_quarter'),
    ('last_7_days', 'same_period_last_month'),
    ('last_7_days', 'same_period_last_year'),
    ('last_7_days', 'same_period_last_quarter'),
    ('last_14_days', 'same_period_last_month'),
    ('last_14_days', 'same_period_last_year'),
    ('last_14_days', 'same_period_last_quarter'),
    ('last_30_days', 'same_period_last_month'),
    ('last_30_days', 'same_period_last_year'),
    ('last_30_days', 'same_period_last_quarter'),
    ('this_quarter', 'same_period_last_month'),
    ('this_quarter', 'same_period_last_quarter'),
    ('last_quarter', 'same_period_last_month'),
    ('last_quarter', 'same_period_last_quarter'),
    ('this_year', 'same_period_last_month'),
    ('this_year', 'same_period_last_year'),
    ('this_year', 'same_period_last_quarter'),
    ('last_year', 'same_period_last_month'),
    ('last_year', 'same_period_last_year'),
    ('last_year', 'same_period_last_quarter'),
])
def test_parse_relative_dates_invalid_arguments(current_date, previous_date):
    with pytest.raises(KeyError):
        sd.parse_relative_dates(current_date, previous_date)


@pytest.mark.parametrize("expected, current_date, previous_date, today", [
    ((('2018-03-26', '2018-03-27'), ('2018-03-19', '2018-03-20')), 'this_week', 'previous_period', '2018-03-28'),
    ((('2018-03-19', '2018-03-25'), ('2018-03-12', '2018-03-18')), 'last_week', 'previous_period', '2018-03-28'),
    ((('2018-03-21', '2018-03-27'), ('2018-03-14', '2018-03-20')), 'last_7_days', 'previous_period', '2018-03-28'),
    ((('2018-03-14', '2018-03-27'), ('2018-02-28', '2018-03-13')), 'last_14_days', 'previous_period', '2018-03-28'),
    ((('2018-02-26', '2018-03-27'), ('2018-01-27', '2018-02-25')), 'last_30_days', 'previous_period', '2018-03-28'),
    ((('2018-03-01', '2018-03-27'), ('2018-02-01', '2018-02-27')), 'this_month', 'previous_period', '2018-03-28'),
    ((('2018-03-01', '2018-03-30'), ('2018-02-01', '2018-02-28')), 'this_month', 'previous_period', '2018-03-31'),
    ((('2018-02-01', '2018-02-28'), ('2018-01-01', '2018-01-28')), 'this_month', 'previous_period', '2018-03-29'),
    ((('2018-03-01', '2018-03-27'), ('2017-03-01', '2017-03-27')), 'this_month', 'same_period_last_year', '2018-03-28'),
    ((('2016-02-01', '2018-03-29'), ('2015-02-01', '2015-02-28')), 'this_month', 'same_period_last_year', '2018-03-30'),
    ((('2016-02-01', '2018-03-29'), ('2015-02-01', '2015-02-28')), 'last_month', 'previous_period', '2016-03-28'),
    ((('2018-02-01', '2018-02-28'), ('2017-11-01', '2017-11-31')), 'last_month', 'same_period_last_quarter', '2016-03-02'),
    ((('2018-02-01', '2018-02-28'), ('2017-02-01', '2017-02-28')), 'last_month', 'same_period_last_quarter', '2016-03-28'),
    ((('2016-02-01', '2016-02-29'), ('2015-02-01', '2015-02-28')), 'last_month', 'same_period_last_quarter', '2016-03-02'),
    ((('2018-01-01', '2018-03-27'), ('2017-10-01', '2017-12-27')), 'this_quarter', 'previous_period', '2018-03-28'),
    ((('2018-01-01', '2018-03-27'), ('2017-01-01', '2017-03-27')), 'this_quarter', 'same_period_last_year', '2018-03-28'),
    ((('2017-10-01', '2017-12-31'), ('2017-07-01', '2017-09-30')), 'last_quarter', 'previous_period', '2018-03-28'),
    ((('2017-10-01', '2017-12-31'), ('2016-10-01', '2016-12-31')), 'last_quarter', 'same_period_last_year', '2018-03-28'),
    ((('2018-01-01', '2018-03-27'), ('2017-01-01', '2017-03-27')), 'this_year', 'previous_period', '2018-03-28'),
    ((('2017-01-01', '2017-12-31'), ('2016-01-01', '2016-12-31')), 'last_year', 'previous_period', '2018-03-28'),
])
def test_parse_relative_dates(expected, current_date, previous_date, today):
    assert expected == sd.parse_relative_dates(current_date=current_date, previous_date=previous_date, today=today)

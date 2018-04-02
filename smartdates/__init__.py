import datetime
from typing import TypeVar

DATE_FORMAT = "%Y-%m-%d"

SmartDate = TypeVar('SmartDate', tuple, str)


def delta_date(date: str, years=0, days=0, months=0) -> str:
    """returns a date with +/- years, days and/or months
    Args:
        date (str): The date you wish to modify as string in format YYYY-MM-DD
        years(int): How many years you want to add or subtract
        months(int): How many months you want to add or subtract
        days(int): How many days you want to add or subtract
    Returns:
        str: Date in format YYYY-MM-DD
        """

    parsed_date = datetime.datetime.strptime(date, DATE_FORMAT)
    new_year = parsed_date.year + years
    new_month = parsed_date.month + months
    start_day = parsed_date.day

    if new_month < 1:
        while new_month < 1:
            new_year -= 1
            new_month += 12
    elif new_month > 12:
        while new_month > 12:
            new_year += 1
            new_month -= 12

    try:
        new_date = datetime.date(year=new_year,
                                 month=new_month,
                                 day=start_day)
    except ValueError:
        raise ValueError('it is not possible to create date {}-{}-{}'.format(new_year, new_month, start_day))

    new_date = new_date + datetime.timedelta(days=days)

    return new_date.strftime(DATE_FORMAT)


def get_year_start(date: str) -> str:
    parsed_date = datetime.datetime.strptime(date, DATE_FORMAT)
    return datetime.date(parsed_date.year, 1, 1).strftime(DATE_FORMAT)


def get_quarter_start(date: str) -> str:
    """returns the date of the start of the quarter for the given date
    Args:
        date (str): The date you want to get the start of the quarter for in format YYYY-MM-DD
    Returns:
     str:  Date in string format YYYY-MM-DD"""
    parsed_date = datetime.datetime.strptime(date, DATE_FORMAT)
    return datetime.date(parsed_date.year, (parsed_date.month - 1) // 3 * 3 + 1, 1).strftime(DATE_FORMAT)


def get_month_start(date: str) -> str:
    parsed_date = datetime.datetime.strptime(date, DATE_FORMAT)
    return datetime.date(parsed_date.year, parsed_date.month, 1).strftime(DATE_FORMAT)


def get_week_start(date: str) -> str:
    """returns the date of the start of the week for the given date
    Args:
        date (str): The date you want to get the start of the quarter for in format YYYY-MM-DD
    Returns:
     str:  Date in string format YYYY-MM-DD"""

    parsed_date = datetime.datetime.strptime(date, DATE_FORMAT)
    return (parsed_date - datetime.timedelta(days=parsed_date.weekday())).strftime(DATE_FORMAT)


def get_week_end(date: str) -> str:
    """returns the date of the end of the week for the given date
    Args:
        date (str): The date you want to get the start of the quarter for in format YYYY-MM-DD
    Returns:
     str:  Date in string format YYYY-MM-DD"""

    week_start = datetime.datetime.strptime(get_week_start(date), DATE_FORMAT)
    return (week_start + datetime.timedelta(days=6)).strftime(DATE_FORMAT)


def parse_query_dates(date: SmartDate, today=datetime.date.today().strftime(DATE_FORMAT)) -> tuple:
    """It gets the start and end date, if there is no end date, it is set to yesterday, if there is no start dante, it
    is set to 30 days before of the end date
    Args:
        date (str): start date in format YYYY-MM-DD

    Returns:
        tuple: a tuple containing the new start_date and end_date
        """
    if not isinstance(date, str):
        return date[0], date[1]

    valid_smart_dates = ['yesterday', 'this_week', 'last_week', 'last_7_days', 'last_14_days', 'last_30_days',
                         'this_month', 'last_month', 'this_quarter', 'last_quarter', 'this_year', 'last_year']
    if date not in valid_smart_dates:
        raise KeyError("{} smart date is not avilable".format(date))

    if date == 'yesterday':
        start_date = end_date = delta_date(today, days=-1)
    elif date == 'this_week':
        start_date, end_date = get_week_start(today), delta_date(today, days=-1)
    elif date == 'last_week':
        start_date = get_week_start(delta_date(today, days=-7))
        end_date = get_week_end(start_date)
    elif date == 'last_7_days':
        start_date = delta_date(today, days=-7)
        end_date = delta_date(today, days=-1)
    elif date == 'last_14_days':
        start_date = delta_date(today, days=-14)
        end_date = delta_date(today, days=-1)
    elif date == 'last_30_days':
        start_date = delta_date(today, days=-30)
        end_date = delta_date(today, days=-1)
    elif date == 'this_month':
        start_date = get_month_start(today)
        end_date = delta_date(today, days=-1)
    elif date == 'last_month':
        end_date = delta_date(get_month_start(today), days=-1)
        start_date = get_month_start(end_date)
    elif date == 'this_quarter':
        start_date = get_quarter_start(today)
        end_date = delta_date(today, days=-1)
    elif date == 'last_quarter':
        end_date = delta_date(get_quarter_start(today), days=-1)
        start_date = get_quarter_start(end_date)
    elif date == 'this_year':
        start_date = get_year_start(today)
        end_date = delta_date(today, days=-1)
    elif date == 'last_year':
        end_date = delta_date(get_year_start(today), days=-1)
        start_date = get_year_start(end_date)
    else:
        raise TypeError('date is not valid')

    return start_date, end_date


def parse_relative_dates(current_date: SmartDate,
                         previous_date: SmartDate,
                         today=datetime.date.today().strftime(DATE_FORMAT)):
    if (current_date == 'this_week'
            or current_date == 'last_week'
            or current_date == 'last_7_days'):
        if previous_date == 'previous_period':
            parsed_current_date = parse_query_dates(current_date, today=today)
            parsed_previous_date = (delta_date(parsed_current_date[0], days=-7),
                                    delta_date(parsed_current_date[1], days=-7))

        else:
            raise KeyError

    elif current_date == 'last_14_days':
        if previous_date == 'previous_period':
            parsed_current_date = parse_query_dates(current_date, today=today)
            parsed_previous_date = (delta_date(parsed_current_date[0], days=-14),
                                    delta_date(parsed_current_date[1], days=-14))

        else:
            raise KeyError

    elif current_date == 'last_30_days':
        if previous_date == 'previous_period':
            parsed_current_date = parse_query_dates(current_date, today=today)
            parsed_previous_date = (delta_date(parsed_current_date[0], days=-30),
                                    delta_date(parsed_current_date[1], days=-30))

        else:
            raise KeyError

    elif current_date == 'this_month':
        parsed_current_date = parse_query_dates(current_date, today=today)
        if previous_date == 'previous_period':
            parsed_previous_date = (delta_date(parsed_current_date[0], months=-1),
                                    delta_date(parsed_current_date[1], months=-1))

        elif previous_date == 'same_period_last_year':
            parsed_previous_date = (delta_date(parsed_current_date[0], years=-1),
                                    delta_date(parsed_current_date[1], years=-1))
        else:
            raise KeyError

    elif current_date == 'last_month':
        parsed_current_date = parse_query_dates(current_date, today=today)
        if previous_date == 'previous_period':
            parsed_previous_date = (delta_date(parsed_current_date[0], months=-1),
                                    delta_date(parsed_current_date[1], months=-1))

        elif previous_date == 'same_period_last_quarter':
            parsed_previous_date = (delta_date(parsed_current_date[0], months=-3),
                                    delta_date(parsed_current_date[1], months=-3))
        elif previous_date == 'same_period_last_year':
            parsed_previous_date = (delta_date(parsed_current_date[0], years=-1),
                                    delta_date(parsed_current_date[1], years=-1))
        else:
            raise KeyError
    elif current_date == 'this_quarter':
        parsed_current_date = parse_query_dates(current_date, today=today)
        if previous_date == 'previous_period':
            parsed_previous_date = (delta_date(parsed_current_date[0], months=-3),
                                    delta_date(parsed_current_date[1], months=-3))

        elif previous_date == 'same_period_last_year':
            parsed_previous_date = (delta_date(parsed_current_date[0], years=-1),
                                    delta_date(parsed_current_date[1], years=-1))
        else:
            raise KeyError

    elif current_date == 'last_quarter':
        parsed_current_date = parse_query_dates(current_date, today=today)
        if previous_date == 'previous_period':
            previous_end_date = delta_date(parsed_current_date[0], days=-1)
            previous_start_date = get_quarter_start(previous_end_date)

            parsed_previous_date = (previous_start_date,
                                    previous_end_date)

        elif previous_date == 'same_period_last_year':
            parsed_previous_date = (delta_date(parsed_current_date[0], years=-1),
                                    delta_date(parsed_current_date[1], years=-1))
        else:
            raise KeyError

    elif current_date == 'this_year' or current_date == 'last_year':
        parsed_current_date = parse_query_dates(current_date, today=today)
        if previous_date == 'previous_period':
            parsed_previous_date = (delta_date(parsed_current_date[0], years=-1),
                                    delta_date(parsed_current_date[1], years=-1))
        else:
            raise KeyError
    else:
        raise KeyError

    return parsed_current_date, parsed_previous_date

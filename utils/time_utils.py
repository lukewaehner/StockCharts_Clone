import datetime
from datetime import timedelta
from config import TIME_RANGES


def calculate_time_range(selected_time_range):
    """
    Calculate the number of weekdays to go back based on selected time range.

    Args:
        selected_time_range (str): The selected time range

    Returns:
        int: Negative number representing days to go back, or 0 for max
    """
    today = datetime.date.today()
    weekday_count = 0

    # Handle YTD (Year to Date) case
    if selected_time_range == 'ytd' or TIME_RANGES.get(selected_time_range) == 'ytd':
        start_of_year = datetime.date(today.year, 1, 3)
        for single_date in (start_of_year + timedelta(days=n)
                            for n in range((today - start_of_year).days + 1)):
            if single_date.weekday() < 5:  # Monday-Friday
                weekday_count += 1
        return -weekday_count

    # Handle normal time ranges
    logged_days = TIME_RANGES.get(selected_time_range, 0)
    if logged_days == 'max':
        return 0

    logged_days = int(logged_days)
    while logged_days > 0:
        if today.weekday() < 5:
            weekday_count += 1
        today = today - timedelta(days=1)
        logged_days -= 1

    return -weekday_count


def get_date_range_from_data(data, time_range):
    """
    Get the appropriate date range from historical data.

    Args:
        data (pd.DataFrame): Historical stock data
        time_range (str): Selected time range

    Returns:
        tuple: (start_date, end_date)
    """
    if len(data.index) == 0:
        return None, None

    time_offset = calculate_time_range(time_range)

    if len(data.index) < abs(time_offset) or time_offset == 0:
        start_date = data.index[0]
    else:
        start_date = data.index[time_offset]

    end_date = data.index[-1]
    return start_date, end_date

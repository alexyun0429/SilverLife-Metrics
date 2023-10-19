import json
import datetime
import pytz


def convertStressDataSet(data):
    """
    Convert and process the given stress data set, providing results in a specific format.

    This function parses the input JSON data, extracts stress details, and processes
    the stress level to categorize it into different categories (e.g., 'Rest', 'Low', 'Medium', 'High').
    The timestamps in the data are converted to the Australia/Brisbane timezone.

    Parameters:
    - data (bytes): The stress data in JSON format, encoded as bytes.

    Returns:
    - list of tuples: Each tuple contains:
        - An initial placeholder (None).
        - User access token.
        - Local date in 'YYYY-MM-DD' format.
        - Local time in 'HH:MM:SS %Z%z' format.
        - Stress value as a string.
        - Stress status (e.g., 'Rest', 'Low', 'Medium', 'High').
    """
    # Load the data
    data = json.loads(str(data, encoding="utf-8"))
    results = []
    stress_details = data["stressDetails"]

    brisbane_tz = pytz.timezone("Australia/Brisbane")

    for detail in stress_details:
        user_access_token = detail["userAccessToken"]
        start_time_in_seconds = detail["startTimeInSeconds"]
        start_time_offset_in_seconds = detail["startTimeOffsetInSeconds"]

        time_offset_stress_level_values = detail["timeOffsetStressLevelValues"]

        for offset, stress_value in time_offset_stress_level_values.items():
            if stress_value < 1:
                continue

            if stress_value <= 25:
                stress_status = "Rest"
            elif stress_value <= 50:
                stress_status = "Low"
            elif stress_value <= 75:
                stress_status = "Medium"
            else:
                stress_status = "High"

            local_date_time = datetime.datetime.fromtimestamp(
                start_time_in_seconds + start_time_offset_in_seconds + int(offset),
                brisbane_tz,
            )

            local_date = local_date_time.strftime("%Y-%m-%d")
            local_time = local_date_time.strftime("%H:%M:%S %Z%z")

            results.append(
                (
                    None,
                    user_access_token,
                    str(local_date),
                    local_time,
                    str(stress_value),
                    stress_status,
                )
            )

    return results

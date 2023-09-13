import json
import datetime
import pytz

data = """

"""

# Load the data
data = json.loads(data)

stress_details = data['stressDetails']

brisbane_tz = pytz.timezone('Australia/Brisbane')

for detail in stress_details:
    user_access_token = detail['userAccessToken']
    start_time_in_seconds = detail['startTimeInSeconds']
    start_time_offset_in_seconds = detail['startTimeOffsetInSeconds']

    time_offset_stress_level_values = detail['timeOffsetStressLevelValues']

    for offset, stress_value in time_offset_stress_level_values.items():
        local_date_time = datetime.datetime.fromtimestamp(start_time_in_seconds + start_time_offset_in_seconds + int(offset), brisbane_tz)

        print(f"Local Date Time: {local_date_time}, Stress Level Value: {stress_value}")
        print(f"User Access Token: {user_access_token}")
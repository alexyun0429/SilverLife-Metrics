import json
import datetime
import pytz

def convertDataTime (data):
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
        if stress_value < 1:
            continue

        if stress_value <= 25:
            stress_status = 'Rest'
        elif stress_value <= 50:
            stress_status = 'Low'
        elif stress_value <= 75:
            stress_status = 'Medium'
        else:
            stress_status = 'High'

        local_date_time = datetime.datetime.fromtimestamp(start_time_in_seconds + start_time_offset_in_seconds + int(offset), brisbane_tz)

        # wanted to name this as just "date" & "time" but it's preoccupied name in sql
        # so named as "local_***"
        local_date = local_date_time.date()
        local_time = local_date_time.time()

        # print(f"Local Date: {local_date}")
        # print(f"Local Time: {local_time}")
        # print(f"Stress Level Value: {stress_value}")
        # print(f"Stress Status: {stress_status}")
        # print(f"User Access Token: {user_access_token}")
         results.append({
                'User Access Token': user_access_token,
                'Local Date': local_date,
                'Local Time': local_time,
                'Stress Level Value': stress_value,
                'Stress Status': stress_status
            })

    return results 


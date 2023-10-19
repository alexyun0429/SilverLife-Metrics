import json
import datetime
import pytz
import sys


def convertHrvDataSet(data):
    # Load the data
    data = json.loads(str(data, encoding="utf-8"))
    results = []
    hrv_details = data["hrv"]

    brisbane_tz = pytz.timezone("Australia/Brisbane")

    for detail in hrv_details:
        summaryId = detail["summaryId"]
        start_time_in_seconds = detail["startTimeInSeconds"]
        start_time_offset_in_seconds = detail["startTimeOffsetInSeconds"]

        hrvValues = detail["hrvValues"]

        for offset, hrv_value in hrvValues.items():
            if not hrv_value: # no entry
                continue

            local_date_time = datetime.datetime.fromtimestamp(
                start_time_in_seconds + start_time_offset_in_seconds + int(offset),
                brisbane_tz,
            )

            local_date = local_date_time.strftime("%Y-%m-%d")
            local_time = local_date_time.strftime("%H:%M:%S %Z%z")

            results.append(
                (
                    None, # auto increment
                    summaryId,
                    #user_access_token, # varchar 
                    str(local_date), # date 
                    local_time, # time
                    hrv_value, # int
                )
            )
    print(results, file=sys.stdout, flush=True)
    return results

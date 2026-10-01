import pandas as pd

# --------------------------------------------------
# File paths
# --------------------------------------------------

input_file = "data/flights_cleaned.csv"

# --------------------------------------------------
# Variables for calculations
# --------------------------------------------------

month_summary = {}
day_summary = {}
hour_summary = {}

chunk_size = 100000


# --------------------------------------------------
# Process flights in chunks
# --------------------------------------------------

for chunk in pd.read_csv(
    input_file,
    chunksize=chunk_size,
    low_memory=False
):

    # ----------------------------------------------
    # Create delayed flag
    # ----------------------------------------------

    chunk["delayed"] = (
        chunk["ARRIVAL_DELAY"] > 0
    ).astype(int)


    # ==============================================
    # Q12 - MONTH ANALYSIS
    # ==============================================

    grouped_month = chunk.groupby("MONTH").agg(
        total_flights=("MONTH", "size"),
        delayed_flights=("delayed", "sum")
    )

    for month, row in grouped_month.iterrows():

        if month not in month_summary:
            month_summary[month] = {
                "total_flights": 0,
                "delayed_flights": 0
            }

        month_summary[month]["total_flights"] += int(
            row["total_flights"]
        )

        month_summary[month]["delayed_flights"] += int(
            row["delayed_flights"]
        )


    # ==============================================
    # Q13 - DAY OF WEEK ANALYSIS
    # ==============================================

    grouped_day = chunk.groupby("DAY_OF_WEEK").agg(
        total_flights=("DAY_OF_WEEK", "size"),
        delayed_flights=("delayed", "sum")
    )

    for day, row in grouped_day.iterrows():

        if day not in day_summary:
            day_summary[day] = {
                "total_flights": 0,
                "delayed_flights": 0
            }

        day_summary[day]["total_flights"] += int(
            row["total_flights"]
        )

        day_summary[day]["delayed_flights"] += int(
            row["delayed_flights"]
        )


    # ==============================================
    # Q14 - DEPARTURE HOUR ANALYSIS
    # ==============================================

    # Convert departure time to numeric
    departure_time = pd.to_numeric(
        chunk["DEPARTURE_TIME"],
        errors="coerce"
    )

    # Remove missing departure times
    valid_departures = chunk[
        departure_time.notna()
    ].copy()

    departure_time = departure_time[
        departure_time.notna()
    ]

    # Convert HHMM format to hour
    valid_departures["departure_hour"] = (
        departure_time // 100
    ).astype(int)

    grouped_hour = valid_departures.groupby(
        "departure_hour"
    ).agg(
        total_flights=("departure_hour", "size"),
        delayed_flights=("delayed", "sum")
    )

    for hour, row in grouped_hour.iterrows():

        if hour not in hour_summary:
            hour_summary[hour] = {
                "total_flights": 0,
                "delayed_flights": 0
            }

        hour_summary[hour]["total_flights"] += int(
            row["total_flights"]
        )

        hour_summary[hour]["delayed_flights"] += int(
            row["delayed_flights"]
        )


    print("Processed a chunk...")


# ==================================================
# CREATE MONTH DATAFRAME
# ==================================================

month_df = pd.DataFrame.from_dict(
    month_summary,
    orient="index"
)

month_df.index.name = "month"

month_df.reset_index(inplace=True)

month_df["delay_rate"] = (
    month_df["delayed_flights"]
    * 100
    / month_df["total_flights"]
)

month_df["delay_rate"] = month_df["delay_rate"].round(2)

month_df = month_df.sort_values(
    "delayed_flights",
    ascending=False
)


# ==================================================
# CREATE DAY DATAFRAME
# ==================================================

day_df = pd.DataFrame.from_dict(
    day_summary,
    orient="index"
)

day_df.index.name = "day_of_week"

day_df.reset_index(inplace=True)

day_df["delay_rate"] = (
    day_df["delayed_flights"]
    * 100
    / day_df["total_flights"]
)

day_df["delay_rate"] = day_df["delay_rate"].round(2)

day_df = day_df.sort_values(
    "delayed_flights",
    ascending=False
)


# ==================================================
# CREATE HOUR DATAFRAME
# ==================================================

hour_df = pd.DataFrame.from_dict(
    hour_summary,
    orient="index"
)

hour_df.index.name = "departure_hour"

hour_df.reset_index(inplace=True)

hour_df["delay_rate"] = (
    hour_df["delayed_flights"]
    * 100
    / hour_df["total_flights"]
)

hour_df["delay_rate"] = hour_df["delay_rate"].round(2)

hour_df = hour_df.sort_values(
    "delayed_flights",
    ascending=False
)


# ==================================================
# SAVE SUMMARY FILES
# ==================================================

month_df.to_csv(
    "data/month_summary.csv",
    index=False
)

day_df.to_csv(
    "data/day_summary.csv",
    index=False
)

hour_df.to_csv(
    "data/hour_summary.csv",
    index=False
)


# ==================================================
# DISPLAY Q12
# ==================================================

print("\n================================")
print("Q12 - MONTHS WITH MOST DELAYS")
print("================================")

print(
    month_df[
        [
            "month",
            "total_flights",
            "delayed_flights",
            "delay_rate"
        ]
    ].to_string(index=False)
)


# ==================================================
# DISPLAY Q13
# ==================================================

print("\n================================")
print("Q13 - DAYS OF WEEK WITH MOST DELAYS")
print("================================")

print(
    day_df[
        [
            "day_of_week",
            "total_flights",
            "delayed_flights",
            "delay_rate"
        ]
    ].to_string(index=False)
)


# ==================================================
# DISPLAY Q14
# ==================================================

print("\n================================")
print("Q14 - DEPARTURE HOURS WITH MOST DELAYS")
print("================================")

print(
    hour_df[
        [
            "departure_hour",
            "total_flights",
            "delayed_flights",
            "delay_rate"
        ]
    ].to_string(index=False)
)


print("\n================================")
print("TIME ANALYSIS COMPLETED!")
print("================================")
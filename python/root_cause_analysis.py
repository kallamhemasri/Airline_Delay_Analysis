import pandas as pd

# --------------------------------------------------
# File paths
# --------------------------------------------------

input_file = "data/flights_cleaned.csv"
airlines_file = "data/airlines.csv"

chunk_size = 100000


# --------------------------------------------------
# Variables for calculations
# --------------------------------------------------

cause_totals = {
    "AIR_SYSTEM_DELAY": 0,
    "SECURITY_DELAY": 0,
    "AIRLINE_DELAY": 0,
    "LATE_AIRCRAFT_DELAY": 0,
    "WEATHER_DELAY": 0
}

airline_causes = {}

airport_causes = {}


# --------------------------------------------------
# Process data in chunks
# --------------------------------------------------

for chunk in pd.read_csv(
    input_file,
    chunksize=chunk_size,
    low_memory=False
):

    # ----------------------------------------------
    # Q15 - Major causes of delays
    # ----------------------------------------------

    for cause in cause_totals:

        cause_totals[cause] += chunk[cause].sum()


    # ----------------------------------------------
    # Q16 & Q17 - Airline causes
    # ----------------------------------------------

    grouped_airline = chunk.groupby("AIRLINE").agg(
        weather_delay=("WEATHER_DELAY", "sum"),
        late_aircraft_delay=("LATE_AIRCRAFT_DELAY", "sum")
    )

    for airline, row in grouped_airline.iterrows():

        if airline not in airline_causes:

            airline_causes[airline] = {
                "weather_delay": 0,
                "late_aircraft_delay": 0
            }

        airline_causes[airline]["weather_delay"] += int(
            row["weather_delay"]
        )

        airline_causes[airline]["late_aircraft_delay"] += int(
            row["late_aircraft_delay"]
        )


    # ----------------------------------------------
    # Q18 - Airport causes
    # ----------------------------------------------

    grouped_airport = chunk.groupby("ORIGIN_AIRPORT").agg(
        weather_delay=("WEATHER_DELAY", "sum"),
        air_system_delay=("AIR_SYSTEM_DELAY", "sum")
    )

    for airport, row in grouped_airport.iterrows():

        if airport not in airport_causes:

            airport_causes[airport] = {
                "weather_delay": 0,
                "air_system_delay": 0
            }

        airport_causes[airport]["weather_delay"] += int(
            row["weather_delay"]
        )

        airport_causes[airport]["air_system_delay"] += int(
            row["air_system_delay"]
        )


    print("Processed a chunk...")


# ==================================================
# Q15 - MAJOR DELAY CAUSES
# ==================================================

cause_df = pd.DataFrame(
    list(cause_totals.items()),
    columns=["cause", "total_delay_minutes"]
)

cause_df["total_delay_minutes"] = (
    cause_df["total_delay_minutes"].round(0)
)

cause_df = cause_df.sort_values(
    "total_delay_minutes",
    ascending=False
)


# ==================================================
# Q16 & Q17 - AIRLINE CAUSES
# ==================================================

airline_df = pd.DataFrame.from_dict(
    airline_causes,
    orient="index"
)

airline_df.index.name = "airline_code"

airline_df.reset_index(inplace=True)

airline_df = airline_df.sort_values(
    "weather_delay",
    ascending=False
)


# ==================================================
# Q18 - AIRPORT CAUSES
# ==================================================

airport_df = pd.DataFrame.from_dict(
    airport_causes,
    orient="index"
)

airport_df.index.name = "airport_code"

airport_df.reset_index(inplace=True)

airport_df = airport_df.sort_values(
    "weather_delay",
    ascending=False
)


# ==================================================
# SAVE RESULTS
# ==================================================

cause_df.to_csv(
    "data/delay_cause_summary.csv",
    index=False
)

airline_df.to_csv(
    "data/airline_cause_summary.csv",
    index=False
)

airport_df.to_csv(
    "data/airport_cause_summary.csv",
    index=False
)


# ==================================================
# DISPLAY Q15
# ==================================================

print("\n================================")
print("Q15 - MAJOR CAUSES OF DELAYS")
print("================================")

print(
    cause_df.to_string(index=False)
)


# ==================================================
# DISPLAY Q16
# ==================================================

print("\n================================")
print("Q16 - AIRLINES MOST AFFECTED BY WEATHER DELAYS")
print("================================")

print(
    airline_df[
        [
            "airline_code",
            "weather_delay",
            "late_aircraft_delay"
        ]
    ].head(14).to_string(index=False)
)


# ==================================================
# DISPLAY Q17
# ==================================================

print("\n================================")
print("Q17 - AIRLINES MOST AFFECTED BY LATE AIRCRAFT DELAYS")
print("================================")

print(
    airline_df
    .sort_values(
        "late_aircraft_delay",
        ascending=False
    )[
        [
            "airline_code",
            "late_aircraft_delay",
            "weather_delay"
        ]
    ]
    .head(14)
    .to_string(index=False)
)


# ==================================================
# DISPLAY Q18
# ==================================================

print("\n================================")
print("Q18 - AIRPORTS WITH HIGHEST WEATHER/SYSTEM DELAYS")
print("================================")

print(
    airport_df[
        [
            "airport_code",
            "weather_delay",
            "air_system_delay"
        ]
    ].head(20).to_string(index=False)
)


print("\n================================")
print("ROOT CAUSE ANALYSIS COMPLETED!")
print("================================")
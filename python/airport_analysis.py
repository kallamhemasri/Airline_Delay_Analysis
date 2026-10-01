import pandas as pd

input_file = "data/flights_cleaned.csv"
airports_file = "data/airports.csv"

output_file = "data/airport_summary.csv"

chunk_size = 100000

airport_summary = {}

for chunk in pd.read_csv(
    input_file,
    chunksize=chunk_size,
    low_memory=False
):

    # --------------------------------
    # Create delayed flag
    # --------------------------------
    chunk["delayed"] = (
        chunk["ARRIVAL_DELAY"] > 0
    ).astype(int)


    # =================================
    # ORIGIN AIRPORT ANALYSIS
    # =================================

    origin_group = chunk.groupby("ORIGIN_AIRPORT").agg(
        origin_flights=("ORIGIN_AIRPORT", "size"),
        origin_delayed_flights=("delayed", "sum")
    )


    # =================================
    # DESTINATION AIRPORT ANALYSIS
    # =================================

    destination_group = chunk.groupby("DESTINATION_AIRPORT").agg(
        destination_flights=("DESTINATION_AIRPORT", "size"),
        destination_delayed_flights=("delayed", "sum")
    )


    # =================================
    # STORE ORIGIN RESULTS
    # =================================

    for airport, row in origin_group.iterrows():

        if airport not in airport_summary:
            airport_summary[airport] = {
                "origin_flights": 0,
                "origin_delayed_flights": 0,
                "destination_flights": 0,
                "destination_delayed_flights": 0
            }

        airport_summary[airport]["origin_flights"] += int(
            row["origin_flights"]
        )

        airport_summary[airport]["origin_delayed_flights"] += int(
            row["origin_delayed_flights"]
        )


    # =================================
    # STORE DESTINATION RESULTS
    # =================================

    for airport, row in destination_group.iterrows():

        if airport not in airport_summary:
            airport_summary[airport] = {
                "origin_flights": 0,
                "origin_delayed_flights": 0,
                "destination_flights": 0,
                "destination_delayed_flights": 0
            }

        airport_summary[airport]["destination_flights"] += int(
            row["destination_flights"]
        )

        airport_summary[airport]["destination_delayed_flights"] += int(
            row["destination_delayed_flights"]
        )


    print("Processed a chunk...")


# =================================
# CREATE DATAFRAME
# =================================

summary_df = pd.DataFrame.from_dict(
    airport_summary,
    orient="index"
)

summary_df.index.name = "airport_code"

summary_df.reset_index(inplace=True)


# =================================
# CALCULATE DELAY RATES
# =================================

summary_df["origin_delay_rate"] = (
    summary_df["origin_delayed_flights"]
    * 100
    / summary_df["origin_flights"]
)

summary_df["destination_delay_rate"] = (
    summary_df["destination_delayed_flights"]
    * 100
    / summary_df["destination_flights"]
)


summary_df["origin_delay_rate"] = (
    summary_df["origin_delay_rate"].round(2)
)

summary_df["destination_delay_rate"] = (
    summary_df["destination_delay_rate"].round(2)
)


# =================================
# SAVE RESULT
# =================================

# Keep only valid 3-letter airport codes
powerbi_df = summary_df[
    summary_df["airport_code"].str.len() == 3
].copy()

powerbi_df.to_csv(
    output_file,
    index=False
)


print("\n================================")
print("AIRPORT ANALYSIS COMPLETED!")
print("================================")

print("\nTotal airports found:")
print(len(summary_df))

print("\nSummary file created:")
print(output_file)


# =================================
# QUESTION 9
# =================================

print("\n================================")
print("Q9 - TOP ORIGIN AIRPORTS BY DELAY RATE")
print("================================")

q9 = summary_df[
    (summary_df["airport_code"].str.len() == 3) &
    (summary_df["origin_flights"] >= 1000)
].sort_values(
    "origin_delay_rate",
    ascending=False
).head(20)

print(
    q9[
        [
            "airport_code",
            "origin_flights",
            "origin_delayed_flights",
            "origin_delay_rate"
        ]
    ].to_string(index=False)
)


# =================================
# QUESTION 10
# =================================

print("\n================================")
print("Q10 - TOP DESTINATION AIRPORTS BY DELAY RATE")
print("================================")

q10 = summary_df[
    (summary_df["airport_code"].str.len() == 3) &
    (summary_df["destination_flights"] >= 1000)
].sort_values(
    "destination_delay_rate",
    ascending=False
).head(20)

print(
    q10[
        [
            "airport_code",
            "destination_flights",
            "destination_delayed_flights",
            "destination_delay_rate"
        ]
    ].to_string(index=False)
)


# =================================
# QUESTION 11
# =================================

print("\n================================")
print("Q11 - AIRPORTS HANDLING THE MOST FLIGHTS")
print("================================")

summary_df["total_airport_flights"] = (
    summary_df["origin_flights"]
    + summary_df["destination_flights"]
)

q11 = summary_df.sort_values(
    "total_airport_flights",
    ascending=False
).head(20)

print(
    q11[
        [
            "airport_code",
            "origin_flights",
            "destination_flights",
            "total_airport_flights"
        ]
    ].to_string(index=False)
)
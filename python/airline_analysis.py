import pandas as pd

# --------------------------------------------------
# File paths
# --------------------------------------------------

input_file = "data/flights_cleaned.csv"
airlines_file = "data/airlines.csv"
output_file = "data/airline_summary.csv"


# --------------------------------------------------
# Variables for airline-level calculations
# --------------------------------------------------

airline_summary = {}

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


    # ----------------------------------------------
    # Group by airline
    # ----------------------------------------------

    grouped = chunk.groupby("AIRLINE").agg(
        total_flights=("AIRLINE", "size"),
        delayed_flights=("delayed", "sum"),
        cancelled_flights=("CANCELLED", "sum"),
        diverted_flights=("DIVERTED", "sum")
    )


    # ----------------------------------------------
    # Add results to overall summary
    # ----------------------------------------------

    for airline_code, row in grouped.iterrows():

        if airline_code not in airline_summary:
            airline_summary[airline_code] = {
                "total_flights": 0,
                "delayed_flights": 0,
                "cancelled_flights": 0,
                "diverted_flights": 0
            }

        airline_summary[airline_code]["total_flights"] += int(
            row["total_flights"]
        )

        airline_summary[airline_code]["delayed_flights"] += int(
            row["delayed_flights"]
        )

        airline_summary[airline_code]["cancelled_flights"] += int(
            row["cancelled_flights"]
        )

        airline_summary[airline_code]["diverted_flights"] += int(
            row["diverted_flights"]
        )

    print("Processed a chunk...")


# --------------------------------------------------
# Convert dictionary to DataFrame
# --------------------------------------------------

summary_df = pd.DataFrame.from_dict(
    airline_summary,
    orient="index"
)

summary_df.index.name = "airline_code"

summary_df.reset_index(inplace=True)


# --------------------------------------------------
# Calculate percentages
# --------------------------------------------------

summary_df["delayed_percentage"] = (
    summary_df["delayed_flights"]
    * 100
    / summary_df["total_flights"]
)

summary_df["cancellation_rate"] = (
    summary_df["cancelled_flights"]
    * 100
    / summary_df["total_flights"]
)

summary_df["diversion_rate"] = (
    summary_df["diverted_flights"]
    * 100
    / summary_df["total_flights"]
)


# --------------------------------------------------
# Round percentages
# --------------------------------------------------

summary_df["delayed_percentage"] = (
    summary_df["delayed_percentage"].round(2)
)

summary_df["cancellation_rate"] = (
    summary_df["cancellation_rate"].round(2)
)

summary_df["diversion_rate"] = (
    summary_df["diversion_rate"].round(2)
)


# --------------------------------------------------
# Add airline names
# --------------------------------------------------

airlines_df = pd.read_csv(airlines_file)

summary_df = summary_df.merge(
    airlines_df,
    left_on="airline_code",
    right_on="IATA_CODE",
    how="left"
)


# --------------------------------------------------
# Rename airline name column
# --------------------------------------------------

summary_df.rename(
    columns={
        "AIRLINE": "airline_name"
    },
    inplace=True
)


# --------------------------------------------------
# Keep useful columns
# --------------------------------------------------

summary_df = summary_df[
    [
        "airline_code",
        "airline_name",
        "total_flights",
        "delayed_flights",
        "delayed_percentage",
        "cancelled_flights",
        "cancellation_rate",
        "diverted_flights",
        "diversion_rate"
    ]
]


# --------------------------------------------------
# Sort by delay percentage
# --------------------------------------------------

summary_df = summary_df.sort_values(
    "delayed_percentage",
    ascending=False
)


# --------------------------------------------------
# Save result
# --------------------------------------------------

summary_df.to_csv(
    output_file,
    index=False
)


# --------------------------------------------------
# Display result
# --------------------------------------------------

print("\n================================")
print("AIRLINE ANALYSIS COMPLETED!")
print("================================")

print(summary_df.to_string(index=False))

print("\nSummary file created:")
print(output_file)
import pandas as pd
import os

# --------------------------------------------------
# File paths
# --------------------------------------------------

input_file = "data/flights.csv"
output_file = "data/flights_cleaned.csv"

# --------------------------------------------------
# Columns where missing values mean "no recorded delay"
# --------------------------------------------------

delay_columns = [
    "AIR_SYSTEM_DELAY",
    "SECURITY_DELAY",
    "AIRLINE_DELAY",
    "LATE_AIRCRAFT_DELAY",
    "WEATHER_DELAY"
]

# --------------------------------------------------
# Process the large CSV in chunks
# --------------------------------------------------

chunk_size = 100000

first_chunk = True
total_rows = 0

for chunk in pd.read_csv(
    input_file,
    chunksize=chunk_size,
    low_memory=False
):

    # ----------------------------------------------
    # 1. Replace missing cancellation reason
    # ----------------------------------------------

    chunk["CANCELLATION_REASON"] = (
        chunk["CANCELLATION_REASON"]
        .fillna("Not Cancelled")
    )

    # ----------------------------------------------
    # 2. Replace missing delay causes with 0
    # ----------------------------------------------

    chunk[delay_columns] = (
        chunk[delay_columns]
        .fillna(0)
    )

    # ----------------------------------------------
    # 3. Write cleaned chunk to output file
    # ----------------------------------------------

    chunk.to_csv(
        output_file,
        mode="w" if first_chunk else "a",
        header=first_chunk,
        index=False
    )

    first_chunk = False
    total_rows += len(chunk)

    print(f"Processed rows: {total_rows}")

# --------------------------------------------------
# Finished
# --------------------------------------------------

print("\nCleaning completed successfully!")
print("Total rows processed:", total_rows)
print("Cleaned file:", output_file)
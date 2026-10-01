# Airline Delay Root Cause Analysis ✈️

## Project Overview

This project analyzes airline flight delays using Python, SQL, and Power BI.

The goal is to identify patterns in flight delays, compare airline and airport performance, analyze delay causes, and identify important operational factors contributing to delays.

## Tools Used

- Python
- Pandas
- MySQL
- Power BI
- Git & GitHub

## Dataset

The project uses the 2015 US Flight Delays dataset containing approximately 5.8 million flight records.

The raw flight dataset is not included in this repository because of its large size.

## Business Questions

### Overall Performance
1. How many flights were operated?
2. What percentage were delayed?
3. How many were cancelled?
4. How many were diverted?

### Airline Analysis
5. Which airlines operate the most flights?
6. Which airlines have the highest delay rate?
7. Which airlines have the highest average delay?
8. Which airlines have the highest cancellation rate?

### Airport Analysis
9. Which origin airports have the highest delay rate?
10. Which destination airports have the highest delay rate?
11. Which airports handle the most flights?

### Time Analysis
12. Which months have the most delays?
13. Which days of the week have the most delays?
14. Which departure hours have the most delays?

### Root Cause Analysis
15. What are the major causes of delays?
16. Which airlines are most affected by weather delays?
17. Which airlines are most affected by late aircraft delays?
18. Which airports have the highest weather/system-related delays?

### Business Conclusions
19. Which airline has the worst overall delay performance?
20. What are the biggest operational factors contributing to delays?

## Key Findings

- Total flights analyzed: 5,819,079
- Delayed flights: 2,086,896
- Overall delay rate: 35.86%
- Cancelled flights: 89,884
- Diverted flights: 15,187

### Airline Findings

- Southwest Airlines operated the highest number of flights.
- Spirit Airlines had the highest delay rate at 48.46%.
- Frontier Airlines had the highest average arrival delay among delayed flights.
- American Eagle had the highest cancellation rate.

### Airport Findings

- ATL handled the highest combined number of origin and destination flights.
- DLH had the highest origin delay rate among airports with at least 1,000 origin flights.
- BQN had the highest destination delay rate among airports with at least 1,000 destination flights.

### Delay Causes

The largest contributors to total delay minutes were:

1. Late aircraft delays
2. Airline-related delays
3. Air system delays
4. Weather delays
5. Security delays

## Dashboard

The Power BI dashboard contains:

- Executive overview
- Airline performance
- Airport performance
- Monthly and daily delay trends
- Departure-hour analysis
- Delay cause analysis
- Airline cause analysis
- Airport cause analysis
import duckdb
import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd
import numpy as np

# read credentials from .env file which is var=value format
with open('./.env') as f:
    credentials = dict(x.rstrip().split('=', 1) for x in f)


conn = mysql.connect(host=credentials['DB_HOST'], database=credentials['DB_NAME'], user=credentials['DB_USER'], password=credentials['DB_PASS'])
cur = conn.cursor()

# get location data
try:
    query = f'SELECT * from crime_hazards_cost_of_living_combined'
    cur.execute(query)
    data = cur.fetchall()
    column_names = [i[0] for i in cur.description]
    locationData = pd.DataFrame(data, columns=column_names)

except mysql.Error as error:
    print('Error querying table: {}'.format(error))

# get jobzone and interest data
try:
    query = f'SELECT * from jobZonesInterestsSalariesByState'
    cur.execute(query)
    data = cur.fetchall()
    column_names = [i[0] for i in cur.description]
    jobZoneInterestData = pd.DataFrame(data, columns=column_names)

except mysql.Error as error:
    print('Error querying table: {}'.format(error))

# get jobDescriptions data
try:
    query = f'SELECT * from jobDescriptions'
    cur.execute(query)
    data = cur.fetchall()
    column_names = [i[0] for i in cur.description]
    jobDescriptionsData = pd.DataFrame(data, columns=column_names)

except mysql.Error as error:
    print('Error querying table: {}'.format(error))

# get nri_counties data
try:
    query = f'SELECT * from nri_counties'
    cur.execute(query)
    data = cur.fetchall()
    column_names = [i[0] for i in cur.description]
    nriCountiesData = pd.DataFrame(data, columns=column_names)

except mysql.Error as error:
    print('Error querying table: {}'.format(error))

# get zipcode_city_county_crosswalk data
try:
    query = f'SELECT * from zipcode_city_county_crosswalk'
    cur.execute(query)
    data = cur.fetchall()
    column_names = [i[0] for i in cur.description]
    zipCityCountyXwalkData = pd.DataFrame(data, columns=column_names)

except mysql.Error as error:
    print('Error querying table: {}'.format(error))

# close connection
cur.close()
conn.close()

# Write the DataFrames to Parquet files
locationData.to_parquet('./parquet/locationData.parquet')
jobZoneInterestData.to_parquet('./parquet/jobZoneInterestData.parquet')
jobDescriptionsData.to_parquet('./parquet/jobDescriptionsData.parquet')
nriCountiesData.to_parquet('./parquet/nriCountiesData.parquet')
zipCityCountyXwalkData.to_parquet('./parquet/zipCityCountyXwalkData.parquet')

# Connect to DuckDB
con = duckdb.connect('job_game_data.duckdb')

# drop tables if they exist
con.execute("DROP TABLE IF EXISTS crime_hazards_cost_of_living_combined")
con.execute("DROP TABLE IF EXISTS jobZonesInterestsSalariesByState")
con.execute("DROP TABLE IF EXISTS jobDescriptions")
con.execute("DROP TABLE IF EXISTS nri_counties")
con.execute("DROP TABLE IF EXISTS zipcode_city_county_crosswalk")

# Create DuckDB tables from the Parquet files
con.execute("CREATE TABLE crime_hazards_cost_of_living_combined AS SELECT * FROM parquet_scan('./parquet/locationData.parquet')")
con.execute("CREATE TABLE jobZonesInterestsSalariesByState AS SELECT * FROM parquet_scan('./parquet/jobZoneInterestData.parquet')")
con.execute("CREATE TABLE jobDescriptions AS SELECT * FROM parquet_scan('./parquet/jobDescriptionsData.parquet')")
con.execute("CREATE TABLE nri_counties AS SELECT * FROM parquet_scan('./parquet/nriCountiesData.parquet')")
con.execute("CREATE TABLE zipcode_city_county_crosswalk AS SELECT * FROM parquet_scan('./parquet/zipCityCountyXwalkData.parquet')")

# Close the connection to write changes to disk
con.close()

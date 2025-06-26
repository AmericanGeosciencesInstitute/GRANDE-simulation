# run as python3 jobgame_app.py

from flask import Flask, render_template, request, redirect, url_for, g, session, jsonify
import duckdb
import pandas as pd
import numpy as np
import uuid
import random
import mysql.connector as mysql
from mysql.connector import Error
import json

app = Flask(__name__)
app.secret_key = 'your secret key' 
DATABASE = 'job_game_data.duckdb'

# get the hazardZone descriptions
with open('./static/json/hazardZoneText.json') as f:
    hazardZoneTextJson = json.load(f)

# get the hazardZone colors and titles
with open('./static/json/hazardZoneColors.json') as f:
    hazardZoneColorsJson = json.load(f)
    hazard_zone_color_lookup = {item['code']: item['color'] for item in hazardZoneColorsJson['hazardZoneColors']}
    hazard_zone_title_lookup = {item['code']: item['title'] for item in hazardZoneColorsJson['hazardZoneColors']}

# Initialize cache as an empty dictionary
cache = {}

def empty_cache():
    cache.clear()
    session.clear()

    ## DEBUG
    print("---->>>> EMPTY CACHE: ", cache) # make sure cache is empty...

def round_and_fix(value, decimals=1):
    rounded_value = np.round(float(value), decimals)
    if rounded_value == 0.0:  # This condition catches both 0.0 and -0.0
        return 0.0
    return rounded_value

def get_db():
    if 'db' not in g:
        g.db = duckdb.connect(DATABASE, read_only=True)
    return g.db

def get_location_data(divisions, regions, westcentral):
    #Get locations for jobs (# jobs - location params)
    # 1 - locZone1: Crime rate= HIGH (4); Hazard risk= RELATIVELY HIGH to VERY HIGH (4 or 5)
    # 1 - locZone2: Crime rate= HIGH (4); Hazard risk= VERY LOW (1)
    # 1 - locZone3: Crime rate= LOW (1); Hazard risk= RELATIVELY MODERATE (3)
    # 1 - locZone4: Crime rate= LOW (1); Hazard risk= RELATIVELY HIGH to VERY HIGH (4 or 5)
    # 3 - locZone5: Crime rate= LOW to MEDIUM (1 or 2); Hazard risk= RELATIVELY MODERATE to VERY HIGH (3 to 5)
    # 3 - locZone6: Crime rate= LOW to MEDIUM (1 or 2); Hazard risk= VERY LOW to RELATIVELY MODERATE (1 to 3)
    # 3 - locZone7: Crime rate= MEDIUM to HIGH (2 to 4); Hazard risk= RELATIVELY MODERATE to VERY HIGH (3 to 5)
    # 3 - locZone8: Crime rate= MEDIUM to HIGH (2 to 4); Hazard risk= VERY LOW to RELATIVELY MODERATE (1 to 3)

    # get west central divisions for zone4 - we only use this because the west region has no data for locZone4.
    # also the west central divisions are adjacent to the west region
    westcentralZone4 = westcentral[(westcentral['crime_rank_total_offenses'] == 1) & (westcentral['haz_overall_risk_rating_rank'] >= 4)]

    # get all rows in divisions by zone
    divZone1 = divisions[(divisions['crime_rank_total_offenses'] == 4) & (divisions['haz_overall_risk_rating_rank'] >= 4)]
    divZone2 = divisions[(divisions['crime_rank_total_offenses'] == 4) & (divisions['haz_overall_risk_rating_rank'] == 1)]
    divZone3 = divisions[(divisions['crime_rank_total_offenses'] == 1) & (divisions['haz_overall_risk_rating_rank'] == 3)]
    divZone4 = divisions[(divisions['crime_rank_total_offenses'] == 1) & (divisions['haz_overall_risk_rating_rank'] >= 4)]
    divZone5 = divisions[(divisions['crime_rank_total_offenses'] <= 2) & (divisions['haz_overall_risk_rating_rank'] >= 3)]
    divZone6 = divisions[(divisions['crime_rank_total_offenses'] <= 2) & (divisions['haz_overall_risk_rating_rank'] <= 3)]
    divZone7 = divisions[(divisions['crime_rank_total_offenses'].between(2, 4)) & (divisions['haz_overall_risk_rating_rank'] >= 3)]
    divZone8 = divisions[(divisions['crime_rank_total_offenses'].between(2, 4)) & (divisions['haz_overall_risk_rating_rank'] <= 3)]

    # get all rows in regions by zone
    regZone1 = regions[(regions['crime_rank_total_offenses'] == 4) & (regions['haz_overall_risk_rating_rank'] >= 4)]
    regZone2 = regions[(regions['crime_rank_total_offenses'] == 4) & (regions['haz_overall_risk_rating_rank'] == 1)]
    regZone3 = regions[(regions['crime_rank_total_offenses'] == 1) & (regions['haz_overall_risk_rating_rank'] == 3)]
    regZone4 = regions[(regions['crime_rank_total_offenses'] == 1) & (regions['haz_overall_risk_rating_rank'] >= 4)]
    regZone5 = regions[(regions['crime_rank_total_offenses'] <= 2) & (regions['haz_overall_risk_rating_rank'] >= 3)]
    regZone6 = regions[(regions['crime_rank_total_offenses'] <= 2) & (regions['haz_overall_risk_rating_rank'] <= 3)]
    regZone7 = regions[(regions['crime_rank_total_offenses'].between(2, 4)) & (regions['haz_overall_risk_rating_rank'] >= 3)]
    regZone8 = regions[(regions['crime_rank_total_offenses'].between(2, 4)) & (regions['haz_overall_risk_rating_rank'] <= 3)]

    # construct location zones
    locZone1 = divZone1 if len(divZone1) > 0 else regZone1
    locZone2 = divZone2 if len(divZone2) > 0 else regZone2
    locZone3 = divZone3 if len(divZone3) > 0 else regZone3
    locZone4 = divZone4 if len(divZone4) > 0 else regZone4 if len(regZone4) > 0 else westcentralZone4
    locZone5 = divZone5 if len(divZone5) > 0 else regZone5
    locZone6 = divZone6 if len(divZone6) > 0 else regZone6
    locZone7 = divZone7 if len(divZone7) > 0 else regZone7
    locZone8 = divZone8 if len(divZone8) > 0 else regZone8

    location1 = locZone1.sample(1)
    location2 = locZone2.sample(1)
    location3 = locZone3.sample(1)
    location4 = locZone4.sample(1)
    location5 = locZone5.sample(3)
    location6 = locZone6.sample(3)
    location7 = locZone7.sample(3)
    location8 = locZone8.sample(3)

    location1[["ch_zone", "sal_to_col"]] = [1, 2]
    location2[["ch_zone", "sal_to_col"]] = [2, 1]
    location3[["ch_zone", "sal_to_col"]] = [3, 3]
    location4[["ch_zone", "sal_to_col"]] = [4, 3]
    location5["ch_zone"] = 5
    location6["ch_zone"] = 6
    location7["ch_zone"] = 7
    location8["ch_zone"] = 8

    location5['sal_to_col'] = range(1, len(location5) + 1)
    location6['sal_to_col'] = range(1, len(location6) + 1)
    location7['sal_to_col'] = range(1, len(location7) + 1)
    location8['sal_to_col'] = range(1, len(location8) + 1)

    # combine locations
    locations = pd.concat([location1, location2, location3, location4, location5, location6, location7, location8])
    locations.rename(columns={'id': 'location_id'}, inplace=True)
    locations.reset_index(drop=True, inplace=True)

    # Create a new column 'job_posting_id' with default value as empty string
    locations['job_posting_id'] = ''

    # create job posting ids - combo of 2 numbers, job id, and 1 number
    for index, row in locations.iterrows():
        jobId = str(index + 1)
        jobIdPrefix = str(random.randint(0, 10))
        jobIdSuffix = str(random.randint(0, 9))

        if len(jobId) == 1:
            jobId = '0' + jobId
        if len(jobIdPrefix) == 1:
            jobIdPrefix = '0' + jobIdPrefix

        locations.at[index, 'job_posting_id'] = str(jobIdPrefix) + str(jobId) + str(jobIdSuffix)
    
    locations['job_id'] = locations.index + 1
    states = locations['state_abbreviation'].unique()

    return locations, states

def get_locations_and_states(db, divisions, regions):
    divConditions = ' OR '.join(f"division='{div}'" for div in divisions)
    divQuery = f'SELECT * FROM crime_hazards_cost_of_living_combined WHERE {divConditions}'
    divisionData = db.execute(divQuery).fetchdf()

    regConditions = ' OR '.join(f"region='{reg}'" for reg in regions)
    regQuery = f'SELECT * FROM crime_hazards_cost_of_living_combined WHERE {regConditions}'
    regionData = db.execute(regQuery).fetchdf()

    # we do this because the west region has no data for zone4. 
    wcConditions = f"division='westnorthcentral' OR division = 'westsouthcentral'"
    westcentralQuery = f'SELECT * FROM crime_hazards_cost_of_living_combined WHERE {wcConditions}'
    westcentralData = db.execute(westcentralQuery).fetchdf()

    locations, states = get_location_data(divisionData, regionData, westcentralData)
    return locations, states

def get_job_data_with_descriptions(db, jobZone, states, degreeField):
    if degreeField == 'na':
        DegreeFieldConditions =  f"degree_field_short='generic'"
    else:
        DegreeFieldConditions =  f"degree_field_short='{degreeField}' OR degree_field_short='generic'"
    
    JobZoneConditions = f"job_zone={jobZone}"
    LocationConditions = ' OR '.join(f"state_abbreviation='{loc}'" for loc in states)
    
    jobConditions = '(' + JobZoneConditions + ') AND (' + LocationConditions + ') AND (' + DegreeFieldConditions + ')'
    jobSelect = f'SELECT jobZonesInterestsSalariesByState.*, jobDescriptions.id as job_description_id, jobDescriptions.degree_field_short, jobDescriptions.organization_name, jobDescriptions.job_title, jobDescriptions.job_description'
    jobQuery = f'{jobSelect} FROM jobZonesInterestsSalariesByState INNER JOIN jobDescriptions ON jobZonesInterestsSalariesByState.occ_code = jobDescriptions.occ_code WHERE {jobConditions}'
    jobData = db.execute(jobQuery).fetchdf()

    return jobData

def get_jobs_in_locations(jobData, locations):
    jobs = pd.DataFrame(columns=['job_id', 'state','occ_code','salary','job_description_id', 'degree_field_short', 'job_title', 'organization_name', 'job_description'])

    for index, row in locations.iterrows():
        jobId = row['job_id']
        state = row['state_abbreviation']
        col_min_salary = row['col_min_salary']
        sal_to_col = row['sal_to_col']

        if sal_to_col == 1:
            salary_min = 1
            salary_max = 1.2
        elif sal_to_col == 2:
            salary_min = 1.21
            salary_max = 1.5
        elif sal_to_col == 3:       
            salary_min = 1.51
            salary_max = 2


        salary = round(col_min_salary * np.random.uniform(salary_min, salary_max)/ 100) * 100

        potentialJobs = jobData[(jobData['degree_field_short'] != 'generic') & (jobData['state_abbreviation'] == state) & (salary >= jobData['a_pct10']*.9) & (salary <= jobData['a_pct90'] * 1.1)]
        potentialJobs1 = jobData[(jobData['state_abbreviation'] == state) & (salary >= jobData['a_pct10']*.9) & (salary <= jobData['a_pct90'] * 1.1)] # get all jobs that match salary cap

        potentialJobs2 = jobData[(jobData['state_abbreviation'] == state)] # get this b/c the salary cap sometimes returns no results

        if len(potentialJobs) > 0:
            job = potentialJobs.sample(1)
        else:
            if len(potentialJobs1) > 0:
                job = potentialJobs1.sample(1)
            else:
                job = potentialJobs2.sample(1)

        occ_code = job['occ_code'].values[0]
        jobDescriptionId = job['job_description_id'].values[0]
        degreeField = job['degree_field_short'].values[0]
        jobTitle = job['job_title'].values[0]
        jobDescription = job['job_description'].values[0]
        jobOrganization = job['organization_name'].values[0]

        # changed due to multiple comments about salaries being too low for high paying jobs 8/1/2024
        # readjust high salary jobs that exceed bls data to be more reasonable
        if sal_to_col == 3 and job['a_pct90'].values[0] == 239200:
            salary = round(col_min_salary * np.random.uniform(salary_min, 5)/ 100) * 100

        dfAdds = pd.DataFrame([[jobId, state, occ_code, salary, jobDescriptionId, degreeField, jobTitle, jobOrganization, jobDescription]], columns=['job_id','state','occ_code','salary','job_description_id', 'degree_field_short', 'job_title', 'organization_name', 'job_description'])
        jobs = pd.concat([jobs, dfAdds], ignore_index=True)    

    return jobs

def get_job_search_results(jobsWithDescriptions, locations):
    allData = pd.merge(jobsWithDescriptions, locations, on='job_id')
    finalData = allData[['job_id', 'job_posting_id', 'ch_zone', 'job_description_id', 'location_id', 'city_name', 'state_abbreviation', 'state_county_fips',
        'occ_code', 'degree_field_short', 'salary', 'job_title', 'organization_name', 'job_description',
        'col_total_monthly_cost','col_housing', 'col_food', 'col_transportation', 'col_healthcare', 'col_other_necessities', 'col_taxes', 
        'crime_rate_total_offenses', 'crime_rank_total_offenses', 'crime_rank_personal', 'crime_rank_property', 'crime_rank_society',
        'haz_overall_risk_rating_rank', 'haz_avalanche_risk_rating_rank', 'haz_coastal_flood_risk_rating_rank', 'haz_cold_wave_risk_rating_rank',
        'haz_drought_risk_rating_rank', 'haz_earthquake_risk_rating_rank', 'haz_hail_risk_rating_rank', 'haz_heat_wave_risk_rating_rank',
        'haz_hurricane_risk_rating_rank', 'haz_icestorm_risk_rating_rank', 'haz_landslide_risk_rating_rank', 'haz_lightning_risk_rating_rank',
        'haz_river_flood_risk_rating_rank', 'haz_strong_wind_risk_rating_rank', 'haz_tornado_risk_rating_rank', 'haz_tsunami_risk_rating_rank',
        'haz_volcano_risk_rating_rank', 'haz_wildfire_risk_rating_rank', 'haz_winter_weather_risk_rating_rank','col_min_salary', 'sal_to_col'
    ]].copy()

    # add in haz calcs for 6 hazards ; we keep the highest value for all sub hazards in the category
    # category = hazards from NRI
    # earthquake = earthquake
    # fire = wildfire
    # slide = avalanche, landslide
    # flood = coastal_flood, river_flood, tsunami
    # severe weather = cold_wave, drought, hail, heat_wave, hurricane, ice_storm, lightning, strong_wind, tornado, winter_weather
    # volcano = volcano

    finalData['haz_earthquake'] = finalData['haz_earthquake_risk_rating_rank']
    finalData['haz_fire'] = finalData['haz_wildfire_risk_rating_rank']
    finalData['haz_slide'] = finalData[['haz_avalanche_risk_rating_rank', 'haz_landslide_risk_rating_rank']].max(axis=1)
    finalData['haz_flood'] = finalData[['haz_coastal_flood_risk_rating_rank', 'haz_river_flood_risk_rating_rank', 'haz_tsunami_risk_rating_rank']].max(axis=1)
    finalData['haz_severe_weather'] = finalData[['haz_cold_wave_risk_rating_rank', 'haz_drought_risk_rating_rank', 'haz_hail_risk_rating_rank', 'haz_heat_wave_risk_rating_rank', 'haz_hurricane_risk_rating_rank', 'haz_icestorm_risk_rating_rank', 'haz_lightning_risk_rating_rank', 'haz_strong_wind_risk_rating_rank', 'haz_tornado_risk_rating_rank', 'haz_winter_weather_risk_rating_rank']].max(axis=1)
    finalData['haz_volcano'] = finalData['haz_volcano_risk_rating_rank']

    # convert numbers to colors
    finalData['crime_icon'] = finalData['crime_rank_total_offenses'].apply(lambda x: 'icon-red' if x >= 3 else 'icon-yellow' if x == 2 else 'icon-blue')
    finalData['haz_earthquake_icon'] = finalData['haz_earthquake'].apply(lambda x: 'icon-red' if x >= 4 else 'icon-yellow' if x == 3 else 'icon-blue' if x in [2, 1] else 'icon-none')
    finalData['haz_fire_icon'] = finalData['haz_fire'].apply(lambda x: 'icon-red' if x >= 4 else 'icon-yellow' if x == 3 else 'icon-blue' if x in [2, 1] else 'icon-none')
    finalData['haz_slide_icon'] = finalData['haz_slide'].apply(lambda x: 'icon-red' if x >= 4 else 'icon-yellow' if x == 3 else 'icon-blue' if x in [2, 1] else 'icon-none')
    finalData['haz_flood_icon'] = finalData['haz_flood'].apply(lambda x: 'icon-red' if x >= 4 else 'icon-yellow' if x == 3 else 'icon-blue' if x in [2, 1] else 'icon-none')
    finalData['haz_severe_weather_icon'] = finalData['haz_severe_weather'].apply(lambda x: 'icon-red' if x >= 4 else 'icon-yellow' if x == 3 else 'icon-blue' if x in [2, 1] else 'icon-none')
    finalData['haz_volcano_icon'] = finalData['haz_volcano'].apply(lambda x: 'icon-red' if x >= 4 else 'icon-yellow' if x == 3 else 'icon-blue' if x in [2, 1] else 'icon-none')

    finalData['col_annual_total'] = finalData['col_total_monthly_cost'] * 12
    finalData['col_annual_housing'] = finalData['col_housing'] * 12
    finalData['col_annual_food'] = finalData['col_food'] * 12
    finalData['col_annual_transportation'] = finalData['col_transportation'] * 12
    finalData['col_annual_healthcare'] = finalData['col_healthcare'] * 12
    finalData['col_annual_other_necessities'] = finalData['col_other_necessities'] * 12
    finalData['col_annual_taxes'] = finalData['col_taxes'] * 12
    finalData['annual_disposable_income'] = finalData['salary'] - finalData['col_annual_total']

    # drop monthly col columns
    finalData.drop(columns=['col_min_salary','col_total_monthly_cost','col_housing', 'col_food', 'col_transportation', 'col_healthcare', 'col_other_necessities', 'col_taxes', 'haz_overall_risk_rating_rank', 'haz_avalanche_risk_rating_rank', 'haz_coastal_flood_risk_rating_rank', 'haz_cold_wave_risk_rating_rank', 'haz_drought_risk_rating_rank', 'haz_earthquake_risk_rating_rank', 'haz_hail_risk_rating_rank', 'haz_heat_wave_risk_rating_rank', 'haz_hurricane_risk_rating_rank', 'haz_icestorm_risk_rating_rank', 'haz_landslide_risk_rating_rank', 'haz_lightning_risk_rating_rank', 'haz_river_flood_risk_rating_rank', 'haz_strong_wind_risk_rating_rank', 'haz_tornado_risk_rating_rank', 'haz_tsunami_risk_rating_rank', 'haz_volcano_risk_rating_rank', 'haz_wildfire_risk_rating_rank', 'haz_winter_weather_risk_rating_rank',], inplace=True)

    return finalData

def get_current_location_hazard_risk(db, stcofips):
    curlocConditions = f"state_county_fips='{stcofips}'"
    curlocQuery = f"""SELECT state_county_fips, county_name, state_abbreviation, haz_overall_risk_rating_rank, haz_avalanche_risk_rating_rank, haz_coastal_flood_risk_rating_rank,
    haz_cold_wave_risk_rating_rank, haz_drought_risk_rating_rank, haz_earthquake_risk_rating_rank, haz_hail_risk_rating_rank,
    haz_heat_wave_risk_rating_rank, haz_hurricane_risk_rating_rank, haz_icestorm_risk_rating_rank, haz_landslide_risk_rating_rank,
    haz_lightning_risk_rating_rank, haz_river_flood_risk_rating_rank, haz_strong_wind_risk_rating_rank, haz_tornado_risk_rating_rank,
    haz_tsunami_risk_rating_rank, haz_volcano_risk_rating_rank, haz_wildfire_risk_rating_rank, haz_winter_weather_risk_rating_rank
    FROM crime_hazards_cost_of_living_combined WHERE {curlocConditions}"""
        
    curlocData = db.execute(curlocQuery).fetchdf()

    # drop duplicates
    curlocData.drop_duplicates(inplace=True)

    # if curlocData is empty, query the nri data
    if len(curlocData) == 0:
        curlocConditions = f"stcofips='{stcofips}'"
        curlocQuery = f"""SELECT stcofips, county, stateabbrv, risk_ratng, avln_riskr, cfld_riskr, cwav_riskr, drgt_riskr, erqk_riskr, hail_riskr, hwav_riskr, hrcn_riskr, istm_riskr, lnds_riskr, ltng_riskr, rfld_riskr, swnd_riskr, trnd_riskr, tsun_riskr, vlcn_riskr, wfir_riskr, wntw_riskr FROM nri_counties WHERE {curlocConditions}"""

        curlocData = db.execute(curlocQuery).fetchdf()

        # drop duplicates
        curlocData.drop_duplicates(inplace=True)

        # calculate ranks
        rankratingDict = {"Very Low": 1, "Relatively Low": 2, "Relatively Moderate": 3, "Relatively High": 4, "Very High": 5, "No Rating": 0, "Insufficient Data": 0, "Not Applicable": 0}

        colNameXmap = {
            "risk_ratng": "haz_overall_risk_rating_rank",
            "avln_riskr": "haz_avalanche_risk_rating_rank",
            "cfld_riskr": "haz_coastal_flood_risk_rating_rank",
            "cwav_riskr": "haz_cold_wave_risk_rating_rank",
            "drgt_riskr": "haz_drought_risk_rating_rank",
            "erqk_riskr": "haz_earthquake_risk_rating_rank",
            "hail_riskr": "haz_hail_risk_rating_rank",
            "hwav_riskr": "haz_heat_wave_risk_rating_rank",
            "hrcn_riskr": "haz_hurricane_risk_rating_rank",
            "istm_riskr": "haz_icestorm_risk_rating_rank",
            "lnds_riskr": "haz_landslide_risk_rating_rank",
            "ltng_riskr": "haz_lightning_risk_rating_rank",
            "rfld_riskr": "haz_river_flood_risk_rating_rank",
            "swnd_riskr": "haz_strong_wind_risk_rating_rank",
            "trnd_riskr": "haz_tornado_risk_rating_rank",
            "tsun_riskr": "haz_tsunami_risk_rating_rank",
            "vlcn_riskr": "haz_volcano_risk_rating_rank",
            "wfir_riskr": "haz_wildfire_risk_rating_rank",
            "wntw_riskr": "haz_winter_weather_risk_rating_rank"
            }

        for key in colNameXmap:
            if key in curlocData.columns:
                curlocData[colNameXmap[key]] = curlocData[key].map(rankratingDict).astype(int)
                curlocData.drop(columns=[key], inplace=True)
                curlocData.rename(columns={key: colNameXmap[key]}, inplace=True)
        
        # rename stcofips, county, stateabbrv to state_county_fips, county_name, state_abbreviation
        curlocData.rename(columns={'stcofips': 'state_county_fips', 'county': 'county_name', 'stateabbrv': 'state_abbreviation'}, inplace=True)
        
        # replace NaN with 0
        curlocData.fillna(0, inplace=True)

    # add in haz calcs for 6 hazards ; we keep the highest value for all sub hazards in the category
    # category = hazards from NRI
    # earthquake = earthquake
    # fire = wildfire
    # slide = avalanche, landslide
    # flood = coastal_flood, river_flood, tsunami
    # severe weather = cold_wave, drought, hail, heat_wave, hurricane, ice_storm, lightning, strong_wind, tornado, winter_weather
    # volcano = volcano

    curlocData['haz_earthquake'] = curlocData['haz_earthquake_risk_rating_rank']
    curlocData['haz_fire'] = curlocData['haz_wildfire_risk_rating_rank']
    curlocData['haz_slide'] = curlocData[['haz_avalanche_risk_rating_rank', 'haz_landslide_risk_rating_rank']].max(axis=1)
    curlocData['haz_flood'] = curlocData[['haz_coastal_flood_risk_rating_rank', 'haz_river_flood_risk_rating_rank', 'haz_tsunami_risk_rating_rank']].max(axis=1)
    curlocData['haz_severe_weather'] = curlocData[['haz_cold_wave_risk_rating_rank', 'haz_drought_risk_rating_rank', 'haz_hail_risk_rating_rank', 'haz_heat_wave_risk_rating_rank', 'haz_hurricane_risk_rating_rank', 'haz_icestorm_risk_rating_rank', 'haz_lightning_risk_rating_rank', 'haz_strong_wind_risk_rating_rank', 'haz_tornado_risk_rating_rank', 'haz_winter_weather_risk_rating_rank']].max(axis=1)
    curlocData['haz_volcano'] = curlocData['haz_volcano_risk_rating_rank']

    # convert numbers to colors
    curlocData['haz_earthquake_icon'] = curlocData['haz_earthquake'].apply(lambda x: 'icon-red' if x >= 4 else 'icon-yellow' if x == 3 else 'icon-blue' if x in [2, 1] else 'icon-none')
    curlocData['haz_fire_icon'] = curlocData['haz_fire'].apply(lambda x: 'icon-red' if x >= 4 else 'icon-yellow' if x == 3 else 'icon-blue' if x in [2, 1] else 'icon-none')
    curlocData['haz_slide_icon'] = curlocData['haz_slide'].apply(lambda x: 'icon-red' if x >= 4 else 'icon-yellow' if x == 3 else 'icon-blue' if x in [2, 1] else 'icon-none')
    curlocData['haz_flood_icon'] = curlocData['haz_flood'].apply(lambda x: 'icon-red' if x >= 4 else 'icon-yellow' if x == 3 else 'icon-blue' if x in [2, 1] else 'icon-none')
    curlocData['haz_severe_weather_icon'] = curlocData['haz_severe_weather'].apply(lambda x: 'icon-red' if x >= 4 else 'icon-yellow' if x == 3 else 'icon-blue' if x in [2, 1] else 'icon-none')
    curlocData['haz_volcano_icon'] = curlocData['haz_volcano'].apply(lambda x: 'icon-red' if x >= 4 else 'icon-yellow' if x == 3 else 'icon-blue' if x in [2, 1] else 'icon-none')

    curlocHazardData = curlocData[['state_county_fips', 'haz_earthquake', 'haz_fire', 'haz_slide', 'haz_flood', 'haz_severe_weather', 'haz_volcano',
        'haz_earthquake_icon', 'haz_fire_icon', 'haz_slide_icon', 'haz_flood_icon', 'haz_severe_weather_icon', 'haz_volcano_icon']].copy()

    return curlocHazardData

def generate_job_list(jobListId):
    jobListId = jobListId
    degreeField = cache[session['token']]['degreeField']
    jobZone = cache[session['token']]['jobZone']
    divisions = cache[session['token']]['divisions']
    regions = cache[session['token']]['regions']

    # Get the database connection
    db = get_db()

    #STEP 1 - get locations from crime_hazards_cost_of_living_combined table
    locations, states = get_locations_and_states(db, divisions, regions)

    # #STEP 2 - get jobs
    jobData = get_job_data_with_descriptions(db, jobZone, states, degreeField)
    jobsInLocations = get_jobs_in_locations(jobData, locations)

    #STEP 3 - merge data and compute final costs
    jobSearchResults = get_job_search_results(jobsInLocations, locations)

    ## DEBUG
    for index,row in jobSearchResults.iterrows():
        print(row['job_id'], row['degree_field_short'], row['occ_code'], row['job_title'])

    # initialize job data
    if 'jobdata' not in cache[session['token']]:
        cache[session['token']]['jobdata'] = {}
    
    # initialize this set of jobs, ids, pairs and choices
    cache[session['token']]['jobdata'][jobListId] = {'joblist': [],'shuffled_job_ids': [], 'job_pairs': {}, 'choices': {}}

    # add job data
    for index, row in jobSearchResults.iterrows():
        cache[session['token']]['jobdata'][jobListId]['joblist'].append(row.to_dict())

    # Shuffle job IDs and store them in the cache
    jobIds = np.random.permutation(jobSearchResults['job_id'].tolist())
    cache[session['token']]['jobdata'][jobListId]['shuffled_job_ids'] = jobIds.tolist()

    return cache[session['token']]['jobdata'][jobListId]['joblist']

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/', methods=['GET', 'POST'])
def startgame():
    if request.path == '/' and request.method == 'GET':
        if cache:
            cache.clear()
            session.clear()

        session['token'] = uuid.uuid4().hex
        cache[session['token']] = {}

        ## DEBUG
        print(cache) # make sure cache is empty...

    if request.method == 'POST':
        cache[session['token']]['age'] = request.form.get('age')
        
        ##DEBUG 
        print("-- AGE: ", cache[session['token']]['age'])

        return redirect(url_for('filters1'))
    return render_template('index.html')

@app.route('/filters1', methods=['GET', 'POST'])
def filters1():
    if request.method == 'POST':
        cache[session['token']]['jobZone'] = request.form.get('jobZone')
        cache[session['token']]['degreeField'] = request.form.get('degreeField')

        ##DEBUG
        print("-- JOBZONE: ", cache[session['token']]['jobZone'])
        print("-- DEGREEFIELD: ", cache[session['token']]['degreeField'])

        return redirect(url_for('filters3'))
    return render_template('filters1.html')

@app.route('/filters3', methods=['GET', 'POST'])
def filters3():
    if request.method == 'POST':
        cache[session['token']]['divisions'] = request.form.getlist('division')
        cache[session['token']]['regions'] = request.form.getlist('region')

        ##DEBUG
        print("-- DIVISIONS: ", cache[session['token']]['divisions'])
        print("-- REGIONS: ", cache[session['token']]['regions'])

        # get job list
        jobListId = 0
        generate_job_list(jobListId)
        return redirect(url_for('choice', roundNumber=0, pairNumber=0, jobListId=jobListId, jobOptions=8, numChoices=0))
    return render_template('filters3.html')
        
def get_job_pairs(roundNumber, token, jobListId):
    regen_flag = ''

    ## DEBUG
    print(">>===>> def GET_JOB_PAIRS: round [", roundNumber, "] jobListId [", jobListId, "]")

    if roundNumber == 0:
        job_ids = cache[session['token']]['jobdata'][jobListId]['shuffled_job_ids']
    else:
        job_ids = cache[session['token']]['jobdata'][jobListId]['choices'][roundNumber - 1]
        # remove 0s from the list
        job_ids = [x for x in job_ids if x != 0]
        # if the list has an odd number of items, add the first one to the end of the list
        if len(job_ids) % 2 != 0:
            job_ids.append(job_ids[0])

    # if job_ids is empty, generate new list of ids
    if len(job_ids) == 0 or job_ids[0] == -1:

        ## DEBUG
        print(">>===>> ---->> NO JOBS CHOSEN. GENERATING NEW LIST OF JOBS...")
        
        # generating new list of jobs
        jobListId = jobListId + 1
        regen_flag='newlist'
        generate_job_list(jobListId)
        job_ids = cache[session['token']]['jobdata'][jobListId]['shuffled_job_ids']
        # reset roundNumber to 0
        roundNumber = 0

    job_pairs = [job_ids[i:i+2] for i in range(0, len(job_ids), 2)]

    # add the job pairs to the cache for options
    if 'job_pairs' not in cache[session['token']]['jobdata'][jobListId]:
        cache[session['token']]['jobdata'][jobListId]['job_pairs'] = {}
    if roundNumber not in cache[session['token']]['jobdata'][jobListId]['job_pairs']:
        cache[session['token']]['jobdata'][jobListId]['job_pairs'][roundNumber] = job_pairs

    ## DEBUG
    print(">>===>> ---->> ROUND [", roundNumber , "] JOB LIST ID: [", jobListId, "] JOB PAIRS: ", job_pairs)

    return (job_pairs, regen_flag, jobListId)

def handle_choice(roundNumber, pairNumber, jobListId, jobOptions, numChoices):

    # set the values for the progress bar
    progress_values = {
            (1, 1): 30, (1, 2): 31, (1, 3): 32, (1, 4): 33, (1, 5): 34, (1, 6): 35, (1, 7): 36, (1, 8): 37,
            (2, 1): 38, (2, 2): 39, (2, 3): 40, (2, 4): 41,
            (3, 1): 42, (3, 2): 43,
            (4, 1): 44
        }

    # Get the job pairs for this round
    ## DEBUG
    print(">>===>> def HANDLE_CHOICE: round [", roundNumber, "] pair [", pairNumber, "] jobListId [", jobListId, "]", "  JOB OPTIONS: [", jobOptions, "]  NUM CHOICES: [", numChoices, "]")

    round_job_pairs, regen_flag, newJobListId = get_job_pairs(roundNumber, session['token'], jobListId)
   
    # if the jobListId has changed, reset the round and pair number
    if newJobListId != jobListId:
        jobListId = newJobListId
        roundNumber = 0
        pairNumber = 0
        jobOptions = 8
        numChoices = 0

    nextPairNumber = pairNumber
    nextRound = roundNumber

    # Record the selected job if this is a POST request
    if request.method == 'POST':
        selected_job = request.form.get('selected_job')
        if 'choices' not in cache[session['token']]['jobdata'][jobListId]:
            cache[session['token']]['jobdata'][jobListId]['choices'] = {}
        if roundNumber not in cache[session['token']]['jobdata'][jobListId]['choices']:
            cache[session['token']]['jobdata'][jobListId]['choices'][roundNumber] = []
        if selected_job:
            cache[session['token']]['jobdata'][jobListId]['choices'][roundNumber].append(int(selected_job))

        # Determine nextPairNumber and nextRound
        nextPairNumber = pairNumber + 1
        nextRound = roundNumber
        
        num_job_pairs = len(round_job_pairs)
       
        if nextRound in cache[session['token']]['jobdata'][jobListId]['choices']:
            numChoices = len(([x for x in cache[session['token']]['jobdata'][jobListId]['choices'][nextRound] if x != 0]))
            len_choices = len(cache[session['token']]['jobdata'][jobListId]['choices'][nextRound])
        else:
            numChoices = 0
            len_choices = 0

        jobOptions = (num_job_pairs - len_choices)
        
        if nextPairNumber >= len(round_job_pairs):
            nextPairNumber = 0
            nextRound = roundNumber + 1
            jobOptions = np.ceil(numChoices / 2)
            numChoices = 0

        # set the progress_value
        progress_value = progress_values.get((nextRound + 1, nextPairNumber + 1), 30)

        # Redirect to the next pair or round after recording the selected job
        ##DEBUG
        print(">>===>> ---->> HANDLE CHOICE - POST ---=== MOVING TO NEXT ROUND ===")
        print(">>===>> ---->> HANDLE CHOICE - POST --->> NEXT ROUND: ", nextRound, "  >> NEXT PAIR NUMBER: ", nextPairNumber, " CHOICES: ", cache[session['token']]['jobdata'][jobListId]['choices'], " JOB PAIRS LEFT: ", jobOptions, "  JOBS CHOSEN: ", numChoices)
              
        return redirect(url_for(f'choice', roundNumber=nextRound, pairNumber=nextPairNumber, jobListId=jobListId, jobOptions=jobOptions, numChoices=numChoices, progress_value=progress_value))
    
    if request.method == 'GET':

        # set the progress_value
        progress_value = progress_values.get((nextRound + 1, nextPairNumber + 1), 30)

        # Parse the job pairs into job1 and job2
        this_job1_id, this_job2_id = round_job_pairs[pairNumber]

        # Get the full list of jobs
        joblist = cache[session['token']]['jobdata'][jobListId]['joblist']
        dfJobs = pd.DataFrame(joblist)

        job1 = dfJobs.loc[dfJobs['job_id'] == this_job1_id].iloc[0]
        job2 = dfJobs.loc[dfJobs['job_id'] == this_job2_id].iloc[0]

        jobs = [job1, job2]
        
        if this_job1_id == this_job2_id:
            finaljob_id = this_job1_id
            cache[session['token']]['final_job'] = {}
            cache[session['token']]['final_job']['jobListId'] = jobListId
            cache[session['token']]['final_job']['job_id'] = finaljob_id

            # redirect to final choice
            return redirect(url_for('finalchoice', finaljobId=finaljob_id, jobListId=jobListId))

        else:
            jobs = [job1, job2]
          
            # Render the choice template with the appropriate data
            return render_template('choice.html', roundNumber=roundNumber, pairNumber=nextPairNumber, jobListId=jobListId, nextRound=nextRound, jobs=jobs, flag=regen_flag, jobOptions=jobOptions, numChoices=numChoices, progress_value=progress_value)

@app.route('/choice/<int:roundNumber>/<int:pairNumber>/<int:jobListId>/<int:jobOptions>/<int:numChoices>', methods=['GET', 'POST'])
def choice(roundNumber, pairNumber, jobListId, jobOptions, numChoices):
    return handle_choice(roundNumber, pairNumber, jobListId, jobOptions, numChoices)

@app.route('/finalchoice/<int:finaljobId>/<int:jobListId>', methods=['GET', 'POST'])
def finalchoice(finaljobId, jobListId):
    if request.method == 'POST':
        if 'jobreasons' not in cache[session['token']]:
            cache[session['token']]['jobreasons'] = {}

        cache[session['token']]['jobreasons']['jobtasks'] = request.form.get('jobtasks')
        cache[session['token']]['jobreasons']['location'] = request.form.get('location')
        cache[session['token']]['jobreasons']['income'] = request.form.get('income')
        cache[session['token']]['jobreasons']['crime'] = request.form.get('crime')
        cache[session['token']]['jobreasons']['hazard'] = request.form.get('hazard')
        cache[session['token']]['jobreasons']['climate'] = request.form.get('climate')
        cache[session['token']]['jobreasons']['resources'] = request.form.get('resources')
        cache[session['token']]['jobreasons']['social'] = request.form.get('social')
        cache[session['token']]['jobreasons']['other'] = request.form.get('other')

        ##DEBUG
        print("-- JOB REASONS: ", cache[session['token']]['jobreasons'])

        # go to next page
        return redirect(url_for('currentrisk'))
    
    # Get the job information
    joblist = cache[session['token']]['jobdata'][jobListId]['joblist']
    dfJobs = pd.DataFrame(joblist)
    finaljob = dfJobs.loc[dfJobs['job_id'] == int(finaljobId)].iloc[0]

    ## DEBUG
    print("ST CO FIPS:  ", finaljob['state_county_fips'])

    return render_template('finalchoice.html', job=finaljob, jobListId=jobListId)

@app.route('/currentrisk', methods=['GET', 'POST'])
def currentrisk():
    if request.method == 'POST':
        # get values
        cache[session['token']]['current_loc_stcofips'] = request.form.get('fipscode-input')

        if 'current_haz_risk' not in cache[session['token']]:
            cache[session['token']]['current_haz_concern'] = {}

        cache[session['token']]['current_haz_concern']['earthquake'] = request.form.get('earthquake')
        cache[session['token']]['current_haz_concern']['wildfire'] = request.form.get('wildfire')
        cache[session['token']]['current_haz_concern']['flood'] = request.form.get('flood')
        cache[session['token']]['current_haz_concern']['landslide'] = request.form.get('landslide')
        cache[session['token']]['current_haz_concern']['severe-weather'] = request.form.get('severe-weather')
        cache[session['token']]['current_haz_concern']['volcano'] = request.form.get('volcano')
        
        ##DEBUG
        print("-- CURRENT STCO FIPS: ", cache[session['token']]['current_loc_stcofips'])
        print("-- CURRENT HAZARD CONCERN: ", cache[session['token']]['current_haz_concern'])

        # get current location hazard risk
        db = get_db()
        curlocHazardData = get_current_location_hazard_risk(db, cache[session['token']]['current_loc_stcofips'])
        
        # store in cache
        # cache[session['token']]['current_location_haz_risk'] = {}
        cache[session['token']]['current_location_haz_risk'] =curlocHazardData.iloc[0].to_dict()

        ## DEBUG
        print("-- CURRENT LOCATION HAZ RISK: ",  cache[session['token']]['current_location_haz_risk'])

        # go to next page
        return redirect(url_for('currentrisk2'))

    return render_template('currentrisk.html')
    
@app.route('/currentrisk2', methods=['GET', 'POST'])
def currentrisk2():
    
    if request.method == 'POST':
        # get values
        if 'prevention_cost' not in cache[session['token']]:
            cache[session['token']]['prevention_cost'] = {}

        cache[session['token']]['prevention_cost']['earthquake'] = request.form.get('earthquake')
        cache[session['token']]['prevention_cost']['wildfire'] = request.form.get('wildfire')
        cache[session['token']]['prevention_cost']['flood'] = request.form.get('flood')
        cache[session['token']]['prevention_cost']['landslide'] = request.form.get('landslide')
        cache[session['token']]['prevention_cost']['severe-weather'] = request.form.get('severe-weather')
        cache[session['token']]['prevention_cost']['volcano'] = request.form.get('volcano')

        ##DEBUG
        print("-- PREVENTION COST: ", cache[session['token']]['prevention_cost'])

        # go to next page
        return redirect(url_for('currentrisk3'))
    
    return render_template('currentrisk2.html')

@app.route('/currentrisk3', methods=['GET', 'POST'])
def currentrisk3():
    
    if request.method == 'POST':
        # get values
        if 'impact_severity' not in cache[session['token']]:
            cache[session['token']]['impact_severity'] = {}

        cache[session['token']]['impact_severity']['earthquake'] = request.form.get('earthquake')
        cache[session['token']]['impact_severity']['wildfire'] = request.form.get('wildfire')
        cache[session['token']]['impact_severity']['flood'] = request.form.get('flood')
        cache[session['token']]['impact_severity']['landslide'] = request.form.get('landslide')
        cache[session['token']]['impact_severity']['severe-weather'] = request.form.get('severe-weather')
        cache[session['token']]['impact_severity']['volcano'] = request.form.get('volcano')

        ##DEBUG
        print("-- IMPACT SEVERITY: ", cache[session['token']]['impact_severity'])

        # go to next page
        return redirect(url_for('currentlocation'))
    
    return render_template('currentrisk3.html')

@app.route('/geolocator')
def geolocator():
    query = request.args.get('query', '').lower()
    results = []
    
    if query:
        sql_query = """
        SELECT county_name, state_abbreviation, city_name, zipcode, state_county_fips
        FROM zipcode_city_county_crosswalk 
        WHERE LOWER(county_name) LIKE ? 
        OR LOWER(state_abbreviation) LIKE ? 
        OR LOWER(city_name) LIKE ? 
        OR zipcode LIKE ?
        LIMIT 10
        """
        query_param = f"%{query}%"
        db = get_db()
        results = db.execute(sql_query, (query_param, query_param, query_param, query_param)).fetchall()

    return jsonify(results)

@app.route('/currentlocation', methods=['GET', 'POST'])
def currentlocation():
    
    if request.method == 'POST':
        # get values
        if 'current_loc_reasons' not in cache[session['token']]:
            cache[session['token']]['current_loc_reasons'] = {}

        cache[session['token']]['current_loc_reasons']['climate'] = request.form.get('climate')
        cache[session['token']]['current_loc_reasons']['resources'] = request.form.get('resources')
        cache[session['token']]['current_loc_reasons']['social'] = request.form.get('social')
        cache[session['token']]['current_loc_reasons']['income'] = request.form.get('income')
        cache[session['token']]['current_loc_reasons']['crime'] = request.form.get('crime')
        cache[session['token']]['current_loc_reasons']['hazard'] = request.form.get('hazard')
        cache[session['token']]['current_loc_reasons']['location'] = request.form.get('location')
        cache[session['token']]['current_loc_reasons']['other'] = request.form.get('other')

        ##DEBUG
        print("-- CURRENT LOCATION REASONS: ", cache[session['token']]['current_loc_reasons'])

        # go to next page
        return redirect(url_for('currentoccupation'))
    
    return render_template('currentlocation.html')

@app.route('/currentoccupation', methods=['GET', 'POST'])
def currentoccupation():
    
    if request.method == 'POST':
        # get values
        if 'current_occ_reasons' not in cache[session['token']]:
            cache[session['token']]['current_occ_reasons'] = {}
        
        cache[session['token']]['current_occ_reasons']['jobtasks'] = request.form.get('occ_jobtasks')
        cache[session['token']]['current_occ_reasons']['location'] = request.form.get('occ_location')
        cache[session['token']]['current_occ_reasons']['income'] = request.form.get('occ_income')
        cache[session['token']]['current_occ_reasons']['other'] = request.form.get('occ_other')

        ##DEBUG
        print("-- CURRENT OCCUPATION REASONS: ", cache[session['token']]['current_occ_reasons'])

        # go to next page
        return redirect(url_for('cohort'))
    
    return render_template('currentoccupation.html')

@app.route('/cohort', methods=['GET', 'POST'])
def cohort():
    
    if request.method == 'POST':
        # get values
        cache[session['token']]['career_stage'] = request.form.get('careerstage')
        cache[session['token']]['race_ethnicity'] = request.form.getlist('race_ethnicity')
        cache[session['token']]['gender'] = request.form.getlist('gender')

        ##DEBUG
        print("-- CAREER STAGE: ", cache[session['token']]['career_stage'])
        print("-- RACE-ETHNICITY: ", cache[session['token']]['race_ethnicity'])
        print("-- GENDER: ", cache[session['token']]['gender'])

        # go to next page
        return redirect(url_for('finalpage'))
    
    return render_template('cohort.html')

def calculate_perception(importance, concern, impact_severity):
    # coeff_WiWt = 0.05
    # WiWt = ((adv_warning / warning_time) -1 ) * coeff_WiWt
    # result = (coeff_I * importance) + coeff_CSI * (CSI + WiWt)

    # set coefficents
    coeff_I = 0.85
    coeff_CSI = 0.15
    
    if impact_severity > 0 : 
        CSI = (concern / impact_severity) - 1
    else:
        CSI = concern
    result = (coeff_I * importance) + coeff_CSI * CSI

    roundResult = round_and_fix(result, 1)

    return roundResult
                         
def calculate_risk_perception_chart_data(cache, finaljob):
    # set constants
    hazard_abbrev = {
        'earthquake':'eq',
        'flood':'fl',
        'landslide':'ls',
        'severe-weather':'sw',
        'volcano':'va',
        'wildfire':'wf',
    }

    # warningTime = {
    #     'earthquake': 1,
    #     'flood': 2,
    #     'landslide': 2,
    #     'severe-weather': 2,
    #     'volcano': 2,
    #     'wildfire': 2,
    # }

    # set up dataframe
    df = pd.DataFrame(columns=['hazard_name', 'hazard_abbrev', 'hazrisk_current', 'hazrisk_future', 'concern_current', 'impact_severity', 'importance_current', 'importance_future', 'perception_current', 'perception_future','change_hazrisk', 'change_perception' ])
    df['hazard_name'] = ['earthquake', 'flood', 'landslide', 'severe-weather', 'volcano', 'wildfire']
    df['hazard_abbrev'] = df['hazard_name'].map(hazard_abbrev)

    # get the data
    importance_current = cache[session['token']]['current_loc_reasons']['hazard']
    importance_future = cache[session['token']]['jobreasons']['hazard']
    hazard_concern_current = cache[session['token']]['current_haz_concern'] #[HAZARD]
    impact_severity =  cache[session['token']]['impact_severity'] #[HAZARD]
    hazard_risk_current = cache[session['token']]['current_location_haz_risk'] #['haz_HAZARD']
    hazard_risk_future = finaljob #['haz_HAZARD'] 

    # rename data to match hazard keys
    hazard_risk_future.rename(index={'haz_severe_weather': 'haz_severe-weather'}, inplace=True)
    hazard_risk_future.rename(index={'haz_fire': 'haz_wildfire'}, inplace=True)
    hazard_risk_future.rename(index={'haz_slide': 'haz_landslide'}, inplace=True)

    hazard_risk_current['haz_wildfire'] = hazard_risk_current.pop('haz_fire')
    hazard_risk_current['haz_landslide'] = hazard_risk_current.pop('haz_slide')
    hazard_risk_current['haz_severe-weather'] = hazard_risk_current.pop('haz_severe_weather')

    for haz in hazard_abbrev.keys():
        importance_current = int(importance_current)
        importance_future = int(importance_future)
        concern = int(hazard_concern_current[haz])
        impact = int(impact_severity[haz])
        risk_current = int(hazard_risk_current[f'haz_{haz}'])
        risk_future = int(hazard_risk_future[f'haz_{haz}'])
        perception_current = calculate_perception(importance_current, concern, impact) #, adv_warning_indiv, warning_time)
        perception_future = calculate_perception(importance_future, concern, impact) #, adv_warning_indiv, warning_time)
        change_hazrisk = risk_future - risk_current
        change_perception = perception_future - perception_current

        df.loc[df['hazard_name'] == haz, 'hazrisk_current'] = round_and_fix(risk_current, 1)
        df.loc[df['hazard_name'] == haz, 'hazrisk_future'] = round_and_fix(risk_future, 1)
        df.loc[df['hazard_name'] == haz, 'concern_current'] = round_and_fix(concern, 1)
        df.loc[df['hazard_name'] == haz, 'impact_severity'] = round_and_fix(impact, 1)
        df.loc[df['hazard_name'] == haz, 'importance_current'] = round_and_fix(importance_current, 1)
        df.loc[df['hazard_name'] == haz, 'importance_future'] = round_and_fix(importance_future, 1)
        df.loc[df['hazard_name'] == haz, 'perception_current'] = round_and_fix(perception_current, 1)
        df.loc[df['hazard_name'] == haz, 'perception_future'] = round_and_fix(perception_future, 1)
        df.loc[df['hazard_name'] == haz, 'change_hazrisk'] = round_and_fix(change_hazrisk, 1)
        df.loc[df['hazard_name'] == haz, 'change_perception'] = round_and_fix(change_perception, 1)
        
    # Get average of columns
    df_numerics = df.copy()
    df_numerics.drop(['hazard_name', 'hazard_abbrev'], axis=1, inplace=True)
    dfnumericCols = df_numerics.columns
    df_means = df_numerics.mean()

    # convert df_means to df
    df_means = pd.DataFrame(df_means).T
    df_means.columns = dfnumericCols

    df_means = df_means.stack().map(lambda x: round_and_fix(x, 1)).unstack()
    df_means['hazard_name'] = 'average'
    df_means['hazard_abbrev'] = 'avg'

    # Concatenate the new DataFrame with the original DataFrame
    df = pd.concat([df, df_means], ignore_index=True)

    return df

def calculate_sensitivity_zone(hsArray):
    risk = hsArray[0]
    perception = hsArray[1]

    # Rid (risk indifferent): (risk >= 2.5) and (perception < 2.5)
    # Rav (risk averse): (risk < 2.5) and (perception >= 2.5)
    # RAl (risk aware -low risk): (risk < 2.5) and (perception < 2.5)
    # RAh (risk aware - high risk): (risk >= 2.5) and (perception >= 2.5)
    # RAn (risk neutral): (risk = 2.5) and (perception = 2.5)

    if (risk >= 2.5) and (perception < 2.5):
        return 'Rid'
    elif (risk < 2.5) and (perception >= 2.5):
        return 'Rav'
    elif (risk < 2.5) and (perception < 2.5):
        return 'RAl'
    elif (risk >= 2.5) and (perception >= 2.5):
        return 'RAh'
    elif (risk == 2.5) and (perception == 2.5):
        return 'RAn'
    else:
        return None
    
def get_sensitivity_text(chartData):
    avgSensitivity = {}
    hazOrder = {
        'avg': 'Hazard average',
        'eq': 'Earthquakes',
        'fl': 'Floods',
        'wf': 'Wildfires',
        'ls': 'Landslides',
        'sw': 'Severe weather',
        'va': 'Volcanic activity',
    }

    hsCodeOrder = {1: 'RidRid',
                    2: 'RavRid',
                    3: 'RAnRid',
                    4: 'RAlRid',
                    5: 'RAhRid',
                    6: 'RavRav',
                    7: 'RidRav',
                    8: 'RAnRav',
                    9: 'RAlRav',
                    10: 'RAhRav',
                    11: 'RAnRAn',
                    12: 'RidRAn',
                    13: 'RavRAn',
                    14: 'RAlRAn',
                    15: 'RAhRAn',
                    16: 'RAlRAl',
                    17: 'RavRAl',
                    18: 'RAnRAl',
                    19: 'RAhRAl',
                    20: 'RAhRAh',
                    21: 'RidRAl',
                    22: 'RidRAh',
                    23: 'RavRAh',
                    24: 'RAnRAh',
                    25: 'RAlRAh'
                }
    dfHSData = pd.DataFrame(columns=['hazard_abbrev','hazard_name','hs_start', 'hs_end','hs_code'])   

    for index, row in chartData.iterrows():
        hazAbbrev = row['hazard_abbrev']
        hazName = hazOrder[row['hazard_abbrev']]

        # calculate the hazard Sensitivity zones and colors
        hsZoneStart = calculate_sensitivity_zone([row['hazrisk_current'], row['perception_current']])
        hsZoneEnd = calculate_sensitivity_zone([row['hazrisk_future'], row['perception_future']])
        hsZone = hsZoneStart + hsZoneEnd

        dfAdds = pd.DataFrame([[hazAbbrev, hazName, hsZoneStart, hsZoneEnd, hsZone]], columns=['hazard_abbrev', 'hazard_name', 'hs_start', 'hs_end', 'hs_code'])
        dfHSData = pd.concat([dfHSData, dfAdds], ignore_index=True)

    # get pieces and parts

    # get the text for the avg section
    avg_hsEnd = dfHSData.loc[dfHSData['hazard_abbrev'] == 'avg', 'hs_end'].values[0]
    avg_hsTrend = dfHSData.loc[dfHSData['hazard_abbrev'] == 'avg', 'hs_code'].values[0]
    avg_hsEnd_color = hazard_zone_color_lookup.get(avg_hsEnd)
    avg_hsEnd_title = hazard_zone_title_lookup.get(avg_hsEnd)
    avg_hsTrendText = next((item['text'] for item in hazardZoneTextJson['hazardZoneText'] if item['code'] == avg_hsTrend), None)

    avgSensitivity['avg'] = {
                'color': avg_hsEnd_color,
                'title': avg_hsEnd_title,
                'text': avg_hsTrendText
            }

    dfIndivHS = dfHSData.copy()
    dfIndivHS = dfIndivHS[dfIndivHS['hazard_abbrev'] != 'avg']
    
    # Create a dictionary to store hazard_names for each hs_code
    indivSensitivity = {}

    # Iterate over unique hs_code values
    for hs_code in dfIndivHS['hs_code'].unique():
        # get the last three characters of hs_code to get the color
        hs_code_end = hs_code[-3:]
        hs_code_end_color = hazard_zone_color_lookup.get(hs_code_end)
        hs_code_end_title = hazard_zone_title_lookup.get(hs_code_end)

        hs_code_start = hs_code[:3]
        hs_code_start_color = hazard_zone_color_lookup.get(hs_code_start)
        hs_code_start_title = hazard_zone_title_lookup.get(hs_code_start)

        filtered_rows = dfIndivHS[dfIndivHS['hs_code'] == hs_code]
        hazard_names = ', '.join(filtered_rows['hazard_name'].tolist())
        
        # Find the corresponding entry in hazardZoneTextJson
        hazard_zone_entry = next((item for item in hazardZoneTextJson['hazardZoneText'] if item['code'] == hs_code), None)
        
        if hazard_zone_entry:
            # Add to the dictionary
            indivSensitivity[hs_code] = {
                'start_title' : hs_code_start_title,
                'start_color': hs_code_start_color,
                'end_title' : hs_code_end_title,
                'end_color': hs_code_end_color,
                'title': hazard_zone_entry['title'],
                'hazard_names': hazard_names,
                'text': hazard_zone_entry['text']
            }

    # order indivSensitivity by hsCodeOrder order
    # Create a reverse lookup dictionary to map hs_code to their order
    order_lookup = {v: k for k, v in hsCodeOrder.items()}

    # Sort the dictionary by the order specified in hsCodeOrder
    sorted_indivSensitivity = dict(sorted(indivSensitivity.items(), key=lambda item: order_lookup.get(item[0], float('inf'))))

    return avgSensitivity, sorted_indivSensitivity

def convert_chart_data_to_json(chartData):
    # create data array like this: start and end are [Hazard Risk Current, Perception Curr] and [Hazard Risk Future, Perception Future]
    chartJson = []
    hazOrder = {
        'avg': 'Hazard average',
        'eq': 'Earthquake',
        'fl': 'Flood',
        'wf': 'Wildfire',
        'ls': 'Landslide',
        'sw': 'Severe weather',
        'va': 'Volcanic activity',
    }

    for index, row in chartData.iterrows():
        data = {}
        data['label'] = row['hazard_abbrev']
        data['label_long'] = hazOrder[row['hazard_abbrev']]
        data['start'] = [row['hazrisk_current'], row['perception_current']]
        data['end'] = [row['hazrisk_future'], row['perception_future']]
        if row['change_hazrisk'] < 0:
            chg_hazrisk = "arrow-down"
        elif row['change_hazrisk'] > 0:
            chg_hazrisk = "arrow-up"
        else:
            chg_hazrisk = "dash"
        if row['change_perception'] < 0:
            chg_perception = "arrow-down"
        elif row['change_perception'] > 0:
            chg_perception = "arrow-up"
        else:
            chg_perception = "dash"
        data['change']  = [chg_hazrisk, chg_perception]

        chartJson.append(data)

    # reorder according to hazOrder
    chartJson = sorted(chartJson, key=lambda x: list(hazOrder.keys()).index(x['label']))
    
    return chartJson

def get_factors_text(cache):

    hr_values_text = {
        1: "not important",
        2: "slightly important",
        3: "somewhat important",
        4: "very important",
        5: "extremely important"
    }
    factors_text = {
        'jobtasks': "job tasks",
        'location': "location",
        'income': "disposable income",
        'crime': "crime risk",
        'climate': "weather",
        'resources': "community resources",
        'social': "social networks",
        'other': "other factors"
    }
    current_reasons = cache[session['token']]['current_loc_reasons']
    job_reasons = cache[session['token']]['jobreasons']
    current_jobtasks = cache[session['token']]['current_occ_reasons']['jobtasks']
    # add current_jobtasks to current_reasons
    current_reasons['jobtasks'] = current_jobtasks
    
    ## DEBUG
    print("-- CURRENT REASONS INCL JOBTASKS -- ", current_reasons)

    factors = ['jobtasks', 'location', 'income',  'crime', 'climate','resources','social', 'other']
    
    hr_current = int(current_reasons["hazard"])
    hr_future = int(job_reasons["hazard"])
    hr_current_text = hr_values_text[hr_current]
    hr_future_text = hr_values_text[hr_future]
    hr_change = hr_future - hr_current

    ## DEBUG
    print("-- HAZ RISK CUR and FUTURE -- ", hr_current, hr_future)

    if hr_change < 0:
        hr_change_text = f"Hazard risk is becoming less important as you weigh your choice of location and job. You rated the importance of hazard risk as {hr_current_text} in choosing your current location and as {hr_future_text} in choosing your future job."
    elif hr_change > 0:
        hr_change_text = f"Hazard risk is becoming more important as you weigh your choice of location and job. You rated the importance of hazard risk as {hr_current_text} in choosing your current location and as {hr_future_text} in choosing your future job."
    elif hr_change == 0:
        hr_change_text = f"Hazard risk continues to be {hr_current_text} as you weigh your choice of location and job. "
    else:
        hr_change_text = None
    
    ## DEBUG
    print("-- HR CHANGE TEXT: ", hr_change_text)

    factors_current = []
    factors_future = []

    if hr_current < 5: 
        factors_current = [f for f in factors if int(current_reasons[f]) > hr_current]
        factors_current_text_start = "Factors more important than hazard risk in your choice of your current location are "

    if len(factors_current) == 0 or hr_current == 5:
        # get factors as important as hazard risk
        factors_current = [f for f in factors if int(current_reasons[f]) == hr_current]  
        factors_current_text_start = "Factors as important as hazard risk in your choice of your current location are "

    if hr_future < 5:
        factors_future = [f for f in factors if int(job_reasons[f]) > hr_future]
        factors_future_text_start = "Factors more important than hazard risk in your choice of your future job are "
   
    if len(factors_future) == 0 or hr_future == 5:
        # get factors as important as hazard risk
        factors_future = [f for f in factors if int(job_reasons[f]) == hr_future]
        factors_future_text_start = "Factors as important as hazard risk in your choice of your future job are "
    
    # get corresponding text: factors_text[f] for each factor in factors_current and factors_future
    if len(factors_current) > 0: 
        factors_current_text_items = [factors_text[f] for f in factors_current]
        if len(factors_current_text_items) > 1:
            factors_current_text = factors_current_text_start + ", ".join(factors_current_text_items[:-1]) + ", and " + factors_current_text_items[-1] + "."
        else:
            factors_current_text = factors_current_text_start + factors_current_text_items[0] + "."
    else: 
        factors_current_text = "Hazard risk is the most important factor in your choice of your current location."   

    if len(factors_future) > 0:
        factors_future_text_items = [factors_text[f] for f in factors_future]
        if len(factors_future_text_items) > 1:
            factors_future_text = factors_future_text_start + ", ".join(factors_future_text_items[:-1]) + ", and " + factors_future_text_items[-1] + "."
        else:
            factors_future_text = factors_future_text_start + factors_future_text_items[0] + "."
    else: 
        factors_future_text = "Hazard risk is the most important factor in your choice of your future job."   
    
    importance_factors_text = {'hr_change_text': hr_change_text, 
                               'factors_current_text': factors_current_text,
                               'factors_future_text': factors_future_text 
                               }
    return importance_factors_text

def get_factors_chart_data(cache):
    current_reasons = cache[session['token']]['current_loc_reasons']
    job_reasons = cache[session['token']]['jobreasons']
    current_jobtasks = cache[session['token']]['current_occ_reasons']['jobtasks']
    # add current_jobtasks to current_reasons
    current_reasons['jobtasks'] = current_jobtasks

    icdata = []
    ifdata = []
    factors = ['other', 'social', 'resources', 'climate', 'crime', 'income', 'location', 'jobtasks', 'hazard']

    for factor in factors:
        cv = int(current_reasons[factor])
        fv = int(job_reasons[factor])

        # get factor value from current_reasons and job_reasons
        # adj for 0-4 index of chart from values 1-5; If no answer (val = 0), consider it to be not important
        current_val = cv -1 if cv > 0 else 0
        job_val = fv -1 if fv > 0 else 0

        # create data arrays for importance and factors [factor, importance, value]
        for i in range(5):
            icdata.append([factors.index(factor), i, 1 if i == current_val else 0])
            ifdata.append([factors.index(factor), i, 1 if i == job_val else 0])

    return icdata, ifdata

@app.route('/finalpage', methods=['GET', 'POST'])
def finalpage():
    
    if request.method == 'POST':
        return redirect(url_for('startgame'))
    
    # Get the job information
    finaljobId = cache[session['token']]['final_job']['job_id']
    jobListId = cache[session['token']]['final_job']['jobListId']
    joblist = cache[session['token']]['jobdata'][jobListId]['joblist']
    dfJobs = pd.DataFrame(joblist)
    finaljob = dfJobs.loc[dfJobs['job_id'] == int(finaljobId)].iloc[0]
    currentLocHazRisk = cache[session['token']]['current_location_haz_risk']

    # risk perception chart data
    rpChartData = calculate_risk_perception_chart_data(cache, finaljob)
    rpChartJson = convert_chart_data_to_json(rpChartData)
    rp_avg_text, rp_indiv_text = get_sensitivity_text(rpChartData)

    # importance factors data
    icdata, ifdata = get_factors_chart_data(cache)
    importance_factors_text = get_factors_text(cache)

    return render_template('finalpage.html', job=finaljob, hsData=rpChartJson, icData=icdata, ifData=ifdata, avg_sensitivity=rp_avg_text, indiv_sensitivity=rp_indiv_text, importance_factors=importance_factors_text)

@app.route('/about')
def about():
    if request.method == 'POST':
        return redirect(url_for('startgame'))
    
    return render_template('about.html', show_footer=False)

if __name__ == '__main__':
    app.run(debug=True)

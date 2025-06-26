# GRANDE-simulation
This is the code repository for the GRANDE project's [job choice risk assessment simulation](https://grande.americangeosciences.org/data/hazard-game/)

### About the simulation
The Natural Hazards and Job Choice simulation was designed to assess how people weigh natural hazard risks against other factors, such as crime risk, salary, and cost of living, when deciding on a new job and place to live. In the game, participants were given a series of 16 job offer scenarios and had to narrow them down through several rounds to a final choice. Each job offer provided information about salary, the location’s hazard risk level, crime rate, cost of living, and other attributes, so players could consider trade-offs between financial and personal safety factors. After choosing a job, participants answered questions about why they made that choice. They were also asked about their reasons for choosing their current location and job, as well as about their experience with prior impacts from natural hazards, and concern relative to hazards where they currently reside. This setup allowed us to examine which factors drove people’s decisions and whether those with geoscience expertise would tolerate more risk than others.

This simulation is part of the American Geosciences Institute's GRANDE project which was supported by the National Science Foundation under Grant #2223004. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.

### Notes about the scripts

**createJobsDuckDb.py**

This script reads data from five database tables to create the
job\_game\_data.duckdb file that is used by the simulation. See Database
tables below for the contents and sourcing of data in each table.

**jobgame\_app.py**

This script is the main flask app that executes the simulation.

### Notes about the duckdb database tables

The following tables are required to build the duckdb file from which
the simulation operates.

**crime\_hazards\_cost\_of\_living\_combined**

This table combines the data from the FBI Crime Data Explorer, NBIRS
Tables: State tables, offenses by agency for 2022, Economic Policy
Institute (EPI) Family Budget Calculator, January 2024, and the US
Federal Emergency Management Agency, National Risk Index (NRI), and the
US Census Bureau's list of regions and divisions to assign crime, cost
of living, and hazard risk values at the city level.

| **Source** | **Name** | **Type** | **Length** | **Decimal** |
|------------|----------|----------|------------|-------------|
| n.a.       | id       | big|  int  |   |            |             |
|  FBI           |  state\_name                                 |  varchar  |  255  |          
|  FBI           |  state\_abbreviation                         |  char  |  2  |            
|  Census Bureau |  region                                      |  varchar  |  255  |          
|  Census Bureau |  division                                    |  varchar  |  255  |          
|  FBI           |  city\_name                                  |  varchar  |  255  |          
|  FBI           |  county\_name                                |  varchar  |  255  |          
|  FBI           |  county\_type                                |  varchar  |  255  |          
|  FBI           |  state\_county\_fips                         |  char  |  10  |           
|  FBI           |  crime\_rate\_total\_offenses                |  decimal  |  10         |  3  |
|  FBI           |  crime\_rate\_personal                       |  decimal  |  10         |  3  |
|  FBI           |  crime\_rate\_property                       |  decimal  |  10         |  3  |
|  FBI           |  crime\_rate\_society                        |  decimal  |  10         |  3  |
|  FBI           |  crime\_rank\_description\_total\_offenses   |  char  |  20  |           
|  FBI           |  crime\_rank\_description\_personal          |  char  |  20  |           
|  FBI           |  crime\_rank\_description\_property          |  char  |  20  |           
|  FBI           |  crime\_rank\_description\_society           |  char  |  20  |           
|  FBI           |  crime\_rank\_total\_offenses                |  int  |                     
|  FBI           |  crime\_rank\_personal                       |  int  |                     
|  FBI           |  crime\_rank\_property                       |  int  |                     
|  FBI           |  crime\_rank\_society                        |  int  |                     
|  EPI           |  col\_housing                                |  int  |                     
|  EPI           |  col\_food                                   |  int  |                     
|  EPI           |  col\_transportation                         |  int  |                     
|  EPI           |  col\_healthcare                             |  int  |                     
|  EPI           |  col\_other\_necessities                     |  int  |                     
|  EPI           |  col\_taxes                                  |  int  |                     
|  EPI           |  col\_total\_monthly\_cost                   |  int  |                     
|  EPI           |  col\_min\_salary                            |  int  |                     
|   NRI              |  haz\_overall\_risk\_rating                  |  varchar  |  255  |          
|   NRI              |  haz\_avalanche\_risk\_rating                |  varchar  |  255  |          
|   NRI              |  haz\_coastal\_flood\_risk\_rating           |  varchar  |  255  |          
|   NRI              |  haz\_cold\_wave\_risk\_rating               |  varchar  |  255  |          
|   NRI              |  haz\_drought\_risk\_rating                  |  varchar  |  255  |          
|   NRI              |  haz\_earthquake\_risk\_rating               |  varchar  |  255  |          
|   NRI              |  haz\_hail\_risk\_rating                     |  varchar  |  255  |          
|   NRI              |  haz\_heat\_wave\_risk\_rating               |  varchar  |  255  |          
|   NRI              |  haz\_hurricane\_risk\_rating                |  varchar  |  255  |          
|   NRI              |  haz\_icestorm\_risk\_rating                 |  varchar  |  255  |          
|   NRI              |  haz\_landslide\_risk\_rating                |  varchar  |  255  |          
|   NRI              |  haz\_lightning\_risk\_rating                |  varchar  |  255  |          
|   NRI              |  haz\_river\_flood\_risk\_rating             |  varchar  |  255  |          
|   NRI              |  haz\_strong\_wind\_risk\_rating             |  varchar  |  255  |          
|   NRI              |  haz\_tornado\_risk\_rating                  |  varchar  |  255  |          
|   NRI              |  haz\_tsunami\_risk\_rating                  |  varchar  |  255  |          
|   NRI              |  haz\_volcano\_risk\_rating                  |  varchar  |  255  |          
|   NRI              |  haz\_wildfire\_risk\_rating                 |  varchar  |  255  |          
|   NRI              |  haz\_winter\_weather\_risk\_rating          |  varchar  |  255  |          
|   NRI              |  haz\_overall\_risk\_rating\_rank            |  int  |                     
|   NRI              |  haz\_avalanche\_risk\_rating\_rank          |  int  |                     
|   NRI              |  haz\_coastal\_flood\_risk\_rating\_rank     |  int  |                     
|   NRI              |  haz\_cold\_wave\_risk\_rating\_rank         |  int  |                     
|   NRI              |  haz\_drought\_risk\_rating\_rank            |  int  |                     
|   NRI              |  haz\_earthquake\_risk\_rating\_rank         |  int  |                     
|   NRI              |  haz\_hail\_risk\_rating\_rank               |  int  |                     
|   NRI              |  haz\_heat\_wave\_risk\_rating\_rank         |  int  |                     
|   NRI              |  haz\_hurricane\_risk\_rating\_rank          |  int  |                     
|   NRI              |  haz\_icestorm\_risk\_rating\_rank           |  int  |                     
|   NRI              |  haz\_landslide\_risk\_rating\_rank          |  int  |                     
|   NRI              |  haz\_lightning\_risk\_rating\_rank          |  int  |                     
|   NRI              |  haz\_river\_flood\_risk\_rating\_rank       |  int  |                     
|   NRI              |  haz\_strong\_wind\_risk\_rating\_rank       |  int  |                     
|   NRI              |  haz\_tornado\_risk\_rating\_rank            |  int  |                     
|   NRI              |  haz\_tsunami\_risk\_rating\_rank            |  int  |                     
|   NRI              |  haz\_volcano\_risk\_rating\_rank            |  int  |                     
|   NRI              |  haz\_wildfire\_risk\_rating\_rank           |  int  |                     
|   NRI              |  haz\_winter\_weather\_risk\_rating\_rank    |  int  |                     

**jobZonesInterestsSalariesByState**

This table combines the data from the US Bureau of Labor Statistics,
Occupational Employment Statistics, May 2023 (BLS) and the O\*NET® 28.3
Database, U.S. Department of Labor, Employment and Training
Administration (ONET), and the US Census Bureau's list of regions and
divisions.

| **Source** | **Name** | **Type** | **Length** |
|------------|----------|----------|------------|
|  BLS           |  occ\_code\_detailed   |  char  |  12  |           
|  BLS           |  occ\_code             |  char  |  10  |           
|  BLS           |  state\_abbreviation   |  char  |  2  |            
|  Census Bureau  |  region                |  varchar  |  255  |          
|  Census Bureau  |  division              |  varchar  |  255  |          
|  BLS           |  a\_mean               |  int  |                     
|  BLS           |  a\_pct10              |  int  |                     
|  BLS           |  a\_pct25              |  int  |                     
|  BLS           |  a\_median             |  int  |                     
|  BLS           |  a\_pct75              |  int  |                     
|  BLS           |  a\_pct90              |  int  |                     
  ONET           | job\_zone             |  int  |                     

**jobDescriptions**

This table was created by extracting the job titles and descriptions for
the occupations listed in the US Bureau of Labor Statistics,
Occupational Employment Statistics, May 2023 (BLS), and using a Large
Language Model (LLM) to generate job titles and job descriptions given a
focus on a specific degree field. Degree fields were derived from the
list of degree fields in the US National Science Foundation's Scientists
and Engineers Statistical Data System. Specifically, the degree fields
we used were:

-   Art and humanities

-   Biological and agricultural sciences

-   Chemistry

-   Computer and information sciences

-   Earth, atmospheric, and ocean sciences

-   Education

-   Engineering

-   generic

-   Health

-   Management and administration

-   Mathematics and statistics

-   Physics and astronomy

-   Sales and marketing

-   Social sciences

-   Social service

-   Technology and technical fields

-   Non-Science & Engineering fields

-   Science & Engineering-related fields

We first used the LLM to generate a list of topical areas for each
degree field and then asked the LLM to create a job title and
description given the BLS title and description as a base with a focus
on the topical area.

For example, occupational code 35-2014 has a job title of "Cooks,
Restaurant" with a job description as "Prepare, season, and cook dishes
such as soups, meats, vegetables, or desserts in restaurants. May order
supplies, keep records and accounts, price items on menu, or plan menu."
The term "music" was one the topical areas assigned to the Arts &
Humanities degree field. We asked the LLM to use the base job title and
description to generate a job title and description for a job offer
posting on the theme of music. It generated the following title and
description:

    Musical Chef  
    The Musical Chef is responsible for creating a symphony of flavors by combining ingredients and cooking techniques that bring out the unique taste and texture of each dish. Utilizing a deep understanding of music theory and culinary arts, the Musical Chef crafts a menu that is both a feast for the taste buds and a harmonious composition. The ideal candidate has a background in both music and culinary arts, with a passion for creating memorable dining experiences.

Organization names in this table were generated by a combination of a
randomly assigned letter of the Greek alphabet and randomly assigned
Crayola color.

| **Source** | **Name** | **Type** | **Length** |
|------------|----------|----------|------------|
|  n.a.      |   id                     |  big  |  int  |     
|  BLS       |    occ\_code\_detailed    |  char  |  12  |
|  BLS       |    occ\_code              |  char  |  10  |
|  Degree list  |   degree\_field\_short   |  char  |  2  |0
|  Degree list  |  degree\_field          |  varchar  |  255  |
|  Synthetic  |   organization\_name     |  varchar  |  255  |
|  Synthetic  |   job\_title             |  varchar  |  255  |
|  Synthetic   |  job\_description       |  text  |     

**nri\_counties**

This table contains the data from the county-level US Federal Emergency
Management Agency, National Risk Index (NRI) dataset.

| **Source** | **Name** | **Type** | **Length** | **Decimal** |
|------------|----------|----------|------------|-------------|
|  n.a.  |   id                 |  big  |  int  |           
|   NRI        |  objectid           |  int  |               
|   NRI        |  nri\_id            |  char   |  20  |      
|   NRI        |  state              |  char   |  250  |     
|   NRI        |  stateabbrv         |  char   |  20  |      
|   NRI        |  statefips          |  char   |  20  |      
|   NRI        |  county             |  char   |  250  |     
|   NRI        |  countytype         |  char   |  250  |     
|   NRI        |  countyfips         |  char   |  20  |      
|   NRI        |  stcofips           |  char   |  20  |      
|   NRI        |  population         |  int  |               
|   NRI        |  buildvalue         |  double  |  30     |  15  | 
|   NRI        |  agrivalue          |  double  |  30     |  15  | 
|   NRI        |  area               |  double  |  30     |  15  | 
|   NRI        |  risk\_value        |  double  |  30     |  15  | 
|   NRI        |  risk\_score        |  double  |  30     |  15  | 
|   NRI        |  risk\_ratng        |  char   |  50  |      
|   NRI        |  risk\_spctl        |  double  |  30     |  15  | 
|   NRI        |  eal\_score         |  double  |  30     |  15  | 
|   NRI        |  eal\_ratng         |  char   |  50  |      
|   NRI        |  eal\_spctl         |  double  |  30     |  15  | 
|   NRI        |  eal\_valt          |  double  |  30     |  15  | 
|   NRI        |  eal\_valb          |  double  |  30     |  15  | 
|   NRI        |  eal\_valp          |  double  |  30     |  15  | 
|   NRI        |  eal\_valpe         |  double  |  30     |  15  | 
|   NRI        |  eal\_vala          |  double  |  30     |  15  | 
|   NRI        |  alr\_valb          |  double  |  30     |  15  | 
|   NRI        |  alr\_valp          |  double  |  30     |  15  | 
|   NRI        |  alr\_vala          |  double  |  30     |  15  | 
|   NRI        |  alr\_npctl         |  double  |  30     |  15  | 
|   NRI        |  alr\_vra\_npctl    |  double  |  30     |  15  | 
|   NRI        |  sovi\_score        |  double  |  30     |  15  | 
|   NRI        |  sovi\_ratng        |  char   |  50  |      
|   NRI        |  sovi\_spctl        |  double  |  30     |  15  | 
|   NRI        |  resl\_score        |  double  |  30     |  15  | 
|   NRI        |  resl\_ratng        |  char   |  50  |      
|   NRI        |  resl\_spctl        |  double  |  30     |  15  | 
|   NRI        |  resl\_value        |  double  |  30     |  15  | 
|   NRI        |  crf\_value         |  double  |  30     |  15  | 
|   NRI        |  avln\_evnts        |  double  |  30     |  15  | 
|   NRI        |  avln\_afreq        |  double  |  30     |  15  | 
|   NRI        |  avln\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  avln\_expb         |  double  |  30     |  15  | 
|   NRI        |  avln\_expp         |  double  |  30     |  15  | 
|   NRI        |  avln\_exppe        |  double  |  30     |  15  | 
|   NRI        |  avln\_expt         |  double  |  30     |  15  | 
|   NRI        |  avln\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  avln\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  avln\_hlrr         |  char   |  50  |      
|   NRI        |  avln\_ealb         |  double  |  30     |  15  | 
|   NRI        |  avln\_ealp         |  double  |  30     |  15  | 
|   NRI        |  avln\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  avln\_ealt         |  double  |  30     |  15  | 
|   NRI        |  avln\_eals         |  double  |  30     |  15  | 
|   NRI        |  avln\_ealr         |  char   |  50  |      
|   NRI        |  avln\_alrb         |  double  |  30     |  15  | 
|   NRI        |  avln\_alrp         |  double  |  30     |  15  | 
|   NRI        |  avln\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  avln\_riskv        |  double  |  30     |  15  | 
|   NRI        |  avln\_risks        |  double  |  30     |  15  | 
|   NRI        |  avln\_riskr        |  char   |  50  |      
|   NRI        |  cfld\_evnts        |  double  |  30     |  15  | 
|   NRI        |  cfld\_afreq        |  double  |  30     |  15  | 
|   NRI        |  cfld\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  cfld\_expb         |  double  |  30     |  15  | 
|   NRI        |  cfld\_expp         |  double  |  30     |  15  | 
|   NRI        |  cfld\_exppe        |  double  |  30     |  15  | 
|   NRI        |  cfld\_expt         |  double  |  30     |  15  | 
|   NRI        |  cfld\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  cfld\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  cfld\_hlrr         |  char   |  50  |      
|   NRI        |  cfld\_ealb         |  double  |  30     |  15  | 
|   NRI        |  cfld\_ealp         |  double  |  30     |  15  | 
|   NRI        |  cfld\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  cfld\_ealt         |  double  |  30     |  15  | 
|   NRI        |  cfld\_eals         |  double  |  30     |  15  | 
|   NRI        |  cfld\_ealr         |  char   |  50  |      
|   NRI        |  cfld\_alrb         |  double  |  30     |  15  | 
|   NRI        |  cfld\_alrp         |  double  |  30     |  15  | 
|   NRI        |  cfld\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  cfld\_riskv        |  double  |  30     |  15  | 
|   NRI        |  cfld\_risks        |  double  |  30     |  15  | 
|   NRI        |  cfld\_riskr        |  char   |  50  |      
|   NRI        |  cwav\_evnts        |  double  |  30     |  15  | 
|   NRI        |  cwav\_afreq        |  double  |  30     |  15  | 
|   NRI        |  cwav\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  cwav\_expb         |  double  |  30     |  15  | 
|   NRI        |  cwav\_expp         |  double  |  30     |  15  | 
|   NRI        |  cwav\_exppe        |  double  |  30     |  15  | 
|   NRI        |  cwav\_expa         |  double  |  30     |  15  | 
|   NRI        |  cwav\_expt         |  double  |  30     |  15  | 
|   NRI        |  cwav\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  cwav\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  cwav\_hlra         |  double  |  30     |  15  | 
|   NRI        |  cwav\_hlrr         |  char   |  50  |      
|   NRI        |  cwav\_ealb         |  double  |  30     |  15  | 
|   NRI        |  cwav\_ealp         |  double  |  30     |  15  | 
|   NRI        |  cwav\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  cwav\_eala         |  double  |  30     |  15  | 
|   NRI        |  cwav\_ealt         |  double  |  30     |  15  | 
|   NRI        |  cwav\_eals         |  double  |  30     |  15  | 
|   NRI        |  cwav\_ealr         |  char   |  50  |      
|   NRI        |  cwav\_alrb         |  double  |  30     |  15  | 
|   NRI        |  cwav\_alrp         |  double  |  30     |  15  | 
|   NRI        |  cwav\_alra         |  double  |  30     |  15  | 
|   NRI        |  cwav\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  cwav\_riskv        |  double  |  30     |  15  | 
|   NRI        |  cwav\_risks        |  double  |  30     |  15  | 
|   NRI        |  cwav\_riskr        |  char   |  50  |      
|   NRI        |  drgt\_evnts        |  double  |  30     |  15  | 
|   NRI        |  drgt\_afreq        |  double  |  30     |  15  | 
|   NRI        |  drgt\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  drgt\_expa         |  double  |  30     |  15  | 
|   NRI        |  drgt\_expt         |  double  |  30     |  15  | 
|   NRI        |  drgt\_hlra         |  double  |  30     |  15  | 
|   NRI        |  drgt\_hlrr         |  char   |  50  |      
|   NRI        |  drgt\_eala         |  double  |  30     |  15  | 
|   NRI        |  drgt\_ealt         |  double  |  30     |  15  | 
|   NRI        |  drgt\_eals         |  double  |  30     |  15  | 
|   NRI        |  drgt\_ealr         |  char   |  50  |      
|   NRI        |  drgt\_alra         |  double  |  30     |  15  | 
|   NRI        |  drgt\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  drgt\_riskv        |  double  |  30     |  15  | 
|   NRI        |  drgt\_risks        |  double  |  30     |  15  | 
|   NRI        |  drgt\_riskr        |  char   |  50  |      
|   NRI        |  erqk\_evnts        |  double  |  30     |  15  | 
|   NRI        |  erqk\_afreq        |  double  |  30     |  15  | 
|   NRI        |  erqk\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  erqk\_expb         |  double  |  30     |  15  | 
|   NRI        |  erqk\_expp         |  double  |  30     |  15  | 
|   NRI        |  erqk\_exppe        |  double  |  30     |  15  | 
|   NRI        |  erqk\_expt         |  double  |  30     |  15  | 
|   NRI        |  erqk\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  erqk\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  erqk\_hlrr         |  char   |  50  |      
|   NRI        |  erqk\_ealb         |  double  |  30     |  15  | 
|   NRI        |  erqk\_ealp         |  double  |  30     |  15  | 
|   NRI        |  erqk\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  erqk\_ealt         |  double  |  30     |  15  | 
|   NRI        |  erqk\_eals         |  double  |  30     |  15  | 
|   NRI        |  erqk\_ealr         |  char   |  50  |      
|   NRI        |  erqk\_alrb         |  double  |  30     |  15  | 
|   NRI        |  erqk\_alrp         |  double  |  30     |  15  | 
|   NRI        |  erqk\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  erqk\_riskv        |  double  |  30     |  15  | 
|   NRI        |  erqk\_risks        |  double  |  30     |  15  | 
|   NRI        |  erqk\_riskr        |  char   |  50  |      
|   NRI        |  hail\_evnts        |  double  |  30     |  15  | 
|   NRI        |  hail\_afreq        |  double  |  30     |  15  | 
|   NRI        |  hail\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  hail\_expb         |  double  |  30     |  15  | 
|   NRI        |  hail\_expp         |  double  |  30     |  15  | 
|   NRI        |  hail\_exppe        |  double  |  30     |  15  | 
|   NRI        |  hail\_expa         |  double  |  30     |  15  | 
|   NRI        |  hail\_expt         |  double  |  30     |  15  | 
|   NRI        |  hail\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  hail\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  hail\_hlra         |  double  |  30     |  15  | 
|   NRI        |  hail\_hlrr         |  char   |  50  |      
|   NRI        |  hail\_ealb         |  double  |  30     |  15  | 
|   NRI        |  hail\_ealp         |  double  |  30     |  15  | 
|   NRI        |  hail\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  hail\_eala         |  double  |  30     |  15  | 
|   NRI        |  hail\_ealt         |  double  |  30     |  15  | 
|   NRI        |  hail\_eals         |  double  |  30     |  15  | 
|   NRI        |  hail\_ealr         |  char   |  50  |      
|   NRI        |  hail\_alrb         |  double  |  30     |  15  | 
|   NRI        |  hail\_alrp         |  double  |  30     |  15  | 
|   NRI        |  hail\_alra         |  double  |  30     |  15  | 
|   NRI        |  hail\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  hail\_riskv        |  double  |  30     |  15  | 
|   NRI        |  hail\_risks        |  double  |  30     |  15  | 
|   NRI        |  hail\_riskr        |  char   |  50  |      
|   NRI        |  hwav\_evnts        |  double  |  30     |  15  | 
|   NRI        |  hwav\_afreq        |  double  |  30     |  15  | 
|   NRI        |  hwav\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  hwav\_expb         |  double  |  30     |  15  | 
|   NRI        |  hwav\_expp         |  double  |  30     |  15  | 
|   NRI        |  hwav\_exppe        |  double  |  30     |  15  | 
|   NRI        |  hwav\_expa         |  double  |  30     |  15  | 
|   NRI        |  hwav\_expt         |  double  |  30     |  15  | 
|   NRI        |  hwav\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  hwav\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  hwav\_hlra         |  double  |  30     |  15  | 
|   NRI        |  hwav\_hlrr         |  char   |  50  |      
|   NRI        |  hwav\_ealb         |  double  |  30     |  15  | 
|   NRI        |  hwav\_ealp         |  double  |  30     |  15  | 
|   NRI        |  hwav\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  hwav\_eala         |  double  |  30     |  15  | 
|   NRI        |  hwav\_ealt         |  double  |  30     |  15  | 
|   NRI        |  hwav\_eals         |  double  |  30     |  15  | 
|   NRI        |  hwav\_ealr         |  char   |  50  |      
|   NRI        |  hwav\_alrb         |  double  |  30     |  15  | 
|   NRI        |  hwav\_alrp         |  double  |  30     |  15  | 
|   NRI        |  hwav\_alra         |  double  |  30     |  15  | 
|   NRI        |  hwav\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  hwav\_riskv        |  double  |  30     |  15  | 
|   NRI        |  hwav\_risks        |  double  |  30     |  15  | 
|   NRI        |  hwav\_riskr        |  char   |  50  |      
|   NRI        |  hrcn\_evnts        |  double  |  30     |  15  | 
|   NRI        |  hrcn\_afreq        |  double  |  30     |  15  | 
|   NRI        |  hrcn\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  hrcn\_expb         |  double  |  30     |  15  | 
|   NRI        |  hrcn\_expp         |  double  |  30     |  15  | 
|   NRI        |  hrcn\_exppe        |  double  |  30     |  15  | 
|   NRI        |  hrcn\_expa         |  double  |  30     |  15  | 
|   NRI        |  hrcn\_expt         |  double  |  30     |  15  | 
|   NRI        |  hrcn\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  hrcn\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  hrcn\_hlra         |  double  |  30     |  15  | 
|   NRI        |  hrcn\_hlrr         |  char   |  50  |      
|   NRI        |  hrcn\_ealb         |  double  |  30     |  15  | 
|   NRI        |  hrcn\_ealp         |  double  |  30     |  15  | 
|   NRI        |  hrcn\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  hrcn\_eala         |  double  |  30     |  15  | 
|   NRI        |  hrcn\_ealt         |  double  |  30     |  15  | 
|   NRI        |  hrcn\_eals         |  double  |  30     |  15  | 
|   NRI        |  hrcn\_ealr         |  char   |  50  |      
|   NRI        |  hrcn\_alrb         |  double  |  30     |  15  | 
|   NRI        |  hrcn\_alrp         |  double  |  30     |  15  | 
|   NRI        |  hrcn\_alra         |  double  |  30     |  15  | 
|   NRI        |  hrcn\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  hrcn\_riskv        |  double  |  30     |  15  | 
|   NRI        |  hrcn\_risks        |  double  |  30     |  15  | 
|   NRI        |  hrcn\_riskr        |  char   |  50  |      
|   NRI        |  istm\_evnts        |  double  |  30     |  15  | 
|   NRI        |  istm\_afreq        |  double  |  30     |  15  | 
|   NRI        |  istm\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  istm\_expb         |  double  |  30     |  15  | 
|   NRI        |  istm\_expp         |  double  |  30     |  15  | 
|   NRI        |  istm\_exppe        |  double  |  30     |  15  | 
|   NRI        |  istm\_expt         |  double  |  30     |  15  | 
|   NRI        |  istm\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  istm\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  istm\_hlrr         |  char   |  50  |      
|   NRI        |  istm\_ealb         |  double  |  30     |  15  | 
|   NRI        |  istm\_ealp         |  double  |  30     |  15  | 
|   NRI        |  istm\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  istm\_ealt         |  double  |  30     |  15  | 
|   NRI        |  istm\_eals         |  double  |  30     |  15  | 
|   NRI        |  istm\_ealr         |  char   |  50  |      
|   NRI        |  istm\_alrb         |  double  |  30     |  15  | 
|   NRI        |  istm\_alrp         |  double  |  30     |  15  | 
|   NRI        |  istm\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  istm\_riskv        |  double  |  30     |  15  | 
|   NRI        |  istm\_risks        |  double  |  30     |  15  | 
|   NRI        |  istm\_riskr        |  char   |  50  |      
|   NRI        |  lnds\_evnts        |  double  |  30     |  15  | 
|   NRI        |  lnds\_afreq        |  double  |  30     |  15  | 
|   NRI        |  lnds\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  lnds\_expb         |  double  |  30     |  15  | 
|   NRI        |  lnds\_expp         |  double  |  30     |  15  | 
|   NRI        |  lnds\_exppe        |  double  |  30     |  15  | 
|   NRI        |  lnds\_expt         |  double  |  30     |  15  | 
|   NRI        |  lnds\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  lnds\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  lnds\_hlrr         |  char   |  50  |      
|   NRI        |  lnds\_ealb         |  double  |  30     |  15  | 
|   NRI        |  lnds\_ealp         |  double  |  30     |  15  | 
|   NRI        |  lnds\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  lnds\_ealt         |  double  |  30     |  15  | 
|   NRI        |  lnds\_eals         |  double  |  30     |  15  | 
|   NRI        |  lnds\_ealr         |  char   |  50  |      
|   NRI        |  lnds\_alrb         |  double  |  30     |  15  | 
|   NRI        |  lnds\_alrp         |  double  |  30     |  15  | 
|   NRI        |  lnds\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  lnds\_riskv        |  double  |  30     |  15  | 
|   NRI        |  lnds\_risks        |  double  |  30     |  15  | 
|   NRI        |  lnds\_riskr        |  char   |  50  |      
|   NRI        |  ltng\_evnts        |  double  |  30     |  15  | 
|   NRI        |  ltng\_afreq        |  double  |  30     |  15  | 
|   NRI        |  ltng\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  ltng\_expb         |  double  |  30     |  15  | 
|   NRI        |  ltng\_expp         |  double  |  30     |  15  | 
|   NRI        |  ltng\_exppe        |  double  |  30     |  15  | 
|   NRI        |  ltng\_expt         |  double  |  30     |  15  | 
|   NRI        |  ltng\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  ltng\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  ltng\_hlrr         |  char   |  50  |      
|   NRI        |  ltng\_ealb         |  double  |  30     |  15  | 
|   NRI        |  ltng\_ealp         |  double  |  30     |  15  | 
|   NRI        |  ltng\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  ltng\_ealt         |  double  |  30     |  15  | 
|   NRI        |  ltng\_eals         |  double  |  30     |  15  | 
|   NRI        |  ltng\_ealr         |  char   |  50  |      
|   NRI        |  ltng\_alrb         |  double  |  30     |  15  | 
|   NRI        |  ltng\_alrp         |  double  |  30     |  15  | 
|   NRI        |  ltng\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  ltng\_riskv        |  double  |  30     |  15  | 
|   NRI        |  ltng\_risks        |  double  |  30     |  15  | 
|   NRI        |  ltng\_riskr        |  char   |  50  |      
|   NRI        |  rfld\_evnts        |  double  |  30     |  15  | 
|   NRI        |  rfld\_afreq        |  double  |  30     |  15  | 
|   NRI        |  rfld\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  rfld\_expb         |  double  |  30     |  15  | 
|   NRI        |  rfld\_expp         |  double  |  30     |  15  | 
|   NRI        |  rfld\_exppe        |  double  |  30     |  15  | 
|   NRI        |  rfld\_expa         |  double  |  30     |  15  | 
|   NRI        |  rfld\_expt         |  double  |  30     |  15  | 
|   NRI        |  rfld\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  rfld\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  rfld\_hlra         |  double  |  30     |  15  | 
|   NRI        |  rfld\_hlrr         |  char   |  50  |      
|   NRI        |  rfld\_ealb         |  double  |  30     |  15  | 
|   NRI        |  rfld\_ealp         |  double  |  30     |  15  | 
|   NRI        |  rfld\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  rfld\_eala         |  double  |  30     |  15  | 
|   NRI        |  rfld\_ealt         |  double  |  30     |  15  | 
|   NRI        |  rfld\_eals         |  double  |  30     |  15  | 
|   NRI        |  rfld\_ealr         |  char   |  50  |      
|   NRI        |  rfld\_alrb         |  double  |  30     |  15  | 
|   NRI        |  rfld\_alrp         |  double  |  30     |  15  | 
|   NRI        |  rfld\_alra         |  double  |  30     |  15  | 
|   NRI        |  rfld\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  rfld\_riskv        |  double  |  30     |  15  | 
|   NRI        |  rfld\_risks        |  double  |  30     |  15  | 
|   NRI        |  rfld\_riskr        |  char   |  50  |      
|   NRI        |  swnd\_evnts        |  double  |  30     |  15  | 
|   NRI        |  swnd\_afreq        |  double  |  30     |  15  | 
|   NRI        |  swnd\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  swnd\_expb         |  double  |  30     |  15  | 
|   NRI        |  swnd\_expp         |  double  |  30     |  15  | 
|   NRI        |  swnd\_exppe        |  double  |  30     |  15  | 
|   NRI        |  swnd\_expa         |  double  |  30     |  15  | 
|   NRI        |  swnd\_expt         |  double  |  30     |  15  | 
|   NRI        |  swnd\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  swnd\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  swnd\_hlra         |  double  |  30     |  15  | 
|   NRI        |  swnd\_hlrr         |  char   |  50  |      
|   NRI        |  swnd\_ealb         |  double  |  30     |  15  | 
|   NRI        |  swnd\_ealp         |  double  |  30     |  15  | 
|   NRI        |  swnd\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  swnd\_eala         |  double  |  30     |  15  | 
|   NRI        |  swnd\_ealt         |  double  |  30     |  15  | 
|   NRI        |  swnd\_eals         |  double  |  30     |  15  | 
|   NRI        |  swnd\_ealr         |  char   |  50  |      
|   NRI        |  swnd\_alrb         |  double  |  30     |  15  | 
|   NRI        |  swnd\_alrp         |  double  |  30     |  15  | 
|   NRI        |  swnd\_alra         |  double  |  30     |  15  | 
|   NRI        |  swnd\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  swnd\_riskv        |  double  |  30     |  15  | 
|   NRI        |  swnd\_risks        |  double  |  30     |  15  | 
|   NRI        |  swnd\_riskr        |  char   |  50  |      
|   NRI        |  trnd\_evnts        |  double  |  30     |  15  | 
|   NRI        |  trnd\_afreq        |  double  |  30     |  15  | 
|   NRI        |  trnd\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  trnd\_expb         |  double  |  30     |  15  | 
|   NRI        |  trnd\_expp         |  double  |  30     |  15  | 
|   NRI        |  trnd\_exppe        |  double  |  30     |  15  | 
|   NRI        |  trnd\_expa         |  double  |  30     |  15  | 
|   NRI        |  trnd\_expt         |  double  |  30     |  15  | 
|   NRI        |  trnd\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  trnd\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  trnd\_hlra         |  double  |  30     |  15  | 
|   NRI        |  trnd\_hlrr         |  char   |  50  |      
|   NRI        |  trnd\_ealb         |  double  |  30     |  15  | 
|   NRI        |  trnd\_ealp         |  double  |  30     |  15  | 
|   NRI        |  trnd\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  trnd\_eala         |  double  |  30     |  15  | 
|   NRI        |  trnd\_ealt         |  double  |  30     |  15  | 
|   NRI        |  trnd\_eals         |  double  |  30     |  15  | 
|   NRI        |  trnd\_ealr         |  char   |  50  |      
|   NRI        |  trnd\_alrb         |  double  |  30     |  15  | 
|   NRI        |  trnd\_alrp         |  double  |  30     |  15  | 
|   NRI        |  trnd\_alra         |  double  |  30     |  15  | 
|   NRI        |  trnd\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  trnd\_riskv        |  double  |  30     |  15  | 
|   NRI        |  trnd\_risks        |  double  |  30     |  15  | 
|   NRI        |  trnd\_riskr        |  char   |  50  |      
|   NRI        |  tsun\_evnts        |  double  |  30     |  15  | 
|   NRI        |  tsun\_afreq        |  double  |  30     |  15  | 
|   NRI        |  tsun\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  tsun\_expb         |  double  |  30     |  15  | 
|   NRI        |  tsun\_expp         |  double  |  30     |  15  | 
|   NRI        |  tsun\_exppe        |  double  |  30     |  15  | 
|   NRI        |  tsun\_expt         |  double  |  30     |  15  | 
|   NRI        |  tsun\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  tsun\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  tsun\_hlrr         |  char   |  50  |      
|   NRI        |  tsun\_ealb         |  double  |  30     |  15  | 
|   NRI        |  tsun\_ealp         |  double  |  30     |  15  | 
|   NRI        |  tsun\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  tsun\_ealt         |  double  |  30     |  15  | 
|   NRI        |  tsun\_eals         |  double  |  30     |  15  | 
|   NRI        |  tsun\_ealr         |  char   |  50  |      
|   NRI        |  tsun\_alrb         |  double  |  30     |  15  | 
|   NRI        |  tsun\_alrp         |  double  |  30     |  15  | 
|   NRI        |  tsun\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  tsun\_riskv        |  double  |  30     |  15  | 
|   NRI        |  tsun\_risks        |  double  |  30     |  15  | 
|   NRI        |  tsun\_riskr        |  char   |  50  |      
|   NRI        |  vlcn\_evnts        |  double  |  30     |  15  | 
|   NRI        |  vlcn\_afreq        |  double  |  30     |  15  | 
|   NRI        |  vlcn\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  vlcn\_expb         |  double  |  30     |  15  | 
|   NRI        |  vlcn\_expp         |  double  |  30     |  15  | 
|   NRI        |  vlcn\_exppe        |  double  |  30     |  15  | 
|   NRI        |  vlcn\_expt         |  double  |  30     |  15  | 
|   NRI        |  vlcn\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  vlcn\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  vlcn\_hlrr         |  char   |  50  |      
|   NRI        |  vlcn\_ealb         |  double  |  30     |  15  | 
|   NRI        |  vlcn\_ealp         |  double  |  30     |  15  | 
|   NRI        |  vlcn\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  vlcn\_ealt         |  double  |  30     |  15  | 
|   NRI        |  vlcn\_eals         |  double  |  30     |  15  | 
|   NRI        |  vlcn\_ealr         |  char   |  50  |      
|   NRI        |  vlcn\_alrb         |  double  |  30     |  15  | 
|   NRI        |  vlcn\_alrp         |  double  |  30     |  15  | 
|   NRI        |  vlcn\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  vlcn\_riskv        |  double  |  30     |  15  | 
|   NRI        |  vlcn\_risks        |  double  |  30     |  15  | 
|   NRI        |  vlcn\_riskr        |  char   |  50  |      
|   NRI        |  wfir\_evnts        |  double  |  30     |  15  | 
|   NRI        |  wfir\_afreq        |  double  |  30     |  15  | 
|   NRI        |  wfir\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  wfir\_expb         |  double  |  30     |  15  | 
|   NRI        |  wfir\_expp         |  double  |  30     |  15  | 
|   NRI        |  wfir\_exppe        |  double  |  30     |  15  | 
|   NRI        |  wfir\_expa         |  double  |  30     |  15  | 
|   NRI        |  wfir\_expt         |  double  |  30     |  15  | 
|   NRI        |  wfir\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  wfir\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  wfir\_hlra         |  double  |  30     |  15  | 
|   NRI        |  wfir\_hlrr         |  char   |  50  |      
|   NRI        |  wfir\_ealb         |  double  |  30     |  15  | 
|   NRI        |  wfir\_ealp         |  double  |  30     |  15  | 
|   NRI        |  wfir\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  wfir\_eala         |  double  |  30     |  15  | 
|   NRI        |  wfir\_ealt         |  double  |  30     |  15  | 
|   NRI        |  wfir\_eals         |  double  |  30     |  15  | 
|   NRI        |  wfir\_ealr         |  char   |  50  |      
|   NRI        |  wfir\_alrb         |  double  |  30     |  15  | 
|   NRI        |  wfir\_alrp         |  double  |  30     |  15  | 
|   NRI        |  wfir\_alra         |  double  |  30     |  15  | 
|   NRI        |  wfir\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  wfir\_riskv        |  double  |  30     |  15  | 
|   NRI        |  wfir\_risks        |  double  |  30     |  15  | 
|   NRI        |  wfir\_riskr        |  char   |  50  |      
|   NRI        |  wntw\_evnts        |  double  |  30     |  15  | 
|   NRI        |  wntw\_afreq        |  double  |  30     |  15  | 
|   NRI        |  wntw\_exp\_area    |  double  |  30     |  15  | 
|   NRI        |  wntw\_expb         |  double  |  30     |  15  | 
|   NRI        |  wntw\_expp         |  double  |  30     |  15  | 
|   NRI        |  wntw\_exppe        |  double  |  30     |  15  | 
|   NRI        |  wntw\_expa         |  double  |  30     |  15  | 
|   NRI        |  wntw\_expt         |  double  |  30     |  15  | 
|   NRI        |  wntw\_hlrb         |  double  |  30     |  15  | 
|   NRI        |  wntw\_hlrp         |  double  |  30     |  15  | 
|   NRI        |  wntw\_hlra         |  double  |  30     |  15  | 
|   NRI        |  wntw\_hlrr         |  char   |  50  |      
|   NRI        |  wntw\_ealb         |  double  |  30     |  15  | 
|   NRI        |  wntw\_ealp         |  double  |  30     |  15  | 
|   NRI        |  wntw\_ealpe        |  double  |  30     |  15  | 
|   NRI        |  wntw\_eala         |  double  |  30     |  15  | 
|   NRI        |  wntw\_ealt         |  double  |  30     |  15  | 
|   NRI        |  wntw\_eals         |  double  |  30     |  15  | 
|   NRI        |  wntw\_ealr         |  char   |  50  |      
|   NRI        |  wntw\_alrb         |  double  |  30     |  15  | 
|   NRI        |  wntw\_alrp         |  double  |  30     |  15  | 
|   NRI        |  wntw\_alra         |  double  |  30     |  15  | 
|   NRI        |  wntw\_alr\_npctl   |  double  |  30     |  15  | 
|   NRI        |  wntw\_riskv        |  double  |  30     |  15  | 
|   NRI        |  wntw\_risks        |  double  |  30     |  15  | 
|   NRI        |  wntw\_riskr        |  char   |  50  |      
|   NRI        |  nri\_ver           |  char   |  50  |      

**zipcode\_city\_county\_crosswalk**

This table contains data from the US Housing & Urban Development-US
Postal Service ZIP Code crosswalk.

| **Source** | **Name** | **Type** | **Length** |
|------------|----------|----------|------------|
  n.a.       |  id                    |  big  |  int  |     
  HUD        |  state\_abbreviation   |  char  |  2  |
  HUD        |  zipcode               |  char  |  10  |
  HUD        |  county\_name          |  varchar  |  255  |
  HUD        |  city\_name            |  varchar  |  255  |
  HUD        |  state\_county\_fips   |  char  |  10  |

import ssl
import json
from urllib.request import urlopen
from time import sleep

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.express.colors as pc


ssl._create_default_https_context = ssl._create_unverified_context

@st.cache_data
def load_json():
    # File Authentication and Data Frame Creation    
    try:
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            counties = json.load(response)
            return counties
    
    except json.decoder.JSONDecodeError as error:
        print("Failed to load JSON data:", error)
    

@st.cache_data
def load_data():
    # sdoh_path = r"C:\Users\ciar\Documents\dylan\data\sdoh.csv"
    # sdoh_path = r"C:\Users\admin\Downloads\dashboard_codes\sdoh.csv"
    sdoh_path = "sdoh.csv"
    sdoh = pd.read_csv(sdoh_path, dtype={"COUNTYFIPS":str, "STATEFIPS":str}, low_memory=False)
    return sdoh
    

# Columns and Labels to use in "SDOHs Menu"
sdoh_options = ["ACS_PCT_HH_PUB_ASSIST",    # poverty
                "ACS_TOT_CIVIL_EMPLOY_POP", # employment
                "ACS_PCT_LT_HS",            # education
                "ACS_PCT_UNINSURED",        # insurance_coverage
                "HIFLD_MIN_DIST_UC",        # healthcare_access
                "ACS_PCT_GRANDP_NO_RESPS"]  # extended_family
labels_for_counties = ["% Families w/ Public Income/Food Asst",         # poverty
                        "Total Employed Civilians (16+)",                # employment
                        "% Pop. w/ Less Than HS Diploma (25+)",          # education
                        "% Pop. w/o Health Insurance Cov.",              # insurance_coverage
                        "Min. Miles to Nearest Urgent Care",             # healthcare_access
                        "% Child Living w/ Grandpa, Not Legal Guardian"] # extended_family
dict_sdohLabels = dict(zip(sdoh_options, labels_for_counties))


# Descriptions to display extra information to users
descriptions_for_counties = ["Percentage of households with public assistance income or food stamps/SNAP (ZCTA level)",                                          # poverty
                             "Total civilian employed population (ages 16 and over, ZCTA level)",                                                             # employment
                             "Percentage of population with less than high school education (ages 25 and over, ZCTA level)",                                  # education
                             "Percentage of population with no health insurance coverage (ZCTA level)",                                                       # insurance_coverage
                             "Minimum distance in miles to the nearest urgent care, calculated using population weighted tract ZIP centroids in the county",  # healthcare_access
                             "Percentage of children living with grandparent householder whose grandparent is not responsible for them (ZCTA level)"]         # extended_family  
dict_sdohDescriptions = dict(zip(sdoh_options, descriptions_for_counties))


# Columns and Labels to use in "Labs Menu"
lab_options = ["albumin_urine", "bun", "creatinine_serum", "creatinine_urine"]
labels_for_dots = ["Albumin Urine", "Blood Urea Nitrogen", "Creatinine Serum", "Creatinine Urine"]
dict_labLabels = dict(zip(lab_options, labels_for_dots))



st.set_page_config(page_title="Dashboard - Kidney Disease",
                   page_icon=":test_tube:",
                   menu_items={"Get help":"mailto:dylan.cedres@upr.edu",
                               "Report a Bug":"mailto:dylan.cedres@upr.edu",
                               "About":"Dashboard with Kidney Disease Lab Data and Social Determinants of Health Indices"},
                   layout="wide")

counties = load_json()
sdoh = load_data()

st.title("**Dashboard:** \n  **Social Determinants of Health and Kidney Disease Lab Data**")
st.divider()
sleep(0.5)
# st.title("Dashboard: Social Determinants of Health and Kidney Disease Lab Data")
# st.header("Dashboard: Social Determinants of Health and Kidney Disease Lab Data")


# Determines the Menus placement format
col1, col2 = st.columns([0.20,0.80], gap="small")
    
with col1:
    # Menu to change the current SDOH, for the Map's color intensities
    sdoh_selection = st.selectbox(key="current_sdoh",
                                  label="SDOH Options", 
                                  options=sdoh_options, 
                                  index=0, 
                                  format_func=lambda x: dict_sdohLabels[x])
                                  # format_func=lambda x: str(sdoh_options.index(x)+1) + ". " + dict_sdohLabels[x])
    
    # Menu to change the current Lab, for the Dots' color intensities
    lab_selection = st.selectbox(key="current_lab",
                                 label="Lab Options", 
                                 options=lab_options,
                                 index=0,
                                 format_func=lambda y: dict_labLabels[y])
                                 # format_func=lambda y: str(lab_options.index(y)+1) + ". " + dict_labLabels[y])





# Puerto Rico Choropleth Map containing Counties with SDOH Data
mapp = px.choropleth(data_frame=sdoh,                                          # dataframe to use
                     geojson=counties,                                         # establishes coordinates of Puerto Rico to trace its map
                     locations="COUNTYFIPS",                                   # determines considered locations, used for plot traces and updates
                     fitbounds="locations",                                    # associates locations with plot handling
                     scope="south america",                                    # sets section of world map
                     center=dict(lat=18.245, lon=-66.255),                     # sets center coordinate of map projection
                     color=sdoh_selection,                                     # counties color intensities
                     color_continuous_scale=pc.sequential.Purples,             # color scale for color intensities
                     # range_color=[0.35, 1],                                  # min and max color intensities for counties
                     labels=dict_sdohLabels,                                   # labels for sdohs
                     hover_name="COUNTY",                                      # counties names
                     # hover_data={sdoh_selection:True, "COUNTYFIPS":False},   # info contained in counties
                     hover_data={sdoh_selection:True, "COUNTYFIPS":False},     # 
                     width=1200,                                               # map horizontal size/length
                     height=1000)                                               # map vertical size/length
                     # custom_data=sdoh_options)

# Map Background Color
mapp.update_geos(bgcolor="cornflowerblue")  # map background color

# Map Legend Properties
mapp.update_traces(name=dict_sdohLabels[sdoh_selection], # new name of symbol
                   showlegend=True,                      # allows to be shown in the legend
                   legendrank=1,                         # first symbol in the legend
                   legendwidth=10)                       # width of legend box

# Map Figure Layout
mapp.update_layout(margin=dict(r=0, t=0, l=0, b=0),  # Application Boundaries
                   autosize=False,                   # allows custom size
                   paper_bgcolor="indigo",           # application background color
                   
                   title=dict(                       # Main Title Design
                       automargin=True,              # 
                       pad=dict(t=0, l=0, b=0, r=0), # 
                       x=0.50,                       # 
                       y=0.90,                       # 
                       xref="paper",                 # 
                       yref="paper",                 # 
                       xanchor="center",             # 
                       yanchor="top",                # 
                       
                       text="Puerto Rico<br>"        # 
                       "SDOHs-Kidney Disease",       
                       
                       font=dict(                    # 
                           color="purple",           # 
                           family="Rockwell",        # 
                           size=16)),                # 
                   
                   legend=dict(                      # Legend Design 
                       x=0.98,                       # x position 
                       y=0.08,                       # y position
                       
                       bgcolor="white",              # legend background color
                       bordercolor="midnightblue",   # legend border lines color
                       borderwidth=3,                # legend border lines thickness 
                       
                       entrywidth=1,                 # space between symbols and labels
                       entrywidthmode="pixels",      # determines unit of measurement
                       itemwidth=45,                 # size of symbols inside the legend
                       
                       font=dict(                    # Legend Labels
                           color="black",            # labels text color
                           family="Rockwell",        # labels font type
                           size=12),                 # labels text size
                       
                       title=dict(                   # Legend Title Text
                           text="Dashboard Legend",  # contents of legend title
                           
                           font=dict(                # Legend Title Font
                               color="black",        # text color for legend title
                               family="Rockwell",    # font type for legend title
                               size=16))))           # text size for legend title

@st.cache_data
def update_mapp():
    mapp.update_traces(selector=dict(type="choropleth"),     # determines map type
                       visible=True,                         # allows this trace to be drawn
                       z=sdoh[sdoh_selection],               # new color intensities
                       name=dict_sdohLabels[sdoh_selection]) # new name of symbol
                       # showlegend=True,                      # allows to be shown in the legend
                       # legendrank=1)                         # first symbol in the legend
    
    # label = dict_sdohLabels[sdoh_selection]
    # if "%" in label:
        # st.write(label)
        # mapp.update_traces(hovertemplate=[current_sdoh+" %: x:.2f"])
        # mapp.update_traces(hovertemplate="<br>".join([label+": %{"+sdoh_selection+":%}"]))





# Puerto Rico Scattergeo Map containing County Coordinate with Lab Data
# Counties without lab data: Añasco, Florida, Hormigueros, Las Marías, and Orocovis
dots = px.scatter_geo(data_frame=sdoh,
                      lat="lat",
                      lon="lon",
                      fitbounds="locations",
                      scope="south america",                                       # sets section of world map
                      labels=dict_labLabels,                                       # labels for labs
                      hover_name="COUNTY",                                         # dots names
                      hover_data={lab_selection:":.2f", "lat":False, "lon":False}, # info contained in dots
                      size=lab_selection,                                          # dots sizes
                      size_max=10)                                                 # sets maximum size dots can have
                      # color=lab_selection,                                       # dots color intensities
                      # color_continuous_scale=pc.sequential.Oranges,              # color scale for color intensities
                      # range_color=[0.30, 1.0],                                   # min and max color intensities for dots 
                      # opacity=0.75,                                              # transparency level for dots 

dots.update_traces(showlegend=True,                                        # allows to be shown in the legend
                   legendrank=2,                                           # second symbol in the legend
                   name=dict_labLabels[lab_selection], # sets the trace name in the legend and on datum hover 
                   
                   hoverlabel=dict(align="left",                           # sets text to be aligned to the left
                                   bgcolor="indigo",                       # hoverbox background color
                                   bordercolor="black"),                   # hoverbox edges color
                   
                   marker=dict(
                       line=dict(width=1.3, color="black"),                # dots borders line thickness & color
                       autocolorscale=False,                               # allows custom colorscale
                       cauto=False,                                        # allows custom inferior/superior limits & midpoint
                       color=sdoh[lab_selection],                          # determines color intensities
                       colorscale="Oranges",                               # determines color scale for color intensities
                       reversescale=True))                                 # reverses bright and dark values
                       # showscale=True,                                   # displays scale values-to-color-intensities
                       # cmax=sdoh[lab_selection].sort_values().loc[38]))  # midpoint

@st.cache_data
def update_dots():
    dots.update_traces(visible=True,
                       name=dict_labLabels[lab_selection], # sets the trace name in the legend and on datum hover 
                       marker_color=sdoh[lab_selection])   # determines color intensities





# Combines the Dots Traces of the Scattergeo Map to the Counties Traces of the Choropleth Map, based on Puerto Rico's Coordinates.
mapp.append_trace(dots.data[0], row="all", col="all")


with col2:
    # Display the plot and all its traces
    st.plotly_chart(mapp,
                    use_container_width=True,
                    config={"displayModeBar":"hover",  # Sets the mode bar to appear only when the mouse is inside the plot
                            "displaylogo":False})      # Removes the Plotly-Dash logo from appearing in the mode bar options

# st.write(pc.sequential.Oranges)
# arange = np.arange(start=0.10, stop=1.00, step=0.10)
# st.write(sdoh[lab_selection[arange]])
# description = st.write(sdoh[lab_selection].describe(percentiles=arange))


if sdoh_selection:
    update_mapp()
    sleep(0.5)
    st.toast(body="Current SDOH  %s" % dict_sdohLabels[sdoh_selection], icon="⚕️")
        
if lab_selection:
    update_dots()
    sleep(0.5)
    st.toast(body="Current Lab " + dict_labLabels[lab_selection], icon="🧪")

########################################################################################
########################################################################################
# oranges=["darkgoldenrod","goldenrod","sandybrown","darkorange","orange"]
# oranges = pc.sequential.Oranges
# st.write(oranges)
# describe = sdoh[current_lab].describe()
# dic_DotsColors= dict.fromkeys(sdoh[current_lab].sort_values())


# for lab_val in dic_DotsColors.keys():
#     if lab_val>describe["min"] and lab_val<=describe["25%"]:
#         dic_DotsColors.update({lab_val:oranges[1]})
#     elif lab_val>describe["25%"] and lab_val<=describe["50%"]:
#         dic_DotsColors.update({lab_val:oranges[2]})
#     elif lab_val>describe["50%"] and lab_val<=describe["75%"]:
#         dic_DotsColors.update({lab_val:oranges[3]})
#     elif lab_val>describe["75%"] and lab_val<=describe["max"]:
#         dic_DotsColors.update({lab_val:oranges[4]})
#     else:
#         dic_DotsColors.update({lab_val:oranges[0]})

# dots.update_geos(visible=True,
#                  bgcolor="cornflowerblue",
#                  landcolor="green",
#                  #projection=dict(distance=10), scale=0))
#                  showcountries=True,
#                  showframe=True)
# dots.update_annotations(x=0,
#                         y=0,
#                         yanchor="bottom",
#                         text="TESTING!",
#                         arrowsize=3, 
#                         arrowwdith=2)
# mapp.add_scattergeo(lat=sdoh["lat"],
#                     lon=sdoh["lon"],
#                     ids=sdoh["COUNTY"],
#                     locations=sdoh["COUNTYFIPS"],
#                     geojson=counties)
                    # projection="mercator",
                    # scope="south america")
########################################################################################
########################################################################################
# sdoh_options = ["ACS_PCT_INC50_ABOVE65", "ACS_PCT_INC50_BELOW17", "ACS_PCT_HEALTH_INC_BELOW137", 
#                        "ACS_PCT_HEALTH_INC_138_199", "ACS_PCT_HEALTH_INC_200_399", "ACS_PCT_HEALTH_INC_ABOVE400", 
#                        "ACS_PCT_HH_PUB_ASSIST", #poverty
#                        "ACS_TOT_CIVIL_EMPLOY_POP", #employment
#                        "ACS_PCT_COLLEGE_ASSOCIATE_DGR", "ACS_PCT_BACHELOR_DGR", "ACS_PCT_NO_WORK_NO_SCHL_16_19", 
#                        "ACS_PCT_GRADUATE_DGR", "ACS_PCT_HS_GRADUATE", "ACS_PCT_LT_HS", 
#                        "ACS_PCT_POSTHS_ED", #education
#                        "ACS_PCT_UNINSURED", #insurance_coverage
#                        "HIFLD_MIN_DIST_UC", "POS_MIN_DIST_ED", "POS_MIN_DIST_ALC", #healthcare_access
#                        "ACS_PCT_GRANDP_NO_RESPS"#family_extended
#                 ]
# dict_sdohDescriptions = ["Percentage of population with income to poverty ratio under 0.50 (ages 65 and over, ZCTA level)",
#                 "Percentage of children with income to poverty ratio under 0.50 (ages 17 and below, ZCTA level)", 
#                 "Percentage of population under 1.37 of the poverty threshold (relevant for health insurance coverage, ZCTA level)", 
#                 "Percentage of population between 1.38 and 1.99 of the poverty threshold (relevant for health insurance coverage, ZCTA level)", 
#                 "Percentage of population between 2.00 and 3.99 of the poverty threshold (relevant for health insurance coverage, ZCTA level)", 
#                 "Percentage of population over 4.00 of the poverty threshold (relevant for health insurance coverage, ZCTA level)", 
#                 "Percentage of households with public assistance income or food stamps/SNAP (ZCTA level)", 
#                 "Total civilian employed population (ages 16 and over, ZCTA level)", 
#                 "Percentage of population with some college or associate's degree (ages 25 and over, ZCTA level)", 
#                 "Percentage of population with a bachelor's degree (ages 25 and over, ZCTA level)", 
#                 "Percentage of teens and adults who are unemployed and not in school (between ages 16 and 19, ZCTA level)", 
#                 "Percentage of population with a master's or professional school degree or doctorate (ages 25 and over, ZCTA level)", 
#                 "Percentage of population with only high school diploma (ages 25 and over, ZCTA level)", 
#                 "Percentage of population with less than high school education (ages 25 and over, ZCTA level)", 
#                 "Percentage of population with any postsecondary education (ages 25 and over, ZCTA level)", 
#                 "Percentage of population with no health insurance coverage (ZCTA level)", 
#                 "Minimum distance in miles to the nearest urgent care, calculated using population weighted tract ZIP centroids in the county", 
#                 "Minimum distance in miles to the nearest emergency department, calculated using population weighted tract ZIP centroids in the county", 
#                 "Minimum distance in miles to the nearest hospital with alcohol and drug abuse inpatient care, calculated using population weighted tract ZIP centroids in the county", 
#                 "Percentage of children living with grandparent householder whose grandparent is not responsible for them (ZCTA level)"]
########################################################################################
########################################################################################

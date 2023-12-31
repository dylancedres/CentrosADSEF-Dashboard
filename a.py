import ssl
import json
from urllib.request import urlopen

import numpy as np
import pandas as pd

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.express.colors as pc


ssl._create_default_https_context = ssl._create_unverified_context

# File Authentication
# @st.cache_data
def load_json():
    try:
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            return json.load(response)
    
    except json.decoder.JSONDecodeError as error:
        st.write("Failed to load JSON data - Check Interntet Connection or Server Data Fetch Request:", error)
        st.write("")
        
        print("Failed to load JSON data - Check Interntet Connection or Server Data Fetch Request:", error)
        print("")
    

# Data Frame Creation
@st.cache_data
def load_data():
    sdoh_path = "sdoh.csv"
    return pd.read_csv(sdoh_path, dtype={"COUNTYFIPS":str, "STATEFIPS":str}, low_memory=False)
    


# Columns and Labels to use in "SDOHs Dropdown Menu"
sdoh_options = [
    # poverty
    "ACS_PCT_INC50_ABOVE65",          
    "ACS_PCT_HEALTH_INC_BELOW137",
    "ACS_PCT_HEALTH_INC_138_199",
    "ACS_PCT_HEALTH_INC_200_399",
    "ACS_PCT_HEALTH_INC_ABOVE400",
    "ACS_PCT_HH_PUB_ASSIST",
    # education
    "ACS_PCT_COLLEGE_ASSOCIATE_DGR",
    "ACS_PCT_BACHELOR_DGR",
    "ACS_PCT_GRADUATE_DGR",
    "ACS_PCT_HS_GRADUATE",
    "ACS_PCT_LT_HS",
    "ACS_PCT_POSTHS_ED",
    # employment
    "ACS_TOT_CIVIL_EMPLOY_POP",
    # insurance coverage
    "ACS_PCT_UNINSURED",
    # healthcare access
    "HIFLD_MIN_DIST_UC",
    "POS_MIN_DIST_ED",
    "POS_MIN_DIST_ALC",
    # disability
    "ACS_PCT_DISABLE",
    "ACS_PCT_NONVET_DISABLE_18_64",
    "ACS_PCT_VET_DISABLE_18_64",
    # mental health
    "MMD_ANXIETY_DISD",
    "MMD_DEPR_DISD"
    ]        

labels_for_counties = [
    # poverty
    "Percentage of People Under 0.50 of the Income-to-Poverty Ratio (Ages 65 and over) ",
    "Percentage of People Under 1.37 of the Poverty Threshold ",
    "Percentage of People Between 1.38 and 1.99 of the Poverty Threshold ",
    "Percentage of People Between 2.00 and 3.99 of the Poverty Threshold ",
    "Percentage of People Over 4.00 of the Poverty Threshold ",
    "Percentage of Families With Public Income or Food Asssitance ",
    # education
    "Percentage of People with Some College or Associate's Degree (Ages 25 and over) ",
    "Percentage of People with a Bachelor's Degree (Ages 25 and over) ",
    "Percentage of People with a Master's Degree, Professional School Degree, or Doctoral Degree (Ages 25 and over) ",
    "Percentage of People with only high school diploma (Ages 25 and over) ",
    "Percentage of People with Less Than High School Education (Ages 25 and over) ",
    "Percentage of People With Any Postsecondary Education (Ages 25 and over) ",
    # employment
    "Number of Employed Civilians (Thousands) ",
    # insurance converage
    "Percentage of People without Health Insurance Coverage ",
    # healthcare access
    "Miles to Nearest Urgent Care ",
    "Distance in Miles to the Nearest Emergency Department ",
    "Distance in Miles to the Nearest Hospital With Alcohol and Drug Abuse Inpatient Care ",
    # disability
    "Percentage of People with a Disability ",
    "Percentage of Nonveteran Civilians With a Disability (Ages Between 18 and 64) ",
    "Percentage of Veteran Civilians With a Disability (Ages Between 18 and 64) ",
    # mental health
    "Prevalence of Anxiety Disorders Among Medicare Beneficiaries ",
    "Prevalence of Depressive Disorders Among Medicare Beneficiaries "
    ]

descriptions_for_counties = [
    # poverty
    "Percentage of People with Ratio of Income to Poverty Ratio Under 0.50 (Ages 65 and over)."
    " (Income-to-Poverty Ratio (IPR)- Total Family Income divided by the Poverty Threshold).",
    "Percentage of People Under 1.37 of the Poverty Threshold (Relevant for Health Insurance Coverage)."
    " (Measured by the Annual Cost of Necessities).",
    "Percentage of People Between 1.38 and 1.99 of the Poverty Threshold (Relevant for Health Insurance Coverage)."
    " (Measured by the Annual Cost of Necessities).",
    "Percentage of People Between 2.00 and 3.99 of the Poverty Threshold (Relevant for Health Insurance Coverage)."
    " (Measured by the Annual Cost of Necessities).",
    "Percentage of People Over 4.00 of the Poverty Threshold (Relevant for Health Insurance Coverage)."
    " (Measured by the Annual Cost of Necessities).",
    "Percentage of Families that receive Public Assistance Income or Food Stamps/SNAP." 
    " (Supplemental Nutrition Assistance Program).",
    # education
    "Percentage of People with Some College or Associate's Degree (Ages 25 and over).",
    "Percentage of People with a Bachelor's Degree (Ages 25 and over).",
    "Percentage of People with a Master's Degree, Professional School Degree, or Doctoral Degree (Ages 25 and over).",
    "Percentage of People with Only High School Diploma (Ages 25 and over).",
    "Percentage of People With Less Than a High School Education (Ages 25 and over).",
    "Percentage of People With Any Postsecondary Education (Ages 25 and over).",
    # employment
    "Number (Thousands) of Employed Civilians (Ages 16 and over).",
    # insurance converage
    "Percentage of People Without Health Insurance Coverage.",
    # healthcare access
    "Distance in Miles to the Nearest Urgent Care Center (based on ZIP Codes).",
    "Distance in Miles to the Nearest Emergency Department (based on ZIP Codes).",
    "Distance in Miles to the Nearest Hospital With Alcohol and Drug Abuse Inpatient Care (based on ZIP Codes).",
    # disability
    "Percentage of People with a Disability.",
    "Percentage of Nonveteran Civilians With a Disability (Ages Between 18 and 64).",
    "Percentage of Veteran Civilians With a Disability (Ages Between 18 and 64).",
    # mental health
    "Prevalence of Anxiety Disorders Among Medicare (Dual and Non-dual) Beneficiaries.",
    "Prevalence of Depressive Disorders Among Medicare (Dual and Non-dual) Beneficiaries."
    ]    

sdoh_tickvals=[3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000, 
               11000000, 12000000, 13000000, 14000000, 15000000, 16000000, 17000000]

dict_sdohLabels = dict(zip(sdoh_options, labels_for_counties))

dict_sdohDescriptions = dict(zip(sdoh_options, descriptions_for_counties))



# Columns and Labels to use in "Labs Menu"
lab_options = ["albumin_urine", "bun", "creatinine_serum", "creatinine_urine"]

labels_for_dots = ["Average of Albumin Urine lab test ", 
                   "Average of Blood Urea Nitrogen lab test ", 
                   "Average of Creatinine Serum lab test ", 
                   "Average of Creatinine Urine lab test "]

lab_dticks = [5, 2, 0.1, 15]


dict_labLabels = dict(zip(lab_options, labels_for_dots))
dict_labsDticks = dict(zip(lab_options, lab_dticks))



# Dictionary with all labels
dict_Labels = {**dict_labLabels, **dict_sdohLabels}
dict_Labels["COUNTY"] = "County "



########################################
# --DASHBOARD APPLICATION START LINE-- #
########################################

st.set_page_config(layout="wide",
                   page_title="PR Kidney Disease-SDOH",
                   page_icon=":test_tube:",
                   menu_items={"Get help":"mailto:dylan.cedres@upr.edu",
                               "Report a Bug":"mailto:dylan.cedres@upr.edu",
                               "About":"Dashboard with Kidney Disease Lab Data and Social Determinants of Health Indices"})


counties = load_json()  # Puerto Rico's Map Information
sdoh = load_data()      # SDOHs and Labs Data


# st.markdown("""<style>
#                   div:is([data-testid=stHorizontalBlock]) [column-gap=1rem]{
#                     column-gap: 0.9rem;
#                     row-gap=0.9rem
#                   }
#             </style>""", unsafe_allow_html=True)


### Dashboard Main Title ###
logo1, title, logo2 = st.columns([0.12, 0.78, 0.10])
# logo1, title, logo2 = st.columns([0.15, 0.10, 0.75])
# logo, buff, title = st.columns([0.15, 0.10, 0.75])

# logo, logo_buff = st.columns([0.25, 0.75])
# title_buff, title = st.columns([0.34, 0.66])
# title_buff, title2 = st.columns([0.28, 0.72])
# title1, title_buff, title2 = st.columns([0.20, 0.30, 0.50])

# with title1:
    # Application's Main Title (LEFT)
    # st.subheader("Kidney Disease Lab Test / Social Determinants of Health (SDoH)")
    # st.title("Dashboard: Social Determinants of Health and Kidney Disease Lab Data")
#     # st.header("Dashboard: Social Determinants of Health and Kidney Disease Lab Data")
# with logo:
#     st.image("logo.jpeg", width=200, output_format="PNG")

with logo1:
    # st.image("logo_ccr_rcmi.png", use_column_width=True)
    st.markdown("""<a href="https://rcmi.rcm.upr.edu/" hreflang="en" target="_blank">
                      <img style="vertical-align:top; background-color:white; font-size:16px; color:black;"
                      src="https://raw.githubusercontent.com/dylancedres/SDOH-Dashboard/main/logo_ccr_rcmi.png" 
                      alt="CCR RCMI Logo" width="176px" height="108px">
                </a>""", unsafe_allow_html=True)

with title:
    # Application's Main Title (CENTER)
    st.markdown("""<p style="text-align:center; font-weight:bold; font-size:30px">
                    <br>Kidney Disease Lab Test / Social Determinants of Health (SDoH) - Puerto Rico</p>
                """, unsafe_allow_html=True)
    # st.subheader("**Kidney Disease Lab Test / Social Determinants of Health (SDoH) - Puerto Rico**", anchor=False)
    
with logo2:
    # st.image("logo_aim_ahead.png", use_column_width=True)
    st.markdown("""<a href="https://www.aim-ahead.net/" hreflang="en" target="blank">
                    <img style="vertical-align:top; background-color:white; font-size:16px; color:black;"
                    src="https://www.aim-ahead.net/media/4swfpq0h/aim_ahead_600x474.png?width=180&height=142&mode=max"
                    alt="AIM AHEAD Logo" width="164px" height="114px">
                </a>""", unsafe_allow_html=True)


# Hide Images View Fullscreen
st.markdown("""<style>
                button[title="View fullscreen"]{
                visibility: hidden;}
            </style>""", unsafe_allow_html=True)


st.markdown(body="<br><br>", unsafe_allow_html=True)

### Dropdown Menus and SDoHs Descriptions ###
col1, col2 = st.columns([0.20, 0.80], gap="medium")

with col1:
    # st.markdown(body="##### Select the Kidney lab test")
    st.markdown("""<p style="text-align:left; font-weight:bold; font-size:22px">
                   <br><br>Select the Kidney lab test
                </p>""", unsafe_allow_html=True)
    
    # Labs Menu
    lab_selection = st.selectbox(key="current_lab",
                                 label="**Select the Kidney lab test**", 
                                 label_visibility="collapsed",
                                 options=lab_options,
                                 index=0,
                                 format_func=lambda y: dict_labLabels[y])
                                 # format_func=lambda y: str(lab_options.index(y)+1) + ". " + dict_labLabels[y])

    # SDOHs Menu
    # st.markdown(body="##### Select the SDoH")
    st.markdown("""<p style="text-align:left; font-weight:bold; font-size:22px">
                    <br><br><br><br>Select the SDoH
                </p>""", unsafe_allow_html=True)
    
    sdoh_selection = st.selectbox(key="current_sdoh",
                                  label="**Select the SDOH**", 
                                  label_visibility="collapsed",
                                  options=sdoh_options, 
                                  index=0, 
                                  format_func=lambda x: dict_sdohLabels[x])
                                  # format_func=lambda x: str(sdoh_options.index(x)+1) + ". " + dict_sdohLabels[x])
    
    st.markdown(body="")
    sdoh_description = st.markdown(body=dict_sdohDescriptions[sdoh_selection],
                                   help=dict_sdohLabels[sdoh_selection])



# Dictionary for ticks information
arange = np.arange(start=0.0, stop=1.01, step=0.0588)
sdoh_describe = sdoh[sdoh_selection].describe(percentiles=arange)
sdoh_describe.pop("50%")
percentiles_vals = sdoh_describe[7:-1].values

sdoh_ticktexts=(np.rint(percentiles_vals)).astype(int)


### Puerto Rico Choropleth Map containing Counties with SDOH Data ###
mapp = px.choropleth(data_frame=sdoh,                                        # dataframe to use
                     geojson=counties,                                       # establishes coordinates of Puerto Rico to trace its map
                     locations="COUNTYFIPS",                                 # determines considered locations, used for plot traces and updates
                     labels=dict_Labels,                                     # labels for labs and sdohs
                     hover_name="COUNTY",                                    # counties names
                     # hover_data={sdoh_selection:True, "COUNTYFIPS":False}, # info contained in counties
                     hover_data={lab_selection:":.1f", sdoh_selection:":.0f",
                                 "COUNTYFIPS":False},
                     # color=dict_sdohColors[sdoh_selection],                # counties color intensities
                     # color_continuous_scale=pc.sequential.Purples,         # color scale for color intensities
                     # range_color=[0.35, 1],                                # min and max color intensities for counties
                     )      
                     
# Geographical Map Design
mapp.update_geos(scope="world",                         # sets section of world map
                 fitbounds=False,                       # removes mapping of locations with geojson coordinates, same as <fitbounds> in px.choropleth(...)
                 visible=False,                         # removes all other countries and continents, same as <basemap_visible> in px.choropleth(...)
                 center=dict(lat=18.155, lon=-66.245),  # sets center coordinates of the figure's map projection
                 bgcolor="#f5f5f5",                     # background color name: "whitesmoke"
                 projection_scale=172,                  # sets the map's initial zoom and projection type
                 # showframe=True,                       # shows the border lines of the map's plot box
                 )

# Map's Figure Layout
mapp.update_layout(autosize=False,                                      # allows custom size
                   margin=dict(autoexpand=True, r=0, t=0, l=0, b=0),    # figure's boundaries, distance from the plot's borders to the container's borders
                   
                   # width=1425,                                          # map horizontal size/length, same as <width> in px.choropleth(...)
                   # height=712.5,                                          # map vertical size/length, same as <height> in px.choropleth(...)
                   # width=1375,
                   # height=687.5,
                   # width=1100,
                   height=650,
                                      
                   paper_bgcolor="#f5f5f5",                             # application background color
                   # paper_bgcolor="indigo",
                   
                   dragmode=False,                                      # disables dragging of the map figure
                   modebar=dict(color="#303030", 
                                activecolor="#d303fc", 
                                bgcolor="#f5f5f5",
                                remove=["zoomIn", "zoomOut", "select",  # disables modebar's options 
                                        "lasso", "pan", "reset"]),
                   
                   # title=dict(                       # Main Title Design
                   #     automargin=True,              
                   #     pad=dict(t=0, l=0, b=0, r=0),  
                   #     x=0.50,                        
                   #     y=0.90, 
                   #     xref="paper", 
                   #     yref="paper", 
                   #     xanchor="center",
                   #     yanchor="top",
                   #     text="Puerto Rico<br>", 
                   #     "SDOHs-Kidney Disease",       
                   #     font=dict(color="purple", family="Rockwell", size=16)), 
                   
                   
                   showlegend=False,
                   # legend=dict(                       # Legend Design 
                   #    x=0.60, 
                   #    y=-0.175,
                   
                   #    bgcolor="#f5f5f5",              # legend background color
                   #    bordercolor="black",            # legend border lines color
                   #    borderwidth=0.75,               # legend border lines thickness 
                   #    
                   #    entrywidth=1,                   # space between symbols and labels
                   #    entrywidthmode="pixels",        # determines unit of measurement
                   #    itemwidth=30,                   # size of symbols inside the legend
                   #    traceorder="reversed",
                   #    
                   #    title=dict(side="top",                                  # legend's title text properties
                   #               text="Legend",                   
                   #               font=dict(color="black", family="Rockwell", size=14)))
                   #    font=dict(color="black", family="Rockwell", size=13),   # legend's labels text properties
                   )

# Map's Traces Properties
mapp.update_traces(visible=True,
                   name=dict_sdohLabels[sdoh_selection],                # new name of symbol
                   # z=sdoh["color_"+sdoh_selection],
                   z=[14315734] * 78,
                   # z=sdoh[dict_sdohColors[sdoh_selection]],
                   # z=sdoh[sdoh_selection],
                   # zauto=False,                                       # allows custom inferior/superior limits & midpoint
                   # zmin=sdoh[sdoh_selection].min(),
                   # zmax=sdoh[sdoh_selection].max(),     
                   
                   marker=dict(line=dict(color="#303030", width=1.5), opacity=0.925),
                   
                   showscale=True,
                   autocolorscale=False,
                   colorscale=pc.sequential.Purples,
                   reversescale=False,

                   
                   showlegend=False,                     # allows to be shown in the legend
                   legendrank=1,                         # first symbol in the legend
                   legendwidth=10,                       # width of legend box
                   
                   colorbar=dict(
                       orientation="h",                  # sets the colorscale bar to be drawn horizontaly
                       outlinecolor="black",             # sets the color of the bar's borders
                       outlinewidth=1.05,                # sets thickness of the borders' lines
                       
                       x=0.72,
                       y=0.025,                    
                       
                       thickness=13,                     # thickness size of the bar
                       len=0.40,                         # length of the bar                       
                       
                       title=dict(
                           side="bottom",
                           text=dict_sdohLabels[sdoh_selection],
                           font=dict(color="#303030", family="Rockwell", size=11)),   
                       
                       tickmode="array",
                       tickvals=sdoh_tickvals,
                       ticktext=sdoh_ticktexts,
                       # tickformat=".0f",
                       # ticksuffix="%",
                       ticks="inside",
                       tickwidth=1.35,
                       ticklen=3.5,
                       tickcolor="black",
                       tickfont=dict(color="#303030", family="Rockwell", size=10))
                  )




# Puerto Rico Scattergeo Map containing County Coordinate with Lab Data
# Counties without lab data: Añasco, Florida, Hormigueros, Las Marías, and Orocovis
dots = px.scatter_geo(data_frame=sdoh,
                      lat="lat",
                      lon="lon",
                      fitbounds="locations",
                      labels=dict_Labels,                                          # labels for labs and sdohs
                      hover_name="COUNTY",                                         # title of the dots' hoverboxes
                      hover_data={lab_selection:":.1f", sdoh_selection:":.0f",     # information contained inside dots
                                  "lat":False, "lon":False}
                      # color="creatinine_serum",                                  # dots color intensities
                      # color_continuous_scale=pc.sequential.Oranges,              # color scale for color intensities
                      # range_color=[0.30, 1.0],                                   # min and max color intensities for dots 
                      # opacity=0.75,                                              # transparency level for dots 
                      )

# Dot's Figure Layout
dots.update_layout(margin=dict(r=0, t=0, l=0, b=0),
                   autosize=False,                   # allows custom size                   
                   showlegend=False)                        

# Map's Traces Properties 
dots.update_traces(showlegend=False,                                      # allows to be shown in the legend
                   legendrank=2,                                          # second symbol in the legend
                   name=dict_labLabels[lab_selection],                    # sets the trace name in the legend and on datum hover 
                   
                   hoverlabel=dict(align="left",                          # sets text to be aligned to the left
                                   # bgcolor="darkorange",                # hoverbox background color
                                   bordercolor="black"),                  # hoverbox edges color
                   
                   # selected_marker=dict(opacity=1, size=10),
                   marker=dict(
                       # symbol="star-triangle-down",                       # shape type of marker
                       # symbol="star-triangle-down",
                       symbol = "diamond-tall",
                       
                       size=9,                                            # size of dots, same as <size> in px.scatter_geo(...)
                       line=dict(width=1.25, color="#303030"),            # dots borders line thickness & color

                       color=sdoh["color_"+lab_selection],                # determines color intensities
                       # color=sdoh[dict_labColors[lab_selection]],
                       opacity=0.90,
                       cauto=False,                                       # allows custom inferior/superior limits & midpoint
                       cmin=sdoh[lab_selection].min(),
                       cmax=sdoh[lab_selection].max(),
                       
                       showscale=True,                                    # displays scale values-to-color-intensities
                       autocolorscale=False,                              # allows custom colorscale
                       colorscale="Oranges",                              # determines color scale for color intensities
                       reversescale=False,                                # reverses bright and dark values
                       
                       colorbar=dict(
                           orientation="h",                               # sets the colorscale bar to be drawn horizontaly
                           outlinecolor="black",                          # sets the color of the bar's borders
                           outlinewidth=1.05,                             # sets thickness of the borders' lines
                           
                           x=0.28,
                           y=0.025,                      
                           
                           thickness=13,                                   # thickness size of the bar
                           len=0.40,                                       # length of the bar
                           
                           title=dict(
                               side="bottom",
                               text=dict_labLabels[lab_selection],
                               font=dict(color="#303030", family="Rockwell", size=11)), 
                           
                           tickmode="linear",
                           tick0=0,
                           dtick=dict_labsDticks[lab_selection],
                           # tickformat=".1f",
                           ticks="inside",
                           tickwidth=1.30,
                           ticklen=4,
                           tickcolor="black",
                           tickfont=dict(color="#303030", family="Rockwell", size=10)))          
                   )



# Combines the Dots Traces of the Scattergeo Map with the Counties Traces of the Choropleth Map, 
# based on Puerto Rico's Coordinates.
mapp.append_trace(dots.data[0], row="all", col="all")


with col2:
    # Display the plot and all its traces
    st.plotly_chart(mapp,
                    use_container_width=True,
                    config={"displayModeBar":"hover",  # Sets the mode bar to appear only when the mouse is inside the plot
                            "displaylogo":False,       # Removes the Plotly-Dash logo from appearing in the mode bar options
                            "scrollZoom":False})
    
# if sdoh_selection:
#     st.toast(body="Current SDOH  %s" % dict_sdohLabels[sdoh_selection], icon="⚕️") 
# if lab_selection:
#     st.toast(body="Current Lab " + dict_labLabels[lab_selection], icon="🧪")


# Dividing line for the resources information
st.divider()
st.markdown(body="")


# Resources Information Paragraph
footbuff1, footnote, footbuff2 = st.columns([0.01, 0.98, 0.01])

# st.markdown("""<p style="text-align:center; background-color:white; font-size:12px; color:black">
#                 SDoHs were obtained from Agency for Healthcare Research and Quality (AHRQ) database (https://www.ahrq.gov/).<br><br>
#                 Kidney-related lab test results were obtained as part of the pilot project supported by the Office of the Director,<br>
#                 National Institutes of Health Common Fund under award number 1OT2OD032581-01<br>
#                 (Artificial Intelligence/Machine Learning Consortium to Advance Health Equity and Researcher Diversity (AIM-AHEAD)).<br><br> 
#                 It was also supported by the Center for Collaborative Research in Health Disparities (CCRHD),<br>
#                 RCMI grant U54 MD007600 (National Institute on Minority Health and Health Disparities) from the National Institutes of Health.<br><br> 
#                 The work is solely the authors' responsibility and does not necessarily represent the official view of the National Institutes of Health.
#             </p>""", unsafe_allow_html=True)



with footbuff1:
    st.caption("""<p style="text-align:left; font-size:14px">
               </p>""", unsafe_allow_html=True)

with footnote:
    st.caption("""<p style="text-align:justify; font-size:14px">
                   SDoHs were obtained from the Agency for Healthcare Research and Quality database
                   (<a href="https://www.ahrq.gov/sdoh/data-analytics/sdoh-data.html" target="_blank">AHRQ</a>).
                   Kidney-related laboratory test results were obtained as part of the pilot project supported by the Office of the Director,
                   National Institutes of Health Common Fund, under award number 1OT2OD032581-01
                   (Artificial Intelligence/Machine Learning Consortium to Advance Health Equity and Researcher Diversity
                   (<a href="https://www.aim-ahead.net/" target="_blank">AIM-AHEAD</a>)).
                   It was also supported by the Center for Collaborative Research in Health Disparities
                   (<a href="https://rcmi.rcm.upr.edu/" target="_blank">CCRHD</a>),
                   RCMI grant U54 MD007600 (National Institute on Minority Health and Health Disparities
                   (<a href="https://www.nimhd.nih.gov/" target="_blank">NIMHD</a>)) 
                   from the National Institutes of Health 
                   (<a href="https://www.nih.gov/" target="_blank">NIH</a>).
                   The work is solely the authors' responsibility and does not necessarily represent the official view of the NIH.
               </p>""", unsafe_allow_html=True)

with footbuff2:
    st.caption("""<p style="text-align:right; font-size:14px">
               </p>""", unsafe_allow_html=True)


# Removes "Made with Streamlit"
hide_style = """<style>
                 footer {visibility: hidden;}
             </style>"""

st.markdown(hide_style, unsafe_allow_html=True) 

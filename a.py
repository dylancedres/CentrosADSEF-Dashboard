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
# @st.cache_data
def load_data():
    adsef_path = "adsef.csv"
    # adsef_path = r"C:\Users\dcedr\Documents\dashboard_codes\adsef_centros\adsef.csv"
    return pd.read_csv(adsef_path, 
                       dtype={"Region Zipcode":str, "Fipcode":str, "Zipcode":str, "Expiracion de Licencia":str}, 
                       low_memory=False)

# @st.cache_data
def load_fipcodes():
    fips_path = "counties_fips.csv"
    # fips_path = r"C:\Users\dcedr\Documents\dashboard_codes\adsef_centros\counties_fips.csv"
    return pd.read_csv(fips_path,
                       dtype={"COUNTY":str, "COUNTYFIPS":str},
                       low_memory=False)     


########################################
# --DASHBOARD APPLICATION START LINE-- #
########################################

st.set_page_config(layout="wide",
                   page_title="Egidas PR - Centros Adultos Mayores",
                   page_icon=":house_buildings:",
                   menu_items={"Get help":"mailto:dylan.cedres@upr.edu",
                               "Report a Bug":"mailto:dylan.cedres@upr.edu",
                               "About":"Dashboard with Kidney Disease Lab Data and Social Determinants of Health Indices"})


counties = load_json()      # Puerto Rico's geograpical information for map traces
adsef = load_data()         # Senior Centers data
fipcodes = load_fipcodes()  # FIPS codes of Puerto Rico's counties


### Dashboard Main Title ###
logobuff1, logo1, title, logo2, logobuff2 = st.columns([0.05, 0.12, 0.66, 0.10, 0.09])


with logo1:
    st.markdown("""<a href="https://rcmi.rcm.upr.edu/" hreflang="en" target="_blank">
                      <img style="vertical-align:top; font-size:16px; color:black;"
                      src="https://raw.githubusercontent.com/dylancedres/CentrosADSEF-Dashboard/main/logo_ccr_rcmi_clear.png" 
                      alt="CCR RCMI Logo" width="156px" height="150px">
                </a>""", unsafe_allow_html=True)

with title:
    # Application's Main Title (CENTER)
    st.markdown("""<p style="text-align:center; font-weight:bold; font-size:36px">
                    <br>Centros de Adultos Mayores y Envejecientes en Puerto Rico</p>
                """, unsafe_allow_html=True)
    
with logo2:
    st.markdown("""<a href="https://serviciosenlinea.adsef.pr.gov/" hreflang="en" target="blank">
                    <img style="vertical-align:top; background-color:white; font-size:16px; color:black;"
                    src="https://raw.githubusercontent.com/dylancedres/CentrosADSEF-Dashboard/main/logo_adsef.png"
                    alt="ADSEF Logo" width="160px" height="120px">
                </a>""", unsafe_allow_html=True)


# Hide Images View Fullscreen
st.markdown("""<style>
                button[title="View fullscreen"]{
                visibility: hidden;}
            </style>""", unsafe_allow_html=True)



### Puerto Rico Choropleth Map containing Counties Data ###
mapp = px.choropleth(data_frame=fipcodes,                          # dataframe to use
                     geojson=counties,                             # establishes coordinates of Puerto Rico's county borders to trace its map
                     locations="COUNTYFIPS",                       # determines considered locations, used for plot traces and updates
                     hover_name="COUNTY",                          # counties names
                     hover_data={"Total de Centros":True,          # info contained in counties
                     "Total de Capacidad":True,
                     "COUNTYFIPS":False}
                     )      

    
# Geographical Map Design
mapp.update_geos(scope="world",                         # sets section of world map
                 fitbounds=False,                       # removes mapping of locations with geojson coordinates, same as <fitbounds> in px.choropleth(...)
                 visible=False,                         # removes all other countries and continents, same as <basemap_visible> in px.choropleth(...)
                 center=dict(lat=18.190, lon=-66.245),  # sets center coordinates of the figure's map projection
                 bgcolor="#0099bb",                     # map's ocean color
                 projection_scale=175,                  # sets the map's initial zoom and projection type
                 # showframe=True
                 )

# Map's Figure Layout
mapp.update_layout(autosize=False,                                      # allows custom size
                   margin=dict(autoexpand=True, r=0, t=0, l=0, b=0),    # figure's boundaries, distance from the plot's borders to the container's borders
                   # width=1425,                                        # map horizontal size/length, same as <width> in px.choropleth(...)
                   height=520,                                          # map vertical size/length, same as <height> in px.choropleth(...)
                   paper_bgcolor="#0099bb",                             # application background color
                   showlegend=False,                                    # disables legend from appearing    
                   dragmode=False,                                      # disables dragging of the map figure
                   modebar=dict(color="#303030", 
                                activecolor="#d303fc",                                            # modebar's primary color
                                bgcolor="#0099bb",                                                # modebar's background color
                                remove=["zoomIn", "zoomOut", "select", "lasso", "pan", "reset"]), # disables modebar's options
                   # transition=dict(duration=100, ordering="traces first")
                   )

# Map's Traces Properties
mapp.update_traces(visible=True,
                   zauto=False,                                                        # allows custom inferior/superior limits & midpoint
                   autocolorscale=False,
                   colorscale=pc.sequential.Purples,
                   reversescale=False,

                   marker=dict(line=dict(color="#303030", width=1.5), opacity=0.925),  # border traces' color and thickness level

                   hoverlabel=dict(align="left",                                       # sets text to be aligned to the left
                                   bgcolor="#66029c",                                  # hoverbox background color
                                   bordercolor="black",
                                   font=dict(family="Calibri", size=15))
                   )


# Puerto Rico Scattergeo Map containing County Coordinate with Lab Data
# Counties without centers data:
dots = px.scatter_geo(data_frame=fipcodes,
                      lat="lat",
                      lon="lon",
                      fitbounds="locations",
                      hover_name="COUNTY",                     # title of the dots' hoverboxes
                      hover_data={"Total de Centros":True,     # information contained inside dots
                                  "Total de Capacidad":True,
                                  "lat":False, "lon":False}
                      )

# Dot's Figure Layout
dots.update_layout(margin=dict(r=0, t=0, l=0, b=0),
                   autosize=False,                             # allows custom size                   
                   showlegend=False)                        

# Map's Traces Properties 
dots.update_traces(marker=dict(symbol="hexagram-dot",                     # shape type of marker
                               size=10,                                   # size of dots, same as <size> in px.scatter_geo(...)
                               line=dict(width=1.25, color="#303030"),    # dots borders line thickness & color
                               cauto=False,                               # allows custom inferior/superior limits & midpoint
                               color="#dd7722",                           # determines color intensities
                               autocolorscale=False),                     # allows custom colorscale
                   
                   hoverlabel=dict(align="left",                          # sets text to be aligned to the left
                                   bgcolor="#66029c",                     # hoverbox background color
                                   bordercolor="black",                   # hoverbox edges color
                                   font=dict(family="Calibri", size=15))
                  )



# Combines the Dots Traces of the Scattergeo Map with the Counties Traces of the Choropleth Map, 
# based on Puerto Rico's Coordinates.
mapp.append_trace(dots.data[0], row="all", col="all")


### Column containers for PR Map and tabs with Centers Lists ###
colbuff1, col, colbuff2 = st.columns([0.055, 0.89, 0.055], gap="small")

with col:
    # Display the plot and all its traces
    st.plotly_chart(mapp,
                    use_container_width=True,
                    config={"displayModeBar":"hover",  # Sets the mode bar to appear only when the mouse is inside the plot
                            "displaylogo":False,       # Removes the Plotly-Dash logo from appearing in the mode bar options
                            "scrollZoom":False})


# List of Centers for each county
tabsbuff, tabs_long_list, tabshelp = st.columns([0.05, 0.87, 0.08])



with tabs_long_list:

    tabs_names = list(fipcodes["COUNTY"].values)
    tabs = st.tabs(tabs_names)
    
    for tab, current_county in zip(tabs, fipcodes["COUNTY"].values):
        
        i = 1
        df_county = adsef[adsef["Municipio"]==current_county]
        df_county_overview = fipcodes[fipcodes["COUNTY"]==current_county]        

        
        with tab:
            center_total = df_county_overview["Total de Centros"].values
            center_total = str(center_total[0])
            st.caption("Total de Centros:  %s" % center_total)
            
            st.subheader(body="Lista de Centros de %s" % current_county,
                         # anchor="Centros_De_%s" % current_county,
                         divider="orange")
            
            
            for center_name, center_subtype, center_cap, center_adr, center_reg, center_contact, center_tel in zip(df_county["Nombre"], df_county["Subtipo"], df_county["Capacidad"], df_county["Direccion Fisica"], df_county["Region"], df_county["Contacto"], df_county["Telefono"]):
                
                i_label = ("%s - %s :bed:%s") % (str(i), center_name, center_cap)
                i += 1
                
                with st.expander(i_label):
                
                    with st.container(border=True):

                        if len(center_name) > 55 or len(center_adr) > 55 or len(center_contact) > 11:
                            st.metric(label=":house_with_garden: Nombre", 
                                        value=center_name, 
                                        delta=center_subtype, 
                                        delta_color="off", 
                                        label_visibility="visible")
                            
                            st.metric(label=":bed: Capacidad", 
                                        value=center_cap, 
                                        delta="Camas", 
                                        delta_color="off", 
                                        label_visibility="visible")
                            
                            st.metric(label=":round_pushpin: Direccion",
                                        value=center_adr,
                                        delta="Region: %s" % center_reg,
                                        delta_color="off",
                                        label_visibility="visible")
                            
                            st.metric(label=":phone: Info de Contacto", 
                                        value=center_contact, 
                                        delta=center_tel, 
                                        delta_color="off", 
                                        label_visibility="visible")
                            continue
                            
                        met1, met2 = st.columns([4, 1])
                        met3, met4 = st.columns([4, 1])
                        
                        met1.metric(label=":house_with_garden: Nombre", 
                                    value=center_name, 
                                    delta=center_subtype, 
                                    delta_color="off", 
                                    label_visibility="visible")
                        
                        met2.metric(label=":bed: Capacidad", 
                                    value=center_cap, 
                                    delta="Camas", 
                                    delta_color="off", 
                                    label_visibility="visible")
                        
                        met3.metric(label=":round_pushpin: Direccion",
                                    value=center_adr,
                                    delta="Region: %s" % center_reg,
                                    delta_color="off",
                                    label_visibility="visible")
                        
                        met4.metric(label=":phone: Info de Contacto", 
                                    value=center_contact, 
                                    delta=center_tel, 
                                    delta_color="off", 
                                    label_visibility="visible")
                        

with tabshelp:
    st.caption(body="", help="Haz click o presiona :arrow_left::arrow_right: para seleccionar un municipio")
    



# Dividing line for the resources information
# st.divider()
# st.markdown(body="")


# Resources Information Paragraph
# footbuff1, footnote, footbuff2 = st.columns([0.01, 0.98, 0.01])

# with footbuff1:
#     st.caption("""<p style="text-align:left; font-size:14px">
#                </p>""", unsafe_allow_html=True)

# with footnote:
#     st.caption("""<p style="text-align:justify; font-size:14px">
#                    SDoHs were obtained from the Agency for Healthcare Research and Quality database
#                    (<a href="https://www.ahrq.gov/sdoh/data-analytics/sdoh-data.html" target="_blank">AHRQ</a>).
#                    Kidney-related laboratory test results were obtained as part of the pilot project supported by the Office of the Director,
#                    National Institutes of Health Common Fund, under award number 1OT2OD032581-01
#                    (Artificial Intelligence/Machine Learning Consortium to Advance Health Equity and Researcher Diversity
#                    (<a href="https://www.aim-ahead.net/" target="_blank">AIM-AHEAD</a>)).
#                    It was also supported by the Center for Collaborative Research in Health Disparities
#                    (<a href="https://rcmi.rcm.upr.edu/" target="_blank">CCRHD</a>),
#                    RCMI grant U54 MD007600 (National Institute on Minority Health and Health Disparities
#                    (<a href="https://www.nimhd.nih.gov/" target="_blank">NIMHD</a>)) 
#                    from the National Institutes of Health 
#                    (<a href="https://www.nih.gov/" target="_blank">NIH</a>).
#                    The work is solely the authors' responsibility and does not necessarily represent the official view of the NIH.
#                </p>""", unsafe_allow_html=True)

# with footbuff2:
#     st.caption("""<p style="text-align:right; font-size:14px">
#                </p>""", unsafe_allow_html=True)


# Removes "Made with Streamlit"
hide_style = """<style>
                 footer {visibility: hidden;}
             </style>"""
st.markdown(hide_style, unsafe_allow_html=True)





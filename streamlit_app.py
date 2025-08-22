import streamlit as st
import pandas as pd
import altair as alt
import re

st.title("JCPAO Criminal Cases Received by Police Agency")

# Import DataFrame
df = pd.read_csv("Received Cases (1) by Agency.csv", encoding="utf-8")

# Melt the DataFrame to long format
long_df = df.melt(id_vars='ref_month_yr', 
                    var_name='Agency', 
                    value_name='Cases')

# Add JCPAO Location
long_df['JCPAO Location'] = ['Downtown' if agency in ['KCPD', 'Grandview PD'] else 'Eastern Jack' for agency in long_df['Agency']]

# long_df['ref_month_yr'] = pd.to_datetime(long_df['ref_month_yr']) # .dt.strftime("%Y-%m")

# --- st.sidebar ---
with st.sidebar:
    st.title("Please explore the data using the filters below.")

    # Filter by agency
    # st.write("Filter by PD Agency")
    all_agencies = long_df['Agency'].unique().tolist()
    selected_agencies = st.multiselect(
        "Select PD Agency",
        options=all_agencies,
        default=all_agencies
    )

    # Filtering by Time Period
    month_yrs = sorted(long_df['ref_month_yr'].unique().tolist())
    all_years = [year.split("-")[0] for year in month_yrs]
    all_years = list(set(all_years))
    all_months = ["-"+month.split("-")[-1] for month in month_yrs]
    all_months = list(set(all_months))

    # Filter by Year 
    # st.write("Filter by Year")
    selected_years = st.multiselect(
        "Select Year",
        options=all_years,
        default=all_years
    )
    years_pattern = "|".join(map(re.escape, selected_years))

    # Filter by Month
    # st.write("Filter by Month")
    selected_months = st.multiselect(
        "Select Month",
        options=all_months,
        default=all_months
    )
    months_pattern = "|".join(map(re.escape, selected_months))

    # Filtered DataFrame
    filtered_df = long_df[
        (long_df['Agency'].isin(selected_agencies)) &
        (long_df['ref_month_yr'].str.contains(years_pattern)) & 
        (long_df['ref_month_yr'].str.contains(months_pattern))
    ].copy()
    filtered_df['ref_month_yr'] = pd.to_datetime(filtered_df['ref_month_yr']) # .dt.strftime("%Y-%m")

    # JCPAO Location DataFrame
    location_df = long_df[
        (long_df['ref_month_yr'].str.contains(years_pattern)) & 
        (long_df['ref_month_yr'].str.contains(months_pattern))
    ].copy()
    location_df['ref_month_yr'] = pd.to_datetime(location_df['ref_month_yr']) # .dt.strftime("%Y-%m")

    # Caption
    st.caption("Data as of Friday, August 22, 2025.")

# --- st.expanders --- 
# with st.expander("Bar Chart"):
#     st.bar_chart(data=filtered_df, x="ref_month_yr", y='Agency')

with st.expander("Bar Chart - Received Criminal Cases by Police Agency"):
    # Build Altair grouped bar chart
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X('ref_month_yr:T', title='Month-Year'), # sort="-y" 
        xOffset=alt.XOffset('Agency:N'),
        y=alt.Y('Cases:Q', title='Cases Received'),
        color='Agency:N',
        tooltip=['ref_month_yr', 'Agency', 'Cases']
    ).properties(
        title='📊 Monthly Cases Received by Agency',
        width=700,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

with st.expander("Bar Chart - Received Criminal Cases by JCPAO Location"):
    # Build Altair grouped bar chart
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X('ref_month_yr:T', title='Month-Year'), # sort="-y" 
        xOffset=alt.XOffset('JCPAO Location:N'),
        y=alt.Y('Cases:Q', title='Cases Received'),
        color='JCPAO Location:N',
        tooltip=['ref_month_yr', 'JCPAO Location', 'Cases']
    ).properties(
        title='📊 Monthly Cases Received by JCPAO Location (Downtown vs. East Jack)',
        width=700,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

with st.expander("Raw Data"):
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

with st.expander("About the app"):
    st.write(
        '''
        Streamlit app created by Joseph Cho, ujcho@jacksongov.org.
        The data only displays criminal cases received by the JCPAO from the 16 local law enforcement agencies (including the Jackson County Sheriff and the Drug Task Force) within Jackson County, MO.
        - KCPD
        - Independence PD
        - Blue Springs PD
        - Lees Summit PD
        - Raytown PD
        - Grandview PD
        - Sugar Creek PD
        - Grain Valley PD
        - Oak Grove PD
        - Buckner PD
        - Lone Jack PD
        - Greenwood PD 
        - Lake Lotawana PD
        - Lake Tapawingo PD
        - Jackson County Sheriff
        - Jackson County Drug Task Force (JCDTF)
        '''
    )


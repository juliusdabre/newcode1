
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("RADAR March 2025.xlsx", sheet_name='Sheet1')
    return df

df = load_data()

st.title("PropRadar")

# Sidebar filters
st.sidebar.header("Filter Options")

selected_sa4 = st.sidebar.multiselect('Select SA4 Region', options=df['Sa4'].unique(), default=df['Sa4'].unique())
growth_gap = st.sidebar.slider('Growth Gap', min_value=int(df['Growth Gap'].min()), max_value=int(df['Growth Gap'].max()), value=(int(df['Growth Gap'].min()), int(df['Growth Gap'].max())))
yield_filter = st.sidebar.slider('Yield (%)', min_value=float(df['YIELD'].min()), max_value=float(df['YIELD'].max()), value=(float(df['YIELD'].min()), float(df['YIELD'].max())))
price_change_12m = st.sidebar.slider('12 Month Price Change', min_value=float(df['Sale Median 12M Change'].min()), max_value=float(df['Sale Median 12M Change'].max()), value=(float(df['Sale Median 12M Change'].min()), float(df['Sale Median 12M Change'].max())))
rent_change_12m = st.sidebar.slider('12 Month Rent Change', min_value=float(df['RENT CHANGE'].min()), max_value=float(df['RENT CHANGE'].max()), value=(float(df['RENT CHANGE'].min()), float(df['RENT CHANGE'].max())))
sales_turnover = st.sidebar.slider('Sales Turnover', min_value=int(df['Sales Turnover'].min()), max_value=int(df['Sales Turnover'].max()), value=(int(df['Sales Turnover'].min()), int(df['Sales Turnover'].max())))
rent_turnover = st.sidebar.slider('Rent Turnover', min_value=int(df['Rent Turnover'].min()), max_value=int(df['Rent Turnover'].max()), value=(int(df['Rent Turnover'].min()), int(df['Rent Turnover'].max())))
buy_afford = st.sidebar.slider('Buying Affordability', min_value=int(df['Buy Affordability'].min()), max_value=int(df['Buy Affordability'].max()), value=(int(df['Buy Affordability'].min()), int(df['Buy Affordability'].max())))
rent_afford = st.sidebar.slider('Rent Affordability', min_value=float(df['Rent Afford'].min()), max_value=float(df['Rent Afford'].max()), value=(float(df['Rent Afford'].min()), float(df['Rent Afford'].max())))

filtered_df = df[(df['Sa4'].isin(selected_sa4)) &
                 (df['Growth Gap'].between(growth_gap[0], growth_gap[1])) &
                 (df['YIELD'].between(yield_filter[0], yield_filter[1])) &
                 (df['Sale Median 12M Change'].between(price_change_12m[0], price_change_12m[1])) &
                 (df['RENT CHANGE'].between(rent_change_12m[0], rent_change_12m[1])) &
                 (df['Sales Turnover'].between(sales_turnover[0], sales_turnover[1])) &
                 (df['Rent Turnover'].between(rent_turnover[0], rent_turnover[1])) &
                 (df['Buy Affordability'].between(buy_afford[0], buy_afford[1])) &
                 (df['Rent Afford'].between(rent_afford[0], rent_afford[1]))]

st.write("### Filtered Data")
st.dataframe(filtered_df)

# Radar Chart for selected SA3
st.write("### SA3 Radar Comparison")
selected_sa3 = st.multiselect("Select SA3 Regions for Comparison", filtered_df['SA3'].unique(), default=filtered_df['SA3'].unique()[:3])
radar_df = filtered_df[filtered_df['SA3'].isin(selected_sa3)]
radar_df = radar_df[['SA3', 'Growth Gap', '12M Price Change', 'Sales Turnover', 'Buy Affordability', 'Rent Turnover']]

categories = radar_df.columns[1:]
fig = go.Figure()
for i in range(len(radar_df)):
    fig.add_trace(go.Scatterpolar(
        r=radar_df.iloc[i, 1:].values,
        theta=categories,
        fill='toself',
        name=radar_df.iloc[i, 0]
    ))

fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
st.plotly_chart(fig)

# Visualization - Median Price
st.write("### Median Price Comparison")
fig2 = px.bar(filtered_df, x='SA3', y='Median', color='Sa4', title='Median Price by SA3')
st.plotly_chart(fig2)

# Visualization - 12 Month Price Change
st.write("### 12 Month Price Change")
fig3 = px.line(filtered_df, x='SA3', y='Sale Median 12M Change', markers=True, title='12 Month Median Price Change')
st.plotly_chart(fig3)

# Download data
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Data as CSV", csv, "filtered_property_data.csv", "text/csv")

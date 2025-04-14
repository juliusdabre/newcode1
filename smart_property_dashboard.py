
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

st.title("🏘️ Smart Property Investment Dashboard")

# Sidebar filters
st.sidebar.header("Filter Options")

selected_sa4 = st.sidebar.multiselect('Select SA4 Region', options=df['Sa4'].unique(), default=df['Sa4'].unique())
selected_growth_gap = st.sidebar.slider('Growth Gap', min_value=int(df['Growth Gap'].min()), max_value=int(df['Growth Gap'].max()), value=(int(df['Growth Gap'].min()), int(df['Growth Gap'].max())))
selected_yield = st.sidebar.slider('Yield (%)', min_value=float(df['YIELD'].min()), max_value=float(df['YIELD'].max()), value=(float(df['YIELD'].min()), float(df['YIELD'].max())))

filtered_df = df[(df['Sa4'].isin(selected_sa4)) &
                 (df['Growth Gap'] >= selected_growth_gap[0]) & (df['Growth Gap'] <= selected_growth_gap[1]) &
                 (df['YIELD'] >= selected_yield[0]) & (df['YIELD'] <= selected_yield[1])]

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

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True
)

st.plotly_chart(fig)

# Bar Graph - Median Price comparison
st.write("### Median Price Comparison")
fig2 = px.bar(filtered_df, x='SA3', y='Median', color='Sa4', title='Median Price by SA3')
st.plotly_chart(fig2)

# Line Graph - 12M Price Change
st.write("### 12 Month Price Change")
fig3 = px.line(filtered_df, x='SA3', y='Sale Median 12M Change', markers=True, title='12 Month Median Price Change')
st.plotly_chart(fig3)

# Allow user to download filtered data
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download Data as CSV", data=csv, file_name='filtered_property_data.csv', mime='text/csv')

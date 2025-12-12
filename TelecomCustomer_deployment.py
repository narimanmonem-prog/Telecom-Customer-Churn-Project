
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout= 'wide', page_title= 'Telecom Customers Churn')

html_title = """<h1 style="color:white;text-align:center;"> Telecom Customer Churn Data Analysis Project </h1>"""
st.markdown(html_title, unsafe_allow_html=True)
st.image('Home.png')
df = pd.read_csv('cleaned_df.csv', index_col= 0)
page = st.sidebar.radio('Pages', ['Home', "Analysis Report"])
if page == 'Home':
    st.subheader('📖 Project Introduction')
    st.write('Customer churn is one of the most critical challenges faced by telecom providers. Losing customers not only reduces revenue but also increases acquisition costs, as attracting new subscribers is often more expensive than retaining existing ones. The goal of this project is to predict which customers are most likely to leave and to understand the factors driving their decisions.')
    st.write('This project is about turning raw telecom customer data into actionable insights that help companies predict churn, understand customer behavior, and design effective retention strategies')
    st.subheader('Data Columns Description')
    st.image('Descreption.jpg')
    st.subheader('Dataset Overview')
    st.dataframe(df)
    st.subheader('Data Summary')
    Total_customers =len(df)
    Cities_On_Service = df['City'].nunique()
    Total_Revenue = df['Total Revenue'].sum().round(0)
    Total_Charges=df['Total Charges'].sum().round(0)
    col1, col2 = st.columns(2)
    col1.metric("🤵 Total Customers", f"{Total_customers:,}")
    col2.metric("💰 Total Revenue", f"${Total_Revenue:}")
    col3, col4 = st.columns(2)
    col3.metric("🏰 Cities On Service", f"{Cities_On_Service:,}")
    col4.metric("💰 Total Charges", f"${Total_Charges:}")
    st.write("---")
    df_filtered = df.copy()
    Customer_Status = st.sidebar.selectbox('Customer_Status',['All','Stayed', 'Churned','Joined'])
    Internet_service = st.sidebar.selectbox('Internet_service',['All','Yes','No'])
    Phone_service = st.sidebar.selectbox('Phone_service',['All','Yes','No'])
    if Customer_Status != 'All':
        df_filtered=df[df['Customer Status']==Customer_Status]
    if Internet_service!= 'All':
         df_filtered=df[df['Internet Service']==Internet_service]
    if Phone_service!= 'All':
        df_filtered=df[df['Phone Service']==Phone_service]
    st.subheader('Data Filtered')
    st.dataframe(df_filtered)
elif page =='Analysis Report':
    st.subheader('Customer Status Distribution')
    st.plotly_chart(px.pie(data_frame= df, names= 'Customer Status',title='customer status distribution'))
    st.subheader('Customer Status per gender')
    st.plotly_chart(px.histogram(df, x="Gender", color="Customer Status", barmode="group",text_auto=True, title="Customer status per gender"))
    st.subheader('Customer Status per contract Type')
    st.plotly_chart(px.histogram(df, x="Contract", color="Customer Status", barmode="group", title="Churn by Contract Type",text_auto=True))
    st.subheader('Revenue per customer status')
    st.plotly_chart(px.box(data_frame=df,x='Total Revenue',color="Customer Status"))
    st.subheader('Charges per customer status')
    st.plotly_chart(px.box(data_frame=df,x='Total Charges',color="Customer Status"))
    df['Churn_Flag'] = df['Customer Status'].apply(lambda x: 1 if x == "Churned" else 0)
    city_churn_rate = df.groupby("City")['Churn_Flag'].sum().reset_index()
    city_churn_sorted = city_churn_rate.sort_values(by="Churn_Flag", ascending=False)
    top5 = city_churn_sorted.head(5)
    bottom5 = city_churn_sorted.tail(5)
    st.subheader('Top 5 cities by customer churn')
    st.plotly_chart(px.bar(top5, x="City", y="Churn_Flag", color="Churn_Flag", title="Top 5 Cities by Churn Rate",text_auto=True))
    st.subheader('Customer Segmentation')
    st.plotly_chart(px.histogram(data_frame= df, x= 'customer_loyalty',text_auto=True,color='Customer Status',barmode='group').update_xaxes(categoryorder = 'max descending'))
    st.subheader('Service Category')
    st.plotly_chart(px.histogram(data_frame= df, x= 'ServiceCategory',text_auto=True,color='Customer Status',barmode='group').update_xaxes(categoryorder = 'max descending'))
    st.subheader('Charges Level')
    st.plotly_chart(px.histogram(data_frame= df, x= 'charges Level',text_auto=True,color='Customer Status',barmode='group').update_xaxes(categoryorder = 'max descending'))
    corr_df= df.corr(numeric_only=True).round(2)
    st.subheader('Correlation')
    st.plotly_chart(px.imshow(corr_df,text_auto=True,width=1000,height=1000,title='Correlation Heatmap'))

    

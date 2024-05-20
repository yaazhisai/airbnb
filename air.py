# airbnb
Airbnb Analysis using streamlit and Tableau
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pprint import pprint
import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as pt
import plotly.figure_factory as ff
import pydeck as pdk  # For map visualization


def m():
    uri = "mongodb+srv://..."

        # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

        # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        db=client.yy
        record=db.yy_airbnb
        count=record.count_documents({})
        if count!=0:    
            df_air1 = pd.DataFrame(list(record.find({})))

    except Exception as e:
        print(e) 

    finally:
        client.close()
    

def clean_airbnb(df):
    if 'clean' not in st.session_state.keys():
        df.dropna(how='all',inplace=True)
        
        convert_type={'listing_id':'int','minimum_nights':'int','maximum_nights':'int'}
        df.rename(columns={'_id':'listing_id','name':'listing_name'},inplace=True)
        df.astype(convert_type)
        df.drop(columns=['weekly_price','monthly_price','reviews_per_month'],inplace=True)
        df.drop(columns=['listing_url','neighborhood_overview','cancellation_policy','summary','space','notes','description','images','first_review','last_scraped'],inplace=True)
        df.drop(columns=['calendar_last_scraped'],inplace=True)
        df.reset_index(drop=True,inplace=True)
        #df['first_review']=pd.to_datetime(df['first_review'],format='%Y-%m-%d %H:%M:%S')
        df['last_review']=pd.to_datetime(df['last_review'],format='%Y-%m-%d %H:%M:%S')
        df['last_review_year']= pd.to_datetime(df['last_review']).dt.strftime('%Y')
        #df['last_scraped']=pd.to_datetime(df['last_scraped'],format='%Y-%m-%d %H:%M:%S')
        df['cleaning_fee']=df['cleaning_fee'].fillna(0.0)
        df['security_deposit']=df['security_deposit'].fillna(0.0)
        df['bedrooms']=df['bedrooms'].bfill()
        df['beds']=df['beds'].ffill()
        df['bathrooms']=df['bathrooms'].bfill()

        for i in range(0,len(df['address'])):
            df.loc[i,'country']=df.loc[i,'address']['country']
            df.loc[i,'country_code']=df.loc[i,'address']['country_code']
            df.loc[i,'latitude']=df.loc[i,'address']['location']['coordinates'][0]
            df.loc[i,'longitude']=df.loc[i,'address']['location']['coordinates'][1]
            df.loc[i,'city']=df.loc[i,'address']['market']
            df.loc[i,'suburbs']=df.loc[i,'address']['suburb']
            df.fillna({'suburbs':'NOT AVAILABLE'},inplace=True)
        
        for i in range(0,len(df['host'])):
            df.loc[i,'host_verified']=df.loc[i,'host']['host_identity_verified']
            df.loc[i,'hostname']=df.loc[i,'host']['host_name']
            df.loc[i,'host_id']=df.loc[i,'host']['host_id']
            df.loc[i,'host_listing_count']=df.loc[i,'host']['host_total_listings_count']
        for i in range(len(df['availability'])):
            df.loc[i,'availability_30']=df.loc[i,'availability']['availability_30']
            df.loc[i,'availability_365']=df.loc[i,'availability']['availability_365']
        for i in range(len(df)):
            df.loc[i,'no_of_amenities'] = len(df.loc[i,'amenities'])
        for i in range(0,len(df['review_scores'])):
            if 'review_scores_rating' in df['review_scores'][i].keys():
                df.loc[i,'rating']=df['review_scores'][i]['review_scores_rating']
        df['rating']=df['rating'].replace(to_replace=np.nan,value=50).astype('int64')
        df['availability_365'].astype('int64')
        df['host_id'].astype('int')
        df.drop(columns=['address','availability','reviews','host','house_rules','interaction','review_scores','transit','access'],inplace=True)
        st.session_state['clean']='Y'
        return df

if 'clean' not in st.session_state.keys():
    df_air = pd.read_json('sample_airbnb (1).json')
    st.session_state['df_map'] = clean_airbnb(df_air)

##streamlit###

st.title("AIRBNB DATA ANALYSIS")
tab1, tab2, tab3, tab4= st.tabs([":clipboard: AIRBNB INTRO",":clipboard: EDA",":chart: DYNAMIC CHARTS",":world_map: GEO MAP"])
with tab1:
    st.header("ABOUT AIRBNB")
    st.image('C:/Users/yaazhisai/Desktop/airbnb/Airbnb-Logo.jpg')
    st.write("Airbnb has provided many travellers a great, easy and convenient place to stay during their travels.\
    Similarly, it has also given an opportunity for many to earn extra revenue by listing their properties for residents to stay.\
    However, with so many listings available with varying prices, how can an aspiring host know what type of property to invest in if his main aim is to list \
    it in Airbnb and earn rental revenue? Additionally, if a traveller wants to find the cheapest listing available but with certain features he prefers like 'free parking' \
    etc, how does he know what aspects to look into to find a suitable listing? There are many factors which influence the price of a listing. Which is why we aim to find the \
    most important factors that affect the price and more importantly the features that is common\
    among the most expensive listings. This will allow an aspiring Airbnb host to ensure that his listing is equipped with those important features \
    such that he will be able to charge a higher price without losing customers. Moreover, a traveller will also know the factors to look into to get the lowest price possible while having certain features he prefers.")
    st.write("")

with tab2:
    st.header("EDA")
    df_map = st.session_state['df_map']
    st.write('AIRBNB ANALYSIS USING CHARTS')
    rb=st.selectbox("Insights list",( "1. Countries with highest number of listings",
                                       "2. Percentage of listing based on Roomtypes",
                                       "3. Hosts charging higher rents/lower rents",
                                       "4. Analysis of country,Roomtype and no.of amenities",
                                       "5. Impact on Price with respective to location(country) and type of room selected",
                                       "6. Hosts whose listings are busy (0 Availability) throughout the year",
                                       "7. Listings having higher number of reviews",
                                       "8. Distribution Of Airbnb Bookings Price Range Using Histogram after removing outliers",
                                       "9. Top 10 famous suburbs(neighbourhood) with listing count from all countries",
                                       "10. Top 10 hosts on the basis of number of listings"))
    if rb=="1. Countries with highest number of listings":
        df_mod=df_map.groupby(['country']).count()
        df_mod.reset_index(inplace=True)
        df_f1=df_mod[['country','listing_id']]
        bar_chart=pt.bar(df_f1,x='country',y='listing_id',title="Country and Listing count",height=600,width=600)
        st.plotly_chart(bar_chart,theme=None)
    elif rb=="2. Percentage of listing based on Roomtypes":
        df_room=df_map.groupby(['room_type']).count()
        df_room.reset_index(inplace=True)
        df_f2=df_room[['room_type','listing_id']]
        pie_chart=pt.pie(df_f2,values='listing_id',title="Room types and listing count",names='room_type',hover_data=['room_type'],height=600,width=600)
        st.plotly_chart(pie_chart,theme=None)
    elif rb=="3. Hosts charging higher rents/lower rents":
        st.header("TOP 10 HOST WITH HIGHER RENTS")
        out=df_map.groupby(['hostname',"country"])[['price']].max()
        out.reset_index(inplace=True)
        out1=out.sort_values("price",ascending=False).head(10)
        line_chart=pt.line(out1,x="hostname", y="price",color='country', title='TOP 10 HOST WITH HIGHER RENTS',height=500,width=500)
        st.plotly_chart(line_chart, theme=None)

        st.header("TOP 10 HOST WITH LESSER RENTS")
        out=df_map.groupby(['hostname',"country"])[['price']].max()
        out.reset_index(inplace=True)
        out1=out.sort_values("price").head(10)
        line_chart=pt.line(out1,x="hostname", y="price",color='country', title='TOP 10 HOST WITH LESSER RENTS',height=600,width=600)
        st.plotly_chart(line_chart,theme=None)
    elif rb=="4. Analysis of country,Roomtype and no.of amenities":
        df_rp=df_map.groupby(["country",'room_type'])[["no_of_amenities"]].count()
        df_rp.reset_index(inplace=True)
        df_f3=df_rp[['country','room_type','no_of_amenities']]            
        fig =pt.scatter(df_f3, x="room_type", y="no_of_amenities",size="no_of_amenities", color="country",size_max=60, height=600, width=800)
        st.plotly_chart(fig,theme=None)
    elif rb=="5. Impact on Price with respective to location(country) and type of room selected":
            df_cr=df_map.groupby(['country','room_type','no_of_amenities'])[['price']].mean()
            # df_cr['price'].astype('float')
            df_cr.reset_index(inplace=True)
            df_f4=df_cr[['country','room_type','price','no_of_amenities']]
            fig = pt.sunburst(df_f4,path=['country','room_type','price'],values='price',color='country')
            st.plotly_chart(fig)
    elif rb=="6. Hosts whose listings are busy (0 Availability) throughout the year":
            df_avail=df_map.sort_values(by=['availability_365','availability_30'], ascending=[True,True])[['availability_365','availability_30','country','room_type','hostname']].head(10)
            df_avail.reset_index(inplace=True)
            df_f5=df_avail[['country','room_type','hostname','availability_30','availability_365']]
            fig1 = pt.sunburst(df_f5,path=['country','room_type','availability_30','hostname'],hover_data='availability_365',color='country')
            st.plotly_chart(fig1,theme=None)
    elif rb=="7. Listings having higher number of reviews":
            df_new=df_map[['country','number_of_reviews','listing_name','listing_id','rating']].sort_values(by='number_of_reviews',ascending=False).head(10)
            bar_chart1=pt.bar(df_new,x='listing_name',y='number_of_reviews',hover_data=['country', 'rating'], color='rating',title="Listing with high reviews",height=600,width=600)
            st.plotly_chart(bar_chart1,theme=None)
    elif rb=="8. Distribution Of Airbnb Bookings Price Range Using Histogram after removing outliers":
            #first removing outliers calculating max and minimum thresold
            min_threshold = df_map['price'].quantile(0.05)
            max_threshold = df_map['price'].quantile(0.95)
            #len(df_full[df_full['price']<min_thresold])--->273
            #len(df_full[df_full['price']>max_thresold])--->265
            df_thresh=df_map[(df_map['price']<max_threshold) & (df_map['price']>min_threshold)]
            fig=plt.figure(figsize=(12, 5))
            # Set the seaborn theme to darkgrid
            sns.set_theme(style='darkgrid')
            # Create a histogram of the 'price' using df_thresh
            sns.histplot(df_thresh['price'],color=('r'))
            # Add labels to the x-axis and y-axis
            plt.xlabel('Price', fontsize=14)
            plt.ylabel('Density', fontsize=14)
            plt.title('Distribution of Airbnb Prices',fontsize=15)
            st.pyplot(fig)
    elif rb=="9. Top 10 famous suburbs(neighbourhood) with listing count from all countries":
            df_sub=df_map['suburbs'].value_counts()[1:10]
            colors = ['c', 'g', 'olive', 'y', 'm', 'orange', '#C0C0C0', '#800000', '#008000', '#000080']
            fig, ax = plt.subplots()
            ax = df_sub.plot.bar(stacked=True,color=colors,figsize=(15,6))
            plt.xlabel('suburbs', fontsize=14)
            plt.ylabel('count', fontsize=14)
            st.pyplot(fig)
            #fig=df_sub.plot(kind='bar', figsize=(15, 6), color = colors)
    elif rb=="10. Top 10 hosts on the basis of number of listings":
            z=df_map['hostname'].value_counts()[:10]
            colors = ['c', 'g', 'olive', 'y', 'm', 'orange', '#C0C0C0', '#800000', '#008000', '#000080']
            fig, ax = plt.subplots()
            ax = z.plot.bar(stacked=True,color=colors,figsize=(18,7))
            #z.plot(kind='bar', color=colors, figsize=(18, 7))
            plt.xlabel('hostname', fontsize=14)
            plt.ylabel('Total_listings', fontsize=14)
            plt.title('Top 10 hosts on the basis of no of listings', fontsize=15)
            st.pyplot(fig)
    
with tab3:
    st.header("Dynamic charts")
    list_of_q = ["1.AVERAGE PRICE OF DIFFERENT ROOM TYPES",
                                "2.AVERAGE PRICE OF DIFFERENT PROPERTY TYPES BASED ON LOCATION",
                                "3.BASED ON AMENITIES",
                                "4.MINIMUM NIGHTS BASED ON PROPERTY TYPE AND PRICE"]
                                
    option=st.radio("select one:",list_of_q)
    
    if option=="1.AVERAGE PRICE OF DIFFERENT ROOM TYPES":
        country= st.selectbox("Select the Country:",df_map["country"].unique())  
        df1= df_map[df_map["country"] == country]
        df1.reset_index(drop= True, inplace= True)
        df_bar= pd.DataFrame(df1.groupby("room_type")[["price"]].mean())
        df_bar.reset_index(inplace= True)
        fig_bar= pt.bar(df_bar, x='room_type', y= "price",title= "Average Price for Different room types", width=800, height=500, color='room_type')
        st.plotly_chart(fig_bar)

    if option=="2.AVERAGE PRICE OF DIFFERENT PROPERTY TYPES BASED ON LOCATION":
        country= st.selectbox("Select the Country:",df_map["country"].unique())  
        df1= df_map[df_map["country"] == country]
        df1.reset_index(drop= True, inplace= True)
        df_bar= pd.DataFrame(df1.groupby("property_type")[["price"]].mean())
        df_bar.reset_index(inplace= True)
        fig_bar= pt.bar(df_bar, x='property_type', y= "price", title= "Average Price for Different property types", width=800, height=700, color="property_type")
        st.plotly_chart(fig_bar,theme=None)

    if option=="3.BASED ON AMENITIES":
        country= st.selectbox("Select the Country:",df_map["country"].unique())  
        df1= df_map[df_map["country"] == country]
        df1.reset_index(drop= True, inplace= True)
        df_amen = df1.groupby(['no_of_amenities'])[['price']].mean()
        df_amen.reset_index(inplace=True)
        df_amen1=df_amen[['no_of_amenities','price']]
        fig_bar= pt.bar(df_amen1, x='no_of_amenities',y= "price", title= "",hover_data=["price"], width=600, height=500, color='price')
        st.plotly_chart(fig_bar,theme=None)
    
    if option=="4.MINIMUM NIGHTS BASED ON PROPERTY TYPE AND PRICE":
        min_night_option = st.radio("Select Minimum Nights:", ['<=5', '6 to 10', '11 to 20', '21 to 30', '31 to 40', '41 to 50', "\>50"])
        if min_night_option=='<=5':
            df_min_optn = df_map[df_map['minimum_nights'] <= 5]
        elif min_night_option=='6 to 10':
            df_min_optn = df_map[(df_map['minimum_nights'] > 5) & (df_map['minimum_nights'] <= 10)]
        elif min_night_option=='11 to 20':
            df_min_optn = df_map[(df_map['minimum_nights'] > 11) & (df_map['minimum_nights'] <= 20)]
        elif min_night_option=='21 to 30':
            df_min_optn = df_map[(df_map['minimum_nights'] > 21) & (df_map['minimum_nights'] <= 30)]
        elif min_night_option=='31 to 40':
            df_min_optn = df_map[(df_map['minimum_nights'] > 31) & (df_map['minimum_nights'] <= 40)]
        elif min_night_option=='41 to 50':
            df_min_optn = df_map[(df_map['minimum_nights'] > 41) & (df_map['minimum_nights'] <= 50)]
        elif min_night_option=='\>50':
            df_min_optn = df_map[(df_map['minimum_nights'] > 50)]
        
        df_min_optn.reset_index(inplace=True)
        df_line=df_min_optn.groupby(["minimum_nights","room_type"])[["price"]].mean()
        df_line.reset_index(inplace=True)
        df_s=df_line[['minimum_nights','price','room_type']]
        fig = pt.line(df_line, x="minimum_nights", y="price", color="room_type", text="minimum_nights")
        fig.update_traces(textposition="bottom right")
        st.plotly_chart(fig)
        
with tab4:
    st.header("GEO MAP")
    df_map = st.session_state['df_map']
    map=folium.Map(location=(40.730610, -73.935242),zoom_start=8,titles='OpenStreetMap',prefer_canvas=True)

    for i in range(0,len(df_map)):
        html=f"""
        <h3> {df_map.iloc[i]['suburbs']}</h3>
        <p>Listing_id: {df_map.iloc[i]['listing_id']}</p>
        <p>Host Name: {df_map.iloc[i]['hostname']}</p>
        <p>Price: {df_map.iloc[i]['price']}</p>
        """
        iframe = folium.IFrame(html=html, width=200, height=200)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(
            location=[df_map.iloc[i]['longitude'], df_map.iloc[i]['latitude']],
            popup=popup
        ).add_to(map)
        if i==100:
            break

    st_map=st_folium(map,width=700, height=450)


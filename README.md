# Airbnb Intro

Airbnb has provided many travellers a great, easy and convenient place to stay during their travels.
Similarly, it has also given an opportunity for many to earn extra revenue by listing their properties for residents to stay.
However, with so many listings available with varying prices, how can an aspiring host know what type of property to invest in if his main aim is to list it in Airbnb and earn rental revenue.
Additionally, if a traveller wants to find the cheapest listing available but with certain features he prefers like 'free parking' etc, how does he know what aspects to look into to find a suitable listing? 
There are many factors which influence the price of a listing. Which is why we aim to find the most important factors that affect the price and more importantly the features that is common among the most expensive listings.
This will allow an aspiring Airbnb host to ensure that his listing is equipped with those important features such that he will be able to charge a higher price without losing customers. 
Moreover, a traveller will also know the factors to look into to get the lowest price possible while having certain features he prefers.

## Dataset
	shape:(5555, 42)
	
 	columns present:'_id', 'listing_url', 'name', 'summary', 'space', 'description','neighborhood_overview', 'notes', 'transit', 'access', 'interaction',
       'house_rules', 'property_type', 'room_type', 'bed_type','minimum_nights', 'maximum_nights', 'cancellation_policy','last_scraped', 'calendar_last_scraped',
	'first_review', 'last_review',
       'accommodates', 'bedrooms', 'beds', 'number_of_reviews', 'bathrooms','amenities', 'price', 'security_deposit', 'cleaning_fee',
       'extra_people', 'guests_included', 'images', 'host', 'address','availability', 'review_scores', 'reviews', 'weekly_price','monthly_price', 'reviews_per_month'
       
## Steps Involved:
         1. Importing Libraries
	  
         2. Loading the Dataset in MONGODB
	  
         3. Convert to dataframe and Explore Dataset
	  
         4. Data Cleaning and Handling Outliers
	  
         5. Data Visualization

## Approach:
	1. MongoDB Connection and Data Retrieval: Establish a connection to the MongoDB Atlas database and retrieve the Airbnb dataset. 
 		Perform queries and data retrieval operations to extract the necessary information for your analysis.
   
	2. Data Cleaning and Preparation: Clean the Airbnb dataset by handling missing values, removing duplicates, and transforming data types as necessary. 
 		Prepare the dataset for EDA and visualization tasks, ensuring data integrity and consistency.
   
	3. Geospatial Visualization: Develop a streamlit web application that utilizes  the geospatial data from the Airbnb dataset to create interactive maps. 
 		Visualize the distribution of listings across different locations, allowing users to explore prices, ratings, and other relevant factors.
   
	4. Price Analysis and Visualization: Use the cleaned data to analyze and visualize how prices vary across different locations, property types, and seasons. 
 		Create dynamic plots and charts that enable users to explore price trends, outliers, and correlations with other variables.
   
	5. Availability Analysis by Season: Analyze the availability of Airbnb listings based on seasonal variations. 
 		Visualize the occupancy rates, booking patterns, and demand fluctuations throughout the year using line charts, heatmaps, or other suitable visualizations.
   
	6. Location-Based Insights: Investigate how the price of listings varies across different locations. 
 		Use MongoDB queries and data aggregation techniques to extract relevant information for specific regions or neighborhoods. 
   		Visualize these insights on interactive maps or create dashboards in tools like Tableau or Power BI.
     
	7. Interactive Visualizations: Develop dynamic and interactive visualizations that allow users to filter and drill down into the data based on their preferences.
 		Enable users to interact with the visualizations to explore specific regions, property types, or time periods of interest.
   
	8. Dashboard Creation: Utilize Tableau to create a comprehensive dashboard that presents key insights from your analysis. 
 		Combine different visualizations, such as maps, charts, and tables, to provide a holistic view of the Airbnb dataset and its patterns.

  
 Airbnb is a perfect example of an online business that has thrived through the revolutionary changes that have occurred with online businesses.
 This project helps in learning data cleaning and visualizing data and als helps in learning interactive and useful charts.



  

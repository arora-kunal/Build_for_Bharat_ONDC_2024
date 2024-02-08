import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from wordcloud import WordCloud

warnings.filterwarnings("ignore")

pd.options.display.max_columns = None
pd.options.display.max_rows = None

st.set_page_config(
    page_title="ONDC Hackathon Dashboard",
    page_icon="👩🏻‍💻"
)

# Define hardcoded username and password
CORRECT_USERNAME = "admin"
CORRECT_PASSWORD = "password123"

def display_login():
    st.title("Login Page")

    # Get username and password input from the user
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Check if username and password are correct
    if st.button("Login"):
        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            st.success("Login Successful!")
            st.write("You are now logged in.")
            # Display the main dashboard content after successful login
            main_dashboard()
        else:
            st.error("Invalid Username or Password")

def read_dataframe():
    Indian_df = pd.read_csv("../../Zomato/Indian_zomato.csv", encoding='ISO-8859-1')
    Indian_df.rename(columns={'Unnamed: 0': 'ID'}, inplace=True)
    Indian_df.drop(['Restaurant ID', 'Country Code', 'Locality', 'Currency', 'Rating color', 'Switch to order menu'],
                   axis=1, inplace=True)
    return Indian_df

def main_dashboard():
    st.title('Build for Bharat: Data as a service 🇮🇳')
    st.write("Hello, 👋 Welcome to the dashboard by Dlayer team")
    with st.sidebar:
        st.caption("<p style ='text-align:center'> Made with ❤️ by Eshika</p>", unsafe_allow_html=True )

    Industry_list = ['Food and Beverages', 'Fashion', 'Agriculture', 'Beauty and Personal Care']
    Industry = st.selectbox('Select your Industry from the dropdown', Industry_list)

    if Industry:
        if Industry != 'Food and Beverages':
            st.write("We will be there soon...")
        else:
            st.write("Showing results for ", Industry)
            Indian_df = read_dataframe()
            st.header("Analysis # 1")
            city_counts = Indian_df['City'].value_counts().reset_index()
            fig = px.bar(city_counts.head(5), x="count", y="City", orientation='h',
                         color='City', title='Top 5 Cities with Maximum number of Restraunts')
            st.plotly_chart(fig)

            st.header("Analysis # 2")
            Indian_df_cuisines_list = Indian_df['Cuisines'].tolist()
            Indian_df_cuisines_list = flattened_list(Indian_df_cuisines_list)
            Indian_df_Cuisines_df = pd.DataFrame(Indian_df_cuisines_list, columns=['Cuisine'])
            Indian_df_Cuisines_df = Indian_df_Cuisines_df['Cuisine'].value_counts().reset_index()
            fig = px.bar(Indian_df_Cuisines_df.head(5), x="count", y="Cuisine", orientation='h',
                         color='Cuisine', title='Top 5 Famous Cuisines rated by Customers')
            st.plotly_chart(fig)

            st.header("Analysis # 3")
            df_filtered = Indian_df.groupby('City')['Average Cost for two'].apply(remove_outliers).reset_index(name='Average Cost for two')
            df_filtered.drop(['level_1'], axis=1, inplace=True)
            fig_scatter = px.scatter(df_filtered, x='City', y='Average Cost for two', color='City',
                                     title='Average Cost for Two in Different Cities', labels={'price': 'Price'})
            st.plotly_chart(fig_scatter)

            st.header("Analysis # 4")
            popular_cities = city_counts.head(5).sort_values(by='City', ascending=False)
            top_5_cities = popular_cities['City'].tolist()
            top_5_cities_Indian_df = Indian_df[Indian_df['City'].isin(top_5_cities)]
            fig_scatter = px.scatter(top_5_cities_Indian_df, x='City', y='Average Cost for two', color='City',
                                     title='Average Cost for Two in Top 5 Cities with Maximum Restaurants',
                                     labels={'price': 'Price'})
            st.plotly_chart(fig_scatter)

            st.markdown("**For city level insights, click on the City Level insights from the left pane**")
            with st.expander("Want to know something specific about the analysis?Chat with our dashboard bot"):
                st.text_area("Enter your question to ask Dashboard bot")
                st.markdown("**Integration with Generative AI bot in progress. Stay tuned...**")

    st.divider()
    st.caption("<p style ='text-align:center'> Made with ❤️ by Eshika</p>", unsafe_allow_html=True )

def flattened_list(sample_list):
    flattened_items_list = [items.strip() for items in sample_list for items in items.split(',')]
    flattened_items_list = flattened_items_list
    return flattened_items_list

def remove_outliers(group):
    q_low = group.quantile(0.01)
    q_hi = group.quantile(0.99)
    return group[(group > q_low) & (group < q_hi)]

if __name__ == "__main__":
    display_login()

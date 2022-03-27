# Modules
import pandas as pd
import streamlit as st
from PIL import Image
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

img = Image.open('Olympic_rings_without_rims.svg.png')
st.set_page_config(page_title='Olympics-124 Analysis', page_icon=img)

hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden; }
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)

df = pd.read_csv('athlete_events.csv')
region_df = pd .read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("124 Years of Olympic Analysis")
st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_without_rims.svg/300px-Olympic_rings_without_rims.svg.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis', 'Medals Showcase of 2020 Olympics', 'Athletes Showcase of 2020 Olympics', 'Indian Medalist of 2020 Olympics')
)

# Conditions
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in "+str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title("Medal Tally in "+selected_country + "'s Overall Performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Editions", y="region")
    st.title("Participating Nations Over The Years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Editions", y="Event")
    st.title("Events Over The Years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Editions", y="Name")
    st.title("Athletes Over The Years")
    st.plotly_chart(fig)

    st.title("No. of Events Over Time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally Over The Years")
    st.plotly_chart(fig)

    st.title(selected_country + " Excels in the Following Sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    fig1 = ff.create_distplot([athlete_df['Height'].dropna()], ['Height Distribution'], show_hist=False, show_rug=False)
    fig1.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Height")
    st.plotly_chart(fig1)

    fig2 = ff.create_distplot([athlete_df['Weight'].dropna()], ['Weight Distribution'], show_hist=False, show_rug=False)
    fig2.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Weight")
    st.plotly_chart(fig2)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age with respect to Sports (Gold Medalist)")
    st.plotly_chart(fig)

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age with respect to Sports (Silver Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')


    st.title('Height Vs Weight of Athletes')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

df1 = pd.read_csv('Athletes.csv')
medals1_df = pd.read_csv('Medals.csv')
ind_athletes_df = pd.read_csv('Book1.csv')

medals1_df = preprocessor.post2020oly(medals1_df)
df1 = preprocessor.post2020olya(df1)
ind_athletes_df = preprocessor.post2020olyp(ind_athletes_df)


if user_menu == 'Medals Showcase of 2020 Olympics':
    st.sidebar.header("Medals Showcase")
    country_noc = helper.country_noc_show(medals1_df)
    selected_country_noc = st.sidebar.selectbox("Select a Country", country_noc)
    medals_showcase = helper.fetch_country_show(medals1_df, selected_country_noc)
    st.title("Totals Medals Won By Countries")
    st.image('https://www.deccanherald.com/sites/dh/files/styles/article_detail/public/articleimages/2021/07/31/678274-01-02-1-1014867-1627718322.jpg?itok=AA9DxPHr')
    st.table(medals_showcase)

if user_menu == 'Athletes Showcase of 2020 Olympics':
    df1.rename(columns={'NOC': 'Country'}, inplace=True)
    df1.rename(columns={'Discipline': 'Sport'}, inplace=True)
    st.sidebar.header("Athletes Showcase")
    country_athlete = helper.country_athlete_show(df1)
    selected_country_athlete = st.sidebar.selectbox("Select a Country", country_athlete)
    athletes_showcase = helper.fetch_country_athlete_show(df1, selected_country_athlete)
    st.title("Athletes in "+selected_country_athlete+" of Tokyo 2020 Olympics")
    st.image('https://img.olympicchannel.com/images/image/private/f_auto//v1552235080/primary/jux5g5vrxv5fnglq93yj')
    st.table(athletes_showcase)

if user_menu == 'Indian Medalist of 2020 Olympics':
    st.sidebar.image('https://img.olympicchannel.com/images/image/private/f_auto//v1552235080/primary/jux5g5vrxv5fnglq93yj')
    st.title("Indian Athletes with Medals")
    st.table(ind_athletes_df)
    st.image('https://images.news18.com/ibnlive/uploads/2021/08/1628404225_000_9kn9jh.jpg?impolicy=website&width=200&height=200')
    st.image('https://images.news18.com/ibnlive/uploads/2021/08/1628404353_lovlina-borgohain-ap-full-size-new.jpg?impolicy=website&width=200&height=200')
    st.image('https://images.news18.com/ibnlive/uploads/2021/08/1628406967_ap21217455989292.jpg?impolicy=website&width=200&height=200')
    st.image('https://images.news18.com/ibnlive/uploads/2021/08/1628404229_ap21219463148592.jpg?impolicy=website&width=200&height=200')
    st.image('https://images.news18.com/ibnlive/uploads/2021/08/1628404244_pv-sindhu-bronze-medal-toky-2020-ap-2.jpg?impolicy=website&width=200&height=200')
    st.image('https://images.news18.com/ibnlive/uploads/2021/08/1628404247_ravi-kumar-dahiya-1600-afp.jpg?impolicy=website&width=200&height=200')
    st.image('https://images.news18.com/ibnlive/uploads/2021/08/1628404238_mirabai-chanu-1600-ap-1.jpg?impolicy=website&width=200&height=200')

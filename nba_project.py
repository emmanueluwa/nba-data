import streamlit as st
import pandas as pd
import base64

#'st.' stands for streamlit
st.title('NBA Player Performance Stats')

st.markdown("""
This app performs webscraping of NBA players stats data
* **Python libraries used:** base64, pandas, streamlit
* **Data source used:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")


#side bar, title printed. range of years to filter through
st.sidebar.header('Choose your preferred Year, Team(s) and Postion(s)')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2018,2022))))


#scraping the data
# original url = https://www.basketball-reference.com/leagues/NBA_2021_per_game.html
#cache holds record of previously loaded selection
# '+ str(year) +' , allows for different years to be used 
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    #deletes repeated row seperating tables from being one table
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    #drops unwanted columns scraped from original page
    player_stats = raw.drop(['Rk','GS','FGA','3PA','2P','2PA','2P%','eFG%','FTA','ORB','DRB','TOV','PF'], axis=1) #,('MP', axis=8, 'FGA', axis=10, 'FG%', axis=11, '3PA', axis=13, '3P%', axis=14, '2P', axis=15, '2PA', axis=16, '2P%', axis=17)
    return player_stats
player_stats = load_data(selected_year)


#control team selection from the sidebar
#sort the Tm column alphabetically, values uniquely from the team column
sorted_unique_tm = sorted(player_stats.Tm.unique())
#multiselect function allows us to display all possible values, from all teams.. all teams shown
selected_tm = st.sidebar.multiselect('Team', sorted_unique_tm, sorted_unique_tm)

#same as above for positions. All possible positions listed
unique_ps = ['C', 'PF', 'SF', 'PG', 'SG']
selected_ps = st.sidebar.multiselect('Position', unique_ps, unique_ps)


#data filtered by user selection, changes result in team/positon variables updated
#call name of dataframe and inside the brackets you put the condition
df_selected_data = player_stats[(player_stats.Tm.isin(selected_tm)) & (player_stats.Pos.isin(selected_ps))]

#description of data table nafter filter + df(filtered scraped table) displayed
st.header('Stats for Selected Team(s) Per Game')
st.write('Data Dimension: ' + str(df_selected_data.shape[0]) + ' rows and ' + str(df_selected_data.shape[1]) + 'columns.')
st.dataframe(df_selected_data)


#downloading the data to a csv file
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806 for more info
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="player_stats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_data), unsafe_allow_html=True)
st.markdown("""
The following table explains each column heading. (% = Percentage)

| Heading       | Meaning       |
| ------------- |:-------------:| 
|   Pos         | Position      | 
|   Tm          | Team          |   
|   G           | Games         |   
|   MP          | Minutes Played|
|   FG          | Field Goals   |
|   FG %        | Field Goal %  |
|   3P          | 3 Pointers    |
|   3P%         | 3 Point %     |
|   FT          | Free Throws   |
|   FT%         | Free Throw %  |
|   TRB         | Total Rebounds|
|   AST         | Assists       |
|   STL         | Steals        |
|   BLK         | Blocks        |
|   PTS         | Points        |
""")



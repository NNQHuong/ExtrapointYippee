import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
st.title("🎈extra point yippeee🎈")
st.write("project nà")
#Import data
st.write("data raw nà")
url = 'https://drive.google.com/file/d/1uWqLQuaT7QVZekSylqGXNrTi0OXTq1QC/view?usp=drive_link'
url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]
df = pd.read_csv(url) #, encoding='unicode_escape'
df.info()

df.loc[df['Region'] == 'Caribbean ', 'Region'] = df.loc[df['Region'] == 'Caribbean ', 'Region'].str.replace(' ', '')

df = df.replace(",", ".", regex = True)

#Chuyển những cột số sang dạng định lượng bằng cách drop các cột định danh (chữ)
df_numeric = df.drop(columns=['Year','Unit','Code Value','Continent','Region','Country'])
df_numeric = df_numeric.astype(float)
df_numeric.info()

df_words = DataFrame(df, columns = ['Continent','Region','Country','Year','Unit','Code Value'])

#Join 2 data lại thành data hoàn chỉnh
df_typed = df_words.join(df_numeric)
df_typed.info()

#Sort theo GDP theo thứ tự giảm dần
df_sorted = df_typed.sort_values(by = 'GDP Per Capita (US$)', ascending = False)
df_sorted.head()

df_sorted.reset_index(drop=True, inplace=True)
df_sorted.head()

#scale
df_sorted['GDP Per Capita (US$)'] = np.log10(df_sorted['GDP Per Capita (US$)'])
df_sorted.head()

st.write("[qua 7749 bước làm sạch và scale sort dữ liệu các thứ]")

st.write("Nhóm dữ liệu")
#Nhóm tội về người: Human trafficking(buôn người) và Human smuggling (đưa người sang biên giới bất hợp pháp)
human_about = ['Human trafficking', 'Human smuggling']
df_sorted['Crimes About Human'] = df_sorted[human_about].mean(axis=1)

#Nhóm tội về chất cấm: Heroin, Cocaine, Cannabis (cần sa) and synthetic drug (ma túy tổng hợp) trade
drug_about = ['Heroin trade', 'Cocaine trade', 'Cannabis trade', 'Synthetic drug trade']
df_sorted['Crimes About Drugs'] = df_sorted[drug_about].mean(axis=1)

#Nhóm tội có tổ chức: Criminal actors, Mafia-style groups, Criminal networks, State-embedded actors, Foreign actors
group_about = ['Mafia-style groups', 'Criminal networks', 'State-embedded actors', 'Foreign actors']
df_sorted['Organized Crimes'] = df_sorted[group_about].mean(axis=1)

#Nhóm tội khác: Criminality, Criminal markets, Arms trafficking, Flora crimes, Fauna crimes
other_crimes = ['Criminal markets', 'Arms trafficking', 'Flora crimes', 'Fauna crimes']
df_sorted['Other Crimes'] = df_sorted[other_crimes].mean(axis=1)

#Nhóm yếu tố về chính phủ: Political leadership and governance, Government transparency and accountability
gov_about = ['Political leadership and governance', 'Government transparency and accountability']
df_sorted['Anti-crimes About Government'] = df_sorted[gov_about].mean(axis=1)

#Nhóm yếu tố về luật: National policies and laws, Judicial system and detention, Law enforcement
law_about = ['National policies and laws', 'Judicial system and detention', 'Law enforcement']
df_sorted['Anti-crimes About Laws'] = df_sorted[law_about].mean(axis=1)

#Nhóm yếu tố về tổ chức khác: International cooperation, Non-state actors
corp_about = ['International cooperation', 'Non-state actors']
df_sorted['Anti-crimes About Corporations'] = df_sorted[corp_about].mean(axis=1)

#Nhóm yếu tố về kinh tế - xã hội: Anti-money laundering, Economic regulatory capacity, Prevention
society_about = ['Anti-money laundering', 'Economic regulatory capacity', 'Prevention']
df_sorted['Anti-crimes About Society'] = df_sorted[society_about].mean(axis=1)

df_sorted.head()

st.write("ra data hoàn chỉnh")
#Ra data mới đã được làm gọn
grouped = ['Continent', 'Region', 'Country', 'Year', 'Unit', 'Code Value',
           'Criminality', 'Crimes About Human', 'Crimes About Drugs', 'Criminal actors',
           'Organized Crimes', 'Other Crimes', 'Resilience',
           'Victim and witness support', 'Anti-crimes About Government',
           'Anti-crimes About Laws', 'Anti-crimes About Corporations',
           'Anti-crimes About Society', 'GDP Per Capita (US$)']
df_grouped = df_sorted[grouped]
df_grouped.head()

Criminality_GDP = px.scatter(df_grouped, x="Criminality", y="GDP Per Capita (US$)", trendline="ols")
st.show()



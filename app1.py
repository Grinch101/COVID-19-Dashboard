import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
#%matplotlib inline
#import cufflinks as cf
#import plotly.io as pio
import plotly.graph_objects as go
import plotly
# import plotly.express as px
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot 
#cf.go_offline()
#init_notebook_mode(connected = True) 





#################
## Polishing US DATA:
################

#confirmed_cases = pd.read_csv("time_series_covid_19_confirmed_US.csv")
confirmed_cases = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
confirmed_cases = pd.DataFrame(confirmed_cases.groupby(by='Province_State').sum()).reset_index()
confirmed_cases = confirmed_cases.drop(['UID','code3','FIPS','Lat','Long_'],axis=1)


deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv")
#deaths = pd.read_csv("time_series_covid_19_deaths_US.csv")
deaths = pd.DataFrame(deaths.groupby(by='Province_State').sum()).reset_index()
deaths = deaths.drop(['UID','code3','FIPS','Lat','Long_','Population'],axis=1)



trans_confirmed_cases = confirmed_cases.set_index("Province_State").transpose()
trans_deaths = deaths.set_index("Province_State").transpose()



state_names = ['Alabama', 'Alaska', 'American Samoa', 'Arizona', 'Arkansas',
       'California', 'Colorado', 'Connecticut', 'Delaware', 'Diamond Princess',
       'District of Columbia', 'Florida', 'Georgia', 'Grand Princess', 'Guam',
       'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
       'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
       'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
       'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
       'North Carolina', 'North Dakota', 'Northern Mariana Islands', 'Ohio',
       'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island',
       'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',
       'Vermont', 'Virgin Islands', 'Virginia', 'Washington', 'West Virginia',
       'Wisconsin', 'Wyoming']
state_names.sort()

new_col_names2=[]
for i in list(trans_confirmed_cases.columns):
    new_col_names2.append(i+"_Confirmed")


new_col_names=[]
for i in list(trans_deaths.columns):
    new_col_names.append(i+"_Death")

trans_confirmed_cases.columns = new_col_names2
trans_deaths.columns = new_col_names


trans_deaths = trans_deaths.sort_index(axis=1)
trans_confirmed_cases = trans_confirmed_cases.sort_index(axis=1)


new_df = trans_deaths.join(trans_confirmed_cases)


for i in state_names:

    new_df[f"{i}_Rate"] = new_df[f'{i}_Death'] / new_df[f'{i}_Confirmed']
    new_df[f"{i}_Rate"].fillna(0,inplace=True)

new_df.sort_index(axis=1, inplace=True)


my_columns = pd.MultiIndex.from_product([state_names, ['Confirmed', 'Death','Rate']],
                                       names=["Region","Values"])

new_df.columns = my_columns

new_df = new_df.reset_index()


new_df['Time'] =  pd.to_datetime(new_df.reset_index()['index'], format='%m/%d/%y')


new_df.set_index('Time',inplace=True)
new_df.drop('index',axis=1,inplace=True)

my_dict = {'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Islands':'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virgin Islands': 'VI',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'}


US = new_df.copy()
del new_df


########
## China Data:
#######



# Global Confirmed Cases DataFrame
#Global_Confirmed = pd.read_csv("time_series_covid_19_confirmed.csv")
Global_Confirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")

# China Confirmed Cases DataFrame
China_Confirmed = Global_Confirmed[(Global_Confirmed['Country/Region']=="China") ]



# Global Death Cases DataFrame
#Global_Death = pd.read_csv("time_series_covid_19_deaths.csv")
Global_Death = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")

# China Death Cases DataFrame
China_Death = Global_Death[(Global_Confirmed['Country/Region']=="China") ]





China_Confirmed = China_Confirmed.drop(["Lat","Long"],axis=1)
China_Death = China_Death.drop(["Lat","Long"],axis=1)

China_Confirmed.set_index('Province/State',inplace=True)
China_Death.set_index('Province/State',inplace=True)

China_Confirmed.drop("Country/Region",axis=1,inplace=True)
China_Death.drop("Country/Region",axis=1,inplace=True)


China_Death = China_Death.transpose()
China_Confirmed = China_Confirmed.transpose()


China = China_Death.join(China_Confirmed, lsuffix='_Death')

China.sort_index(axis=1,inplace=True)



China.reset_index(inplace=True)

China['Time'] = pd.to_datetime(China["index"])
China.set_index('Time',inplace=True)

China.drop('index' , axis=1 , inplace=True)
China_Provinces = list(China_Confirmed.columns)
for i in China_Provinces:

    China[f"{i}_Rate"] = China[f'{i}_Death'] / China[f'{i}']

China.sort_index(axis=1,inplace=True)
China_columns = pd.MultiIndex.from_product([China_Provinces, ['Confirmed', 'Death','Rate']],
                                       names=["Region","Values"])

China.columns = China_columns

China.fillna(0,inplace=True)



########
## Look at global data:
#######
Countries_Confirmed = pd.DataFrame(Global_Confirmed.groupby(by = 'Country/Region').sum())
Countries_Death = pd.DataFrame(Global_Death.groupby(by = 'Country/Region').sum())

Countries_Confirmed.drop(['Lat',"Long"],axis=1,inplace=True)
Countries_Death.drop(['Lat',"Long"],axis=1,inplace=True)

Countries_Confirmed = Countries_Confirmed.transpose()
Countries_Death = Countries_Death.transpose()

# Countries_Confirmed.sort_index(inplace=True)
# Countries_Death.sort_index(inplace=True)

Countries = Countries_Death.join(Countries_Confirmed, lsuffix='_Death')

#Countries.sort_index(inplace=True,axis=1)


Countries.reset_index(inplace=True)
Countries['Time'] = pd.to_datetime(Countries["index"])
Countries.set_index('Time',inplace=True)

Countries.drop('index' , axis=1 , inplace=True)
Country_names = list(Countries_Confirmed.columns)
for i in Country_names:

    Countries[f"{i}_Rate"] = Countries[f'{i}_Death'] / Countries[f'{i}']
    
    
Countries.sort_index(inplace=True, axis=1)
Countries.fillna(0,inplace=True)
country_names = list(Countries_Confirmed.columns)

Country_cols = pd.MultiIndex.from_product([country_names, ['Confirmed', 'Death','Rate']],
                                       names=["Region","Values"])

Countries.columns = Country_cols
#Countries.sort_index(inplace=True,axis=1)
#del Countries_Confirmed
#del Countries_Death
#del Country_cols
Countries.rename(mapper={'US':"United States"},axis=1,inplace=True)

#Countries.tail(4)


#import pandas as pd


df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")

#df = pd.read_csv("time_series_covid_19_confirmed.csv")
df = df.groupby('Country/Region').sum()

df = df.reset_index()

date_lists=[]
for i in df.columns:
    if i not in [ 'Country/Region', 'Lat', 'Long']:
        date_lists.append(i)

mylist=[]        
for i in date_lists:

    dftemp = df[[ 'Country/Region', 'Lat', 'Long']].copy()
    dftemp["Confirmed"] = df[i].copy()
    dftemp["Date"] = pd.to_datetime(i,dayfirst=False,format='%m/%d/%y')
    mylist.append(dftemp)
    
df_glob_conf= pd.concat(mylist)
df_glob_conf= df_glob_conf.sort_values(by=['Country/Region','Date'])


df =pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")

#df = pd.read_csv("time_series_covid_19_deaths.csv")
df = df.groupby('Country/Region').sum()

df = df.reset_index()
date_lists=[]
for i in df.columns:
    if i not in ['Country/Region', 'Lat', 'Long']:
        date_lists.append(i)

mylist=[]        
for i in date_lists:

    dftemp = df[['Country/Region', 'Lat', 'Long']].copy()
    dftemp["Death"] = df[i].copy()
    dftemp["Date"] = pd.to_datetime(i,dayfirst=False,format='%m/%d/%y')
    mylist.append(dftemp)
    
df_glob_death= pd.concat(mylist)
df_glob_death= df_glob_death.sort_values(by=['Country/Region','Date'])


df_globe = df_glob_conf.merge(df_glob_death)
# df_globe = df_globe.drop("Province/State",axis=1)
df_globe["Country/Region"] = df_globe["Country/Region"].replace("US",'United States')
df_pop = pd.read_csv('population_by_country_2020.csv')
# df_pop = pd.read_csv('https://raw.githubusercontent.com/Grinch101/population-by-country/master/population_by_country_2020.csv')

df_pop.set_index('Country (or dependency)',inplace=True)
pop_dic = df_pop.to_dict()['Population (2020)']
df_globe['Population'] = df_globe['Country/Region'].map(pop_dic)
df_globe["Country/Region"] = df_globe["Country/Region"].replace("US",'United States')

# del df_pop
# del df_glob_conf
# del df_glob_death

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
df.drop('GDP (BILLIONS)',axis=1,inplace=True) # we need countrycodes ... 
df.set_index('COUNTRY',inplace=True)
country_codes = df.to_dict()['CODE']


df_globe['CODE'] = df_globe['Country/Region'].map(country_codes)
df_globe['Death'] = abs(df_globe['Death'])
df_globe['Confirmed'] = abs(df_globe['Confirmed'])


#lat_long = pd.read_csv("time_series_covid_19_deaths.csv")
lat_long = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")

lat_long = lat_long.set_index('Country/Region')

lat_long_dict = lat_long.to_dict()


df_globe['Lat'] = df_globe['Country/Region'].map(lat_long_dict['Lat'])
df_globe['Long'] = df_globe['Country/Region'].map(lat_long_dict['Long'])


today = df_globe["Date"].max().date()
################################################################

#df = pd.read_csv("time_series_covid_19_confirmed_US.csv")
df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")

date_lists=[]
for i in df.columns:
    if i not in ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
       'Country_Region', 'Lat', 'Long_', 'Combined_Key']:
        date_lists.append(i)

mylist=[]        
for i in date_lists:

    dftemp = df[['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
       'Country_Region', 'Lat', 'Long_', 'Combined_Key']].copy()
    dftemp["Confirmed"] = df[i].copy()
    dftemp["Date"] = pd.to_datetime(i,dayfirst=False,format='%m/%d/%y')
    mylist.append(dftemp)

    
    
df_us_conf= pd.concat(mylist)
df_us_conf= df_us_conf.sort_values(by=['Province_State','Date'])



#df = pd.read_csv("time_series_covid_19_deaths_US.csv")
df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv")

date_lists=[]
for i in df.columns:
    if i not in ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
       'Country_Region', 'Lat', 'Long_', 'Combined_Key','Population']:
        date_lists.append(i)

mylist=[]        
for i in date_lists:

    dftemp = df[['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
       'Country_Region', 'Lat', 'Long_', 'Combined_Key','Population']].copy()
    dftemp["death"] = df[i].copy()
    dftemp["Date"] = pd.to_datetime(i,dayfirst=False,format='%m/%d/%y')
    mylist.append(dftemp)
    
df_us_death= pd.concat(mylist)
df_us_death= df_us_death.sort_values(by=['Province_State','Date'])


df_us = df_us_conf.merge(df_us_death)

del df_us_conf
del df_us_death



import cufflinks as cf

fig5 = df_globe[df_globe['Date'] == df_globe['Date'].max()].sort_values(by='Death',ascending=False)[:10].set_index('Country/Region')[['Confirmed','Death']].sort_values(by='Death').iplot(kind='bar',
orientation='h',
asFigure=True,
barmode='group',
colors=['purple','brown'],
title=f'Cumulative Death Cases up to {df_globe["Date"].max().date()}' 
)
fig5.data[0]['name'] = 'Confirmed Cases'
fig5.data[1]['name'] = 'Death Cases'
fig5.update_layout(width=800, height=600,
        margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=80, #top margin
    ))


fig6 = Countries.iloc[:,Countries.columns.get_level_values(1)=='Death'].diff().iloc[-1].sort_values(ascending = False)[:15].sort_values().iplot(
kind='bar',
    colors='red',
    orientation='h',
    title=f'Countries with the heighest deaths at {today}',
    asFigure=True)
fig6.update_layout(
	width=800, height=600,
        margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=80, #top margin
    ))


new_row = []
for i in fig6.data[0]['y']:
    new_row.append(i.split(",")[0].split("(")[1])
    
fig6.data[0]['y'] = new_row 




#######################################



today = df_globe["Date"].max().date()
total_confirmed = df_globe[df_globe['Date']==df_globe['Date'].max()].sum(axis=0)['Confirmed']
total_death = df_globe[df_globe['Date']==df_globe['Date'].max()].sum(axis=0)['Death']
numb_countries = len(pop_dic.keys())
affected_countries = len(df_globe['Country/Region'].unique())
affected_pop = df_globe[df_globe['Date']==df_globe['Date'].min()].sum(axis=0)['Population']
total_pop =df_pop['Population (2020)'].sum()
affected_pop_ratio =affected_pop/ total_pop
affected_pop_ratio = round(affected_pop_ratio,2)
affection_ratio = round(total_death/total_confirmed , 2)


s1 = 'STORY TELLING: '
s2 = f'Up to {today},  {total_confirmed}  cases of COVID-19 have been identified in  {affected_countries}   countries.'
s3 = f'Affected countries have total population of  {int(affected_pop)}  which is about  {affected_pop_ratio}  of the total population of   {total_pop}  .'
s4 = f'{total_death}   individuals have died which is   {affection_ratio}  of the  total COVID-19 cases.'
s44 = f"it means a {round(total_confirmed/total_pop, 4)*100} percent of the world has diagnosed with COVID and {round(total_death/total_pop,5)*100} percent of earth's total population have died due to it."
s5 = f'for more info please hover your mouse over below figure or zoom/pan on a region '


#########################################################
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#import pandas as pd
#import plotly.offline as pyo
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
#import dash_auth

#USERNAME_PASSWORD_PAIRS =[ ["username",'password'],["JamesBond","007"]]

app = dash.Dash()
#auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
server = app.server


app.layout = html.Div([
    html.H1("COVID-19 DASHBOARD "),
    html.Div(dcc.Graph(figure=fig6,style={'width': '100%', 'marginBottom': 10, 'marginTop': 25})),
#     html.Div(dcc.Graph(id='Choropleth3'), style = {"width" : "100%"}),
    html.H2(s1),
    html.H3(s2),
    html.H3(s3),
    html.H3(s4),
    html.H3(s44),
    html.H4(s5),
    
    html.Div(dcc.Graph(id='Choropleth'), style = {"width" : "100%",'marginBottom': 10, 'marginTop': 25}),
    html.H3("Top 10 countires with highest death cases"),
    html.Div(dcc.Graph(figure=fig5),style={'width': '100%', 'marginBottom': 10, 'marginTop': 25}),


    html.H1("."),
    html.H2("BAR PLOTS"),
    html.H4("Change the parameters to compare"),
    html.Div(dcc.Dropdown(id="country", multi = True, 
                 options = [{'label': i, "value": i} for i in Countries.columns.get_level_values(0).unique()],
                  value = ["Iran",'Turkey','Italy']),style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div(dcc.Dropdown(id='feature',multi = True, 
                 options = [{'label':"Confirmed cases","value" : 'Confirmed'},
                {'label':"Death Cases","value" : 'Death'}],
                  value = ['Death']), style = {'width': '48%', 'display': 'inline-block'} ),
    
    html.Div([html.Label("Select Bar chart mode"),dcc.RadioItems(id='mode',
                   options = [{'label':'Nested Bar Chart','value':'group'},
                             {'label':'Stacked Bar Chart','value':'stack'}], 
                            value = 'group')],style={'width': '28%', 'float': 'below'}),
    
    
    html.Div(dcc.Graph(id='barplot'), style = {"width" : "100%"}),

    html.Div(dcc.Graph(id='barplot3'), style = {"width" : "100%"}),
             ])
    

    




@app.callback(Output('barplot','figure'),
              [Input('country','value'),
               Input('feature','value'),
               Input('mode','value')    ])
def graph_barplot1(country,feature,mode):
    

    import random


    fig = make_subplots(cols=1,rows=2,shared_xaxes=True,vertical_spacing=0.001
                       )
    for i in feature:
        for j in country:
            fig.add_trace(go.Bar(x = Countries.index, y = Countries[j][i],hovertext=f'{i}<br>in {j} ' ,
                                 name = f'Cumulative {i} in {j}'),col=1,row=2      )
            fig.update_layout(hovermode = 'x', barmode=mode )


    for i in feature:
        for j in country:
            fig.add_trace(go.Bar(x = Countries.index, y = Countries.diff()[j][i],hovertext=f'{i}<br>in {j}' ,
                                 name = f'Daily {i} in {j}'),col=1,row=1      )
            fig.update_layout(hovermode = 'x', barmode=mode )


    fig.update_layout(width=800, height=600,

                      legend=dict(
            x=0,
            y=1,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2
        ),
                     margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=80, #top margin
    ))

    fig.update_layout(title_text=f"Daily vs Cumulative {feature} in {country}")


    return fig





@app.callback(Output('barplot3','figure'),
              [Input('mode','value'),
               Input('feature','value') ])
def world_barplot(mode,feature):
    
#     rate = (Countries.iloc[ : ,Countries.columns.get_level_values(1)=='Death'].sum(axis=1)) / (Countries.iloc[ : ,Countries.columns.get_level_values(1)=='Confirmed'].sum(axis=1))
#     rate2 = (Countries.diff().iloc[ : ,Countries.diff().columns.get_level_values(1)=='Death'].sum(axis=1)) / (Countries.diff().iloc[ : ,Countries.diff().columns.get_level_values(1)=='Confirmed'].sum(axis=1))
    import random


    fig = make_subplots(cols=1,rows=2,shared_xaxes=True,vertical_spacing=0.001               )
#     fig.add_trace(go.Scatter(name = "Ratio of deaths to confirmed cases ", x = Countries.index , y = rate ) ,col=1,row=2)
    for i in feature:
        fig.add_trace(go.Bar(x = Countries.index, y = Countries.iloc[ : ,Countries.columns.get_level_values(1)==i].sum(axis=1),
                             hovertext=f'{i}<br>in the world ' ,
                                 name = f'Cumulative {i} in the world'),col=1,row=2      )
        fig.update_layout(hovermode = 'x', barmode=mode )

#     fig.add_trace(go.Scatter(name = "Ratio of deaths to confirmed cases ", x = Countries.index , y = rate2 ) ,col=1,row=1)
    for i in feature:
    
        fig.add_trace(go.Bar(x = Countries.index, y = Countries.diff().iloc[ : ,Countries.columns.get_level_values(1)==i].sum(axis=1),
                             hovertext=f'{i}in the world' ,
                             name = f'Daily {i} in the world'),col=1,row=1      )
        fig.update_layout(hovermode = 'x', barmode=mode )


    fig.update_layout(width=800, height=600,

                      legend=dict(
            x=0,
            y=1,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2
        ),
        margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=80, #top margin
    ))

    fig.update_layout(title_text=f"Daily vs Cumulative {feature}")


    return fig
    
    
    




@app.callback(Output('Choropleth','figure'),
             [Input('feature','value')])
def world_choroleth(feature):

    
    df4 = df_globe[df_globe["Date"]==df_globe["Date"].max()].copy()
    today = df_globe["Date"].max().date()
    df4['text_death'] = f" at date: {today}  <br>" + df4['Death'].astype(str) +" Death cases <br>" +  df4['Confirmed'].astype(str) + " Confirmed cases"+ "<br>Population at 2020: " +df4['Population'].astype(str) 
    df4['text_confirmed'] = f" at date: {today} <br>" +  df4['Confirmed'].astype(str) + " Confirmed cases" + "<br>Population at 2020: " +df4['Population'].astype(str) 
    features = ['Confirmed','Death']
    colors = ["Purple","brown"]
    scale = 8000



    data = [go.Choropleth(
        locations = df4['CODE'],
        z = df4['Population'],
        text = df4['Population'],
        colorscale = 'reds_r',
        zmax = 700000000,
        zmin = 20000000,
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title = 'Population',
        colorbar = None,
        showscale = False
        ,name='pop choropleth' )
            ,

         go.Scattergeo(    
        locationmode = 'country names',
        locations = df4["Country/Region"],
           lon = df4['Long'],
           lat = df4['Lat'],
            text = df4['text_confirmed'],
            marker = dict(
                size = df4['Confirmed']/scale,
                color = "purple",
                line_color='rgb(40,40,40)',
                line_width=1,
                sizemode = 'area'
            ),name='Confirmed'),

           go.Scattergeo(    
        locationmode = 'country names',
        locations = df4["Country/Region"],
           lon = df4['Long'],
           lat = df4['Lat'],
            text = df4['text_death'],
            marker = dict(
                size = df4['Death']/scale,
                color = "brown",
                line_color='rgb(40,40,40)',
                line_width=1,
                sizemode = 'area'
            ),name="Death")
          ]



    layout = go.Layout(
        autosize = True,
#             title_text = f"Global situation of COVID-19 at {today}, colored by population",
            showlegend = False,
    #         updatemenus=[dict(
    #             type="buttons",
    #             buttons=[dict(label="Play",
    #                           method="animate",
    #                           args=[None])])]

            )


    # myframes = []



    # for i in df_globe['Date'].unique():
    #     df4 = df_globe[df_globe['Date']==i]

    #     myframes.append(
    #     go.Frame(
    #       baseframe="Total number of confirmed cases",
    #     data=[go.Scattergeo(marker = dict(size = df4["Confirmed"]/2500,
    #                                      color = ["purple"])) ],
    #     name = f"Confirmed at {i}"


    #     ))


    # for i in df_globe['Date'].unique():
    #     df4 = df_globe[df_globe['Date']==i]

    #     myframes.append(
    #     go.Frame(
    #       baseframe="Total number of death cases",
    #     data=[go.Scattergeo(marker = dict(size = df4["Death"]/2500,
    #                                      color = "brown")) ],
    #     name = f"Death at {i}"


    #     ))




    # fig = go.Figure(data=data,layout=layout,frames = myframes)
    fig = go.Figure(data=data,layout=layout) 




    fig.update_layout(
#         title='Map of COVID-19',
                      width=800,
                      height=600 ,
                      margin={"r":5,"t":0,"l":5,"b":5})
    return fig





@app.callback(Output('Choropleth3','figure'),
             [Input('feature','value')])
def animated_choropleth(feature):
    fig = px.scatter_geo(data_frame=df_globe,
                         locationmode='country names',
                         lat='Lat',lon='Long',
                     animation_frame=df_globe["Date"].astype(str),
                         hover_name='Country/Region',
                         size_max=75,
                         size=df_globe["Death"],
                     color='Population'
                     
                )

    fig.update_layout(title= 'Animated Map of COVID19', width=800, height=600 ,
#                       margin={"r":5,"t":25,"l":5,"b":5}
                     )
    return fig



if __name__ == "__main__":
    app.run_server()
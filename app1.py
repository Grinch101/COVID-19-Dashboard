import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import datetime
import pandas as pd
import dash_table
import plotly.figure_factory as ff
import numpy as np
import time
 
  
Update = str(pd.Timestamp.today().date())

########
## Look at global data:
########


### COVID ################################################
Global_Death1 = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")


Global_Confirmed1 = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")


Countries_Confirmed = pd.DataFrame(Global_Confirmed1.groupby(by = 'Country/Region').sum())
Countries_Death = pd.DataFrame(Global_Death1.groupby(by = 'Country/Region').sum())

Countries_Confirmed.drop(['Lat',"Long"],axis=1,inplace=True)
Countries_Death.drop(['Lat',"Long"],axis=1,inplace=True)

Countries_Confirmed = Countries_Confirmed.transpose()
Countries_Death = Countries_Death.transpose()



Countries = Countries_Death.join(Countries_Confirmed, lsuffix='_Death')




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

Countries.rename(mapper={'US':"United States"},axis=1,inplace=True)



df = Global_Confirmed1
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


df = Global_Death1
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
# df_pop = pd.read_csv('population_by_country_2020.csv')
df_pop = pd.read_csv('https://raw.githubusercontent.com/Grinch101/COVID-19-Dashboard/main/population_by_country_2020.csv')

df_pop.set_index('Country (or dependency)',inplace=True)
pop_dic = df_pop.to_dict()['Population (2020)']
df_globe['Population'] = df_globe['Country/Region'].map(pop_dic)
df_globe["Country/Region"] = df_globe["Country/Region"].replace("US",'United States')



df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')

df.drop('GDP (BILLIONS)',axis=1,inplace=True) # we need countrycodes ... 
df.set_index('COUNTRY',inplace=True)
country_codes = df.to_dict()['CODE']


df_globe['CODE'] = df_globe['Country/Region'].map(country_codes)
df_globe['Death'] = abs(df_globe['Death'])
df_globe['Confirmed'] = abs(df_globe['Confirmed'])


lat_long = Global_Death1
lat_long = lat_long.set_index('Country/Region')

lat_long_dict = lat_long.to_dict()


df_globe['Lat'] = df_globe['Country/Region'].map(lat_long_dict['Lat'])
df_globe['Long'] = df_globe['Country/Region'].map(lat_long_dict['Long'])



#+++++++++++++++++++++++
time.sleep(1)

mode='group'
tempz = make_subplots(cols=1,rows=2,shared_xaxes=True,vertical_spacing=0.001)
colors=['blue','red']
country=['Canada']
mode='group'


tempz.add_trace(go.Bar(x = Countries.index, y = Countries.diff()['Canada']['Death'],hovertext=f' Deaths<br>in Canada ' ,
                            name = f'Daily Deaths in Canada',
                        marker_color=colors.pop()),col=1,row=2      )
tempz.update_layout( barmode=mode )





tempz.add_trace(go.Bar(x = Countries.index, y = Countries.diff()['Canada']['Confirmed'],hovertext=f'Confirmed<br>in Canada' ,
                            name = f'Daily Confirmed Cases in Canada',
                        marker_color=colors.pop()),col=1,row=1      )
tempz.update_layout( barmode=mode )

# for j in country:
#     tempz.add_trace(go.Scatter(x=Countries.index, y = Countries.diff()[j]['Confirmed'].rolling(window=7).mean(),
#                              mode='markers',
#                              marker=dict(color='black',
#                                          size=3),
#                         hovertext=f'Confirmed cases<br>in {j} ',
#                         name = f'weekly average of confirmed cases in {j}',
#                         ))


tempz.update_layout(
        hovermode='x',
        autosize=True,
        showlegend=False,
        margin=go.layout.Margin(
        l=35, #left margin
        r=0, #right margin
        b=35, #bottom margin
        t=55, #top margin
        )
        )


tempz.update_layout(title_text=f"Daily (up) and Cumulative (down) cases of COVID-19 in Canada")





###### layout
app = dash.Dash()
app.title = 'PR Applications Progress'
server = app.server


app.layout = html.Div([



html.Div([html.H1('COVID-19 Overview',style={'textAlign':'center','font-family':'calibri'}),
    html.Div(dcc.Graph(id='A',
                       config={"displaylogo": False,
              'modeBarButtonsToRemove': ['pan2d','lasso2d']}
             ),
             style={'width':'48%','display':'inline-block' }),
    
    html.Div(
#         html.Pre(id='hover-data'),
        
        dcc.Loading(dcc.Graph(id='barplot',figure=tempz,
                       config={"displaylogo": False,
              'modeBarButtonsToRemove': ['pan2d','lasso2d']} )),
        
             style={'width':'48%','display':'inline-block' }),
    
     
    html.Div(dcc.Slider(id='S',
                min=0,
                max=len(df_globe['Date'].unique())-1,
                step=1,
            #     step=datetime.timedelta(days=1),
            #     marks={i: '{}'.format(i) for i in range(0, 100)},
                value=len(df_globe['Date'].unique())-1,
                ),style={'width':'48%','display':'inline-block' }),
    
    html.Pre(id='Screen')

    ],
    
    
    style={'width':'95%','font':'Calibri','color':'black', 'border':'1px black solid',
        'marginLeft':4,'marginBottom':100}),

#########

            ])

#...

@app.callback(Output('output-container-date-picker-single','children'),
             [Input('my-date-picker-single','date')])
def update_output(date):
    string_prefix = 'You have selected: '
    if date is not None:
        date = dt.strptime(re.split('T| ', date)[0], '%Y-%m-%d')
        date_string = date.strftime('%A %B %d, %Y')
        return string_prefix + date_string


###################

@app.callback(Output('A','figure'),
             [Input('S','value')])
def world_choroleth(day):
    
    i = day*datetime.timedelta(days=1) + df_globe["Date"].min()

    df4 = df_globe[df_globe["Date"]==i]
    today = i.date()
    df4['text_death'] = f" at date: {today}  <br>" + df4['Death'].astype(str) +" Death cases <br>" +  df4['Confirmed'].astype(str) + " Confirmed cases"+ "<br>Population at 2020: " +df4['Population'].astype(str) 
    df4['text_confirmed'] = f" at date: {today} <br>" +  df4['Confirmed'].astype(str) + " Confirmed cases" + "<br>Population at 2020: " +df4['Population'].astype(str) 
    features = ['Confirmed','Death']
    colors = ["Purple","brown"]
    scale = 5000



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


    fig = go.Figure(data=data) 
    fig.update_layout(
            title='click on a country to see its trend',
            )
        
    fig.update_layout(
        autosize=True,
        showlegend=False,
        margin=go.layout.Margin(
        l=35, #left margin
        r=0, #right margin
        b=35, #bottom margin
        t=55, #top margin
        )
        )  
        
    return fig

@app.callback(Output('Screen','children'),
             [Input('S','value')])
def screen(day):
    
    i = day*datetime.timedelta(days=1) + df_globe["Date"].min()
    i = i.date()
    
    return "You have selected " +str(i)


 

 


@app.callback(Output('barplot','figure'),
              [Input('A','clickData') ])
def callback_image(clickData=['Canada']):
    
    time.sleep(1)
    

    feature = ['Confirmed']
    if clickData==['Canada']:
        country =['Canada']
    if clickData != ['Canada']:
        country = [clickData['points'][0]['location']]

    mode='group'

    fig = make_subplots(cols=1,rows=2,shared_xaxes=True,vertical_spacing=0.001)



    colors=['red','blue']

    for j in country:
        i = 'Confirmed'
        fig.add_trace(go.Bar(x = Countries.index, y = Countries.diff()[j][i],hovertext=f'{i}<br>in {j}' ,
                             name = f'Daily {i} in {j}',
                            marker_color=colors.pop()),col=1,row=1      )
        fig.update_layout( barmode=mode )

    # for j in country:
    #     fig.add_trace(go.Scatter(x=Countries.index, y = Countries.diff()[j][i].rolling(window=7).mean(),
    #                              mode='markers',
    #                              marker=dict(color='black',
    #                                          size=1),
    #                         hovertext=f'Confirmed cases<br>in {j} ',
    #                         name = f'weekly average of confirmed cases in {j}',
    #                         ))
        
        
    for j in country:
        i = 'Death'
        fig.add_trace(go.Bar(x = Countries.index, y = Countries.diff()[j][i],hovertext=f'{i}<br>in {j}' ,
                             name = f'Daily {i} in {j}',
                            marker_color=colors.pop()),col=1,row=2      )
        fig.update_layout( barmode=mode )

    # for j in country:
    #     fig.add_trace(go.Scatter(x=Countries.index, y = Countries.diff()[j][i].rolling(window=7).mean(),
    #                              mode='markers',
    #                              marker=dict(color='black',
    #                                          size=1),
    #                         hovertext=f'Fatility cases<br>in {j} ',
    #                         name = f'weekly average of fatality cases in {j}',
    #                         ), col=1,row=2 )


    fig.update_layout(
        hovermode='x',
        autosize=True,
        showlegend=False,
        margin=go.layout.Margin(
        l=35, #left margin
        r=0, #right margin
        b=35, #bottom margin
        t=55, #top margin
        )
        )


    fig.update_layout(title_text=f"Confirmed cases (up) and Fatality cases (down) in {country[0]}")
    return fig

if __name__ == "__main__":
    app.run_server()
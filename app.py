import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go
import flask

#from database import fetch_all_bpa_as_df
from database import fetch_all_spotify_as_df

# Definitions of constants. This projects uses extra CSS stylesheet at `./assets/style.css`
COLORS = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)','rgb(67,115,115)']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']

# Define the dash app first
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# for multiplage
def url_bar_and_content_div():
    return html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Define component functions


def page_header():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H3('Visualization with datashader and Plotly')],
                 className="ten columns"),
        html.A([html.Img(id='logo', src=app.get_asset_url('github.png'),
                         style={'height': '35px', 'paddingTop': '7%'}),
                html.Span('1050 project', style={'fontSize': '2rem', 'height': '35px', 'bottom': 0,
                                                'paddingLeft': '4px', 'color': '#a3a7b0',
                                                'textDecoration': 'none'})],
               className="two columns row",
               href='https://github.com/zhiyanwang27/data1050-demo-project-f19'),
    ], className="row")

def page_link():
    """
    Returns the page link as a dash html.Div
    """
    return html.Div(children=[
        html.Div([dcc.Link('Go to About Page', href='/page-1'),]),
        html.Div([dcc.Link('Go to Additional Information Page', href='/page-2')])
    ])

def about_page_layout():
    return html.Div([
        html.H3('About'),
        html.Hr(),
        dcc.Markdown('''
        # **Spotify Top Tracks**
         *A project by Amanda Khoo and Zhiyan Wang for Data 1050*


        **Project Abstract & Executive Summary**  

        Streaming music services are responsible for over half of the music industry’s 2018 revenue [1]. 
        With dozens of music streaming providers, retaining paying subscribers is an important part of Spotify and other streaming services’ business model. 
        Investigating listener trends in the top streamed tracks and aggregation of that data is one potential way to investigate what listeners (in aggregate and over time) 
        are streaming to ensure that new tracks from those genres are available on the platform. Toward this, we have queried two spotify databases to obtain 1) the top 200 
        tracks for a given time period and 2) the genres of the artists performing those tracks. We use merge this data in order to summarize which are the top 
        genres at single day resolution and present an interactive user interface.


        **Datasets**

        The dataset we are using is from spotify charts. The dataset is updated daily to record the top 200 tracks played on spotify from different regions. 
        The dataset recorded the top 200 songs from 2017 up to the current date. The dataset can be accessed via https://spotifycharts.com/regional.
        We are using a python tool for accessing the file information called spotify-chart (https://github.com/fbkarsdorp/spotify-chart). 
        The initial dataset will be acquired on the current date. The dataset will contain ***ranking, track information, artist, url, date, region, 
        streams, number of followers of the artist*** and ***genre*** of the artist. Genre and follower information will be acquired through spotify API and is 
        appended to the dataset as a separate column. 

        We can update the dataset as soon as every day, though the top track on spotify may not change interestingly at that resolution. 
        Thus, choosing an interesting time resolution will be something for us to test and implement capabilities that make sense for deployment 
        (i.e: changes across per month, or per week). 


        **Summary of performance**

        Our website is functional. Users can investigate dates of interest and see how what the top genres are for that day. 
        This required obtaining the genre data and summarizing songs of the same genre into the same category. Additionally, 
        we have created three total pages -- an about us page as well as a project detail page that are linked to the home page. 
        Finally, the shared github repo can be accessed through a link in the top corner. 
        

        **Possible Next Steps**

        Some further directions we could take with exploratory data analysis include: 1) Increasing the geographic resolution of the top tracks -- 
        i.e: *How do the top streamed tracks change in different parts of the country?*,
        2) Enabling the user to change the temporal resolution of the genres vs. streams -- 
        i.e: *How does the top streamed tracks change over longer periods of time?*, and 3) Implementing a world map graph enabling 
        users to identify where the most highly streamed genres can be found in the world. 

        This data could also be used to ask predictive questions. For example, it may be possible to predict what the top ten genres 
        might look like for a particular time period. Additionally, in combination with sound metrics, it may be possible to identify how popular 
        (how many streams) a song might obtain and thus if it makes it into the top 200 most streamed songs. 



        **References**

        [1] https://www.riaa.com/wp-content/uploads/2019/02/RIAA-2018-Year-End-Music-Industry-Revenue-Report.pdf

        [2] https://spotifycharts.com/regional

        [3] https://github.com/fbkarsdorp/spotify-chart
        








        


        ''', className='eleven columns', style={'paddingLeft': '5%'}),
        html.Br(),
        html.Div(id='page-1-content'),
        dcc.Link('Go back to Home', href='/'),
        html.Br(),
        dcc.Link('Go to Additional Information', href='/page-2')
])
def additional_page_layout():
    return html.Div([
        html.H3('Additional Information'),
        html.Hr(),
        dcc.Markdown('''
        # **Spotify Top Tracks**
         *A project by Amanda Khoo and Zhiyan Wang for Data 1050*


        **Development Process and Final Technology Stack**

        We built our project off of the examples given by the teaching staff. Thus, our project uses MongoDB as the database and plot.ly & dash app to create an interactive webpage. Actions on our webpage are also redirected to app.py and the data returned and graphed using plot.ly. 

        The data is acquired as raw and is processed into a pandas DataFrame by the package we’re using called spotify-chart. However, to append the new columns genre and date to this dataframe, we had to request raw data and format it ourselves into a pandas DataFrame. We can then call specific columns of the dataframe for plotting purposes through plot.ly and can interact with those plots using dash.

        **Data Acquisition, Caching, ETL Processing, Database Design**

        The top 200 chart data is first accessed through spotify-chart package and saved into data frame. Genre information is added to the chart by query each song using Spotify API. 
        A token is acquired through spotify API to allow data read. Every song is queried through spotify API to acquire the artist ID and the coreresponding 
        genre information. All of the information is then stored in a pandas DataFrame. Furthermore, dataframe is transformed into MongoDB with Date, SongID and Position as the IDs. 
        Each track is updated if the unique IDs already exists. Otherwise, a new entry will be entered into the database. 

        **Further Information**

        The following links are to ipython notebooks that helped build this website. For better accessibility, right click and open in a new tab. 
        [ETL_EDA.py](https://drive.google.com/open?id=15gAPkK5B4bbGsUZIQwevjQ67kWNfVQ7O) and [Enhancement.py](https://drive.google.com/open?id=1EIzmbXS8eJe-VwTIJJEj1k_9eqtVKbP4)
        

        








        


        ''', className='eleven columns', style={'paddingLeft': '5%'}),
        html.Br(),
        html.Div(id='page-2-content'),
        dcc.Link('Go back to Home', href='/'),
        html.Br(),
        dcc.Link('Go to About Page', href='/page-1')
])

def description():
    """
    Returns overall project description in markdown
    """
    return html.Div(children=[dcc.Markdown('''
        # The Genres of Spotify Top 200 Tracks
        Spotify is one of the most commonly used streaming music services worldwide, 
        with over 217 million paying subscribers. Genre, streaming, user and acoustics data are not only interesting on a user level 
        (i.e: what are my listening habits?), but are extremely lucrative when good suggestion algorithms 
        can satisfy user cravings for new music. Toward this, we thought it might be interesting to see what kind of genre trends exist in top streamed songs using
        Spotify Top 200 Tracks data. This tool could uncover interesting trends with respect to what type of 
        music users like to listen to on spotify in aggregate, rather than on a user by user basis. 

        ### Data Source
        Spotify Top 200 Tracks utilizes near-real-time spotify chart data from [Spotify](https://www.spotify.com/us/).
        The [data source](https://spotifycharts.com/regional) 
        **updates daily**. 
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")


def static_stacked_trend_graph(stack=False):
    """
    Returns scatter line plot of all power sources and power load.
    If `stack` is `True`, the 4 power sources are stacked together to show the overall power
    production.
    """
    #df = fetch_all_bpa_as_df()
    df = fetch_all_spotify_as_df()
    if df is None:
        return go.Figure() #empty figure initialized if no data in df
    genres = df.genre.unique()
    date = df.date.unique()
    date = np.sort(date)
    date = date[-6:]
    df = df[df['date'].between(date[0], date[-1], inclusive = True)]
    #genres = genres[:5]
    #x = df['date']
    fig = go.Figure()
    for i, s in enumerate(genres):
        df_by_genre = df[df['genre'] == s]
        # fig.add_trace(go.Scatter(x=df_by_genre['date'], y=df_by_genre['Streams'], mode='markers', name=s,
        #                          connectgaps=False,
        #                          stackgroup='stack' if stack else None))
        fig.add_trace(go.Box(x = df_by_genre['date'], y = df_by_genre['Streams'], name = s, 
                             marker_color = COLORS[i%5]))
    
   # fig.add_trace(go.Scatter(x=x, y=df['Load'], mode='lines', name='Load',
                           #  line={'width': 2, 'color': 'orange'}))
    title = 'Stream by genre across the week'
    if stack:
        title += ' [Stacked]'

    fig.update_layout(template='plotly_dark',
                      title=title,
                      plot_bgcolor='#23272c',
                      paper_bgcolor='#23272c',
                      yaxis_title='Streams',
                      xaxis_title='Date',
                      boxmode='group')
    return fig
    # sources = ['Wind', 'Hydro', 'Fossil/Biomass', 'Nuclear'] #genres
    # x = df['Datetime'] #we have a simliar one in our dataframe -- rename this as Datetime
    # fig = go.Figure() #initializes the figure 
    # for i, s in enumerate(sources): #trace for every genre
    #     fig.add_trace(go.Scatter(x=x, y=df[s], mode='lines', name=s,
    #                              line={'width': 2, 'color': COLORS[i]}, #counter to do different colors
    #                              stackgroup='stack' if stack else None))
    # fig.add_trace(go.Scatter(x=x, y=df['Load'], mode='lines', name='Load', #we don't need the extra trace
    #                          line={'width': 2, 'color': 'orange'})) 
    # title = 'Energy Production & Consumption under BPA Balancing Authority'
    # if stack:
    #     title += ' [Stacked]' #append a string title to if stack is applied (we can keep this for ours too, stack the genres)
    # fig.update_layout(template='plotly_dark', #figure layout
    #                   title=title,
    #                   plot_bgcolor='#23272c',
    #                   paper_bgcolor='#23272c',
    #                   yaxis_title='MW',
    #                   xaxis_title='Date/Time')
    # return fig


def what_if_description(): #text descriptions
    """
    Returns description of "What-If" - the interactive component
    """
    return html.Div(children=[
        dcc.Markdown('''
        # "What genres are on most streamed on Spotify's Top Tracks?"
        
        It might be interesting to zoom in on particular time points from the graph seen above. 
        Enter one of the dates (yyyy-mm-dd) from the week shown above to check out how songs per genre distribute in the top 200 tracks for that day.

        ''', className='eleven columns', style={'paddingLeft': '5%'})
    ], className="row")


def what_if_tool():
    """
    Returns the What-If tool as a dash `html.Div`. The view is a 8:3 division between
    demand-supply plot and rescale sliders.
    """
    return html.Div(children=[
        html.Div(children=[dcc.Graph(id='what-if-figure')], className='nine columns', style={'marginTop': '5rem'}),

        html.Div(children=[
            html.H5("Rescale Power Supply", style={'marginTop': '2rem'}),
            html.Div(children = [
                dcc.Input(
            id="wind-scale-slider".format("wind-scale-slider"),
            type='text',
            placeholder="input date".format('wind-scale-slider')
            )], style={'marginTop': '3rem'}
            )]),

        html.Div(id='wind-scale-text', className = 'three columns', style={'marginTop': '3rem'})
            
            ])

            # html.Div(children=[
            #     dcc.Slider(id='wind-scale-slider', min=0, max=4, step=0.1, value=2.5, className='row',
            #                marks={x: str(x) for x in np.arange(0, 4.1, 1)})
            # ], style={'marginTop': '5rem'}),

    #         html.Div(id='wind-scale-text', style={'marginTop': '1rem'}),

    #         html.Div(children=[
    #             dcc.Slider(id='hydro-scale-slider', min=0, max=4, step=0.1, value=0,
    #                        className='row', marks={x: str(x) for x in np.arange(0, 4.1, 1)})
    #         ], style={'marginTop': '3rem'}),
    #         html.Div(id='hydro-scale-text', style={'marginTop': '1rem'}),
    #     ], className='three columns', style={'marginLeft': 5, 'marginTop': '10%'}),
    # ], className='row eleven columns')


def architecture_summary():
    """
    Returns the text and image of architecture summary of the project.
    """
    return html.Div(children=[
        dcc.Markdown('''
            # Project Architecture
            This project uses MongoDB as the database. All data acquired are stored in raw form to the
            database (with de-duplication). An abstract layer is built in `database.py` so all queries
            can be done via function call. For a more complicated app, the layer will also be
            responsible for schema consistency. A `plot.ly` & `dash` app is serving this web page
            through. Actions on responsive components on the page is redirected to `app.py` which will
            then update certain components on the page.  
        ''', className='row eleven columns', style={'paddingLeft': '5%'}),

        html.Div(children=[
            html.Img(src="https://docs.google.com/drawings/d/e/2PACX-1vQNerIIsLZU2zMdRhIl3ZZkDMIt7jhE_fjZ6ZxhnJ9bKe1emPcjI92lT5L7aZRYVhJgPZ7EURN0AqRh/pub?w=670&amp;h=457",
                     className='row'),
        ], className='row', style={'textAlign': 'center'}),

        dcc.Markdown('''
        
        ''')
    ], className='row')


# Sequentially add page components to the app's layout
def dynamic_layout():
    return html.Div([
        page_header(),
        page_link(),
        html.Hr(),
        description(),
        # dcc.Graph(id='trend-graph', figure=static_stacked_trend_graph(stack=False)),
        dcc.Graph(id='stacked-trend-graph', figure=static_stacked_trend_graph(stack=True)),
        what_if_description(),
        what_if_tool(),
        architecture_summary(),
    ])

def serve_layout():
    if flask.has_request_context():
        return url_bar_and_content_div()
    return html.Div([
        url_bar_and_content_div(),
        dynamic_layout(),
        about_page_layout(),
        additional_page_layout(),
    ])

# set layout to a function which updates upon reloading
app.layout = serve_layout


# Defines the dependencies of interactive components

@app.callback(
    dash.dependencies.Output('wind-scale-text', 'children'),
    [dash.dependencies.Input('wind-scale-slider', 'value')])
    
def update_wind_sacle_text(value):
   """Changes the display text of the wind slider"""
   return "Date shown: ({})".format(value)


#@app.callback(
#    dash.dependencies.Output('hydro-scale-text', 'children'),
#    [dash.dependencies.Input('hydro-scale-slider', 'value')])

#def update_hydro_sacle_text(value):
#    """Changes the display text of the hydro slider"""
#    return "Hydro Power Scale {:.2f}x".format(value)


@app.callback(
   dash.dependencies.Output('what-if-figure', 'figure'),
   [dash.dependencies.Input('wind-scale-slider', 'value')])
    #dash.dependencies.Input('hydro-scale-slider', 'value')

# #@app.callback(
#     Output('graph-with-slider', 'figure'),
#     [Input('year-slider', 'value')])
    
def what_if_handler(selected_year):
    df = fetch_all_spotify_as_df(allow_cached=True)
    x=df['date']

    filtered_df = df[df.date == selected_year]
    traces = []
    for i in filtered_df.genre.unique():
        df_by_genre = filtered_df[filtered_df['genre'] == i]
        traces.append(dict(
            x=df_by_genre['genre'],
            y=df_by_genre['Streams'],
            type = 'box',
            opacity=0.7,
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'genre',
                   'range':[-1,50]},
            yaxis={'title': 'Streams', 'range': [0, 500000]},
            margin={'l': 50, 'b': 180, 't': 10, 'r': 10},
            showlegend = False,
            hovermode='closest',
            transition = {'duration': 500},
        )
    }
    # supply = df['Wind'] * wind + df['Hydro'] * hydro + df['Fossil/Biomass'] + df['Nuclear']
    # load = df['Load']

    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=x, y=supply, mode='none', name='supply', line={'width': 2, 'color': 'pink'},
    #               fill='tozeroy'))
    # fig.add_trace(go.Scatter(x=x, y=load, mode='none', name='demand', line={'width': 2, 'color': 'orange'},
    #               fill='tonexty'))
    # fig.update_layout(template='plotly_dark', title='Supply/Demand after Power Scaling',
    #                   plot_bgcolor='#23272c', paper_bgcolor='#23272c', yaxis_title='MW',
    #                   xaxis_title='Date/Time')
    return fig


@app.callback( dash.dependencies.Output('page-content', 'children'),
              [ dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/page-1":
        return about_page_layout()
    elif pathname == "/page-2":
        return additional_page_layout()
    else:
        return dynamic_layout()

if __name__ == '__main__':
    app.run_server(debug=True, port=1050, host='0.0.0.0')

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go

from database import fetch_all_bpa_as_df

COLORS = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def static_stacked_trend_graph(stack=False):
    df = fetch_all_bpa_as_df()
    if df is None:
        return go.Figure()
    sources = ['Wind', 'Hydro', 'Fossil/Biomass', 'Nuclear']
    x = df['Datetime']
    fig = go.Figure()
    for i, s in enumerate(sources):
        fig.add_trace(go.Scatter(x=x, y=df[s], mode='lines', name=s,
                                 line={'width': 2, 'color': COLORS[i]},
                                 stackgroup='stack' if stack else None))
    fig.add_trace(go.Scatter(x=x, y=df['Load'], mode='lines', name='Load',
                             line={'width': 2, 'color': 'orange'}))
    title = 'Energy Production & Consumption under BPA Balancing Authority'
    if stack:
        title += ' [Stacked]'

    fig.update_layout(template='plotly_dark',
                      title=title,
                      plot_bgcolor='#23272c',
                      paper_bgcolor='#23272c',
                      yaxis_title='MW',
                      xaxis_title='Date/Time')
    return fig


def page_header():
    return html.Div(id='header', children=[
        html.Div([html.H3('Visualization with datashader and Plotly')],
                 className="ten columns"),
        html.A([html.Img(id='logo', src=app.get_asset_url('github.png'),
                         style={'height': '35px', 'paddingTop': '7%'}),
                html.Span('Blownhither', style={'fontSize': '2rem', 'height': '35px', 'bottom': 0,
                                                'paddingLeft': '4px', 'color': '#a3a7b0',
                                                'textDecoration': 'none'})],
               className="two columns row",
               href='https://github.com/blownhither/'),
    ], className="row")


def description():
    return html.Div(children=[
        dcc.Markdown('''
        # Energy Planner
        As of today, 138 cities in the U.S. have formally announced 100% renewable energy goals or
        targets, while others are actively considering similar goals. Despite ambition and progress,
        conversion towards renewable energy remains challenging.
        
        Wind and solar power are becoming more cost effective, but they will always be unreliable
        and intermittent sources of energy. They follow weather patterns with potential for lots of
        variability. Solar power starts to die away right at sunset, when one of the two daily peaks
        arrives (see orange curve for load).
        
        **Energy Planner is a "What-If" tool to assist making power conversion plans.**
        It can be used to explore load satisfiability under different power contribution with 
        near-real-time energy production & consumption data.
        
        ### Data Source
        Energy Planner utilizes near-real-time energy production & consumption data from [BPA 
        Balancing Authority](https://transmission.bpa.gov/business/operations/Wind/baltwg.aspx).
        The data source **updates every 5 minutes**. 
        ''', className='eleven columns', style={'paddingLeft': '5%'})
    ], className="row")


def what_if_description():
    return html.Div(children=[
        dcc.Markdown('''
        # " What If "
        So far, BPA has been relying on hydro power to balance the demand and supply of power. 
        Could our city survive an outage of hydro power and use up-scaled wind power as an
        alternative? Find below **what would happen with 2.5x wind power and no hydro power at 
        all**.   
        Feel free to try out more combinations with the sliders.  
        ''', className='eleven columns', style={'paddingLeft': '5%'})
    ], className="row")


def what_if_tool():
    return html.Div(children=[
        html.Div(children=[dcc.Graph(id='what-if-figure')], className='nine columns'),

        html.Div(children=[
            html.H5("Rescale Power Supply", style={'marginTop': '2rem'}),
            html.Div(children=[
                dcc.Slider(id='wind-scale-slider', min=0, max=4, step=0.1, value=2.5, className='row',
                           marks={x: str(x) for x in np.arange(0, 4.1, 1)})
            ], style={'marginTop': '5rem'}),

            html.Div(id='wind-scale-text', style={'marginTop': '1rem'}),

            html.Div(children=[
                dcc.Slider(id='hydro-scale-slider', min=0, max=4, step=0.1, value=0,
                           className='row', marks={x: str(x) for x in np.arange(0, 4.1, 1)})
            ], style={'marginTop': '3rem'}),
            html.Div(id='hydro-scale-text', style={'marginTop': '1rem'}),
        ], className='three columns', style={'marginLeft': 5, 'marginTop': '10%'}),
    ], className='row')


app.layout = html.Div([
    page_header(),
    html.Hr(),
    description(),
    # dcc.Graph(id='trend-graph', figure=static_stacked_trend_graph(stack=False)),
    dcc.Graph(id='stacked-trend-graph', figure=static_stacked_trend_graph(stack=True)),
    what_if_description(),
    what_if_tool(),
], className='row', id='content')


@app.callback(
    dash.dependencies.Output('wind-scale-text', 'children'),
    [dash.dependencies.Input('wind-scale-slider', 'value')])
def update_wind_sacle_text(value):
    return f"Wind Power Scale {value:.2f}x"


@app.callback(
    dash.dependencies.Output('hydro-scale-text', 'children'),
    [dash.dependencies.Input('hydro-scale-slider', 'value')])
def update_hydro_sacle_text(value):
    return f"Hydro Power Scale {value:.2f}x"


_what_if_data_cache = None


@app.callback(
    dash.dependencies.Output('what-if-figure', 'figure'),
    [dash.dependencies.Input('wind-scale-slider', 'value'),
     dash.dependencies.Input('hydro-scale-slider', 'value')])
def what_if_handler(wind, hydro):
    global _what_if_data_cache
    if _what_if_data_cache is None:
        _what_if_data_cache = fetch_all_bpa_as_df()
        if _what_if_data_cache is None:
            return go.Figure()

    df = _what_if_data_cache.copy()
    x = df['Datetime']

    supply = df['Wind'] * wind + df['Hydro'] * hydro + df['Fossil/Biomass'] + df['Nuclear']
    load = df['Load']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=supply, mode='none', name='supply', line={'width': 2, 'color': 'pink'},
                  fill='tozeroy'))
    fig.add_trace(go.Scatter(x=x, y=load, mode='none', name='demand', line={'width': 2, 'color': 'orange'},
                  fill='tonexty'))

    fig.update_layout(template='plotly_dark', title='Supply/Demand after Power Scaling',
                      plot_bgcolor='#23272c', paper_bgcolor='#23272c', yaxis_title='MW',
                      xaxis_title='Date/Time')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=5000, host='0.0.0.0')

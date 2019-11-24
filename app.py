import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

from database import fetch_all_bpa_as_df

COLORS = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']


def static_stacked_trend_graph(stack=False):
    df = fetch_all_bpa_as_df()
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
        The data source updates every 5 minutes. 
        ''', className='eleven columns', style={'paddingLeft': '5%'})
    ], className="row")


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    page_header(),
    html.Hr(),
    description(),
    dcc.Graph(id='trend-graph', figure=static_stacked_trend_graph(stack=False)),
    dcc.Graph(id='stacked-trend-graph', figure=static_stacked_trend_graph(stack=True)),
], className='row', id='content')


if __name__ == '__main__':
    app.run_server(debug=True)

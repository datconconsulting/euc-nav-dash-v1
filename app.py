from dash import Dash, html, dash_table, dcc, callback, Output, Input
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate


# -- SOURCE DATA
df1 = pd.read_csv('main.csv')  # US CENSUS DATA
df = pd.read_csv('euc_data.csv')  # VICKIE RAW DATA


tenn = df1['STATE_NAME'] == ' Tennessee'# GET LISTING OF TENNESSEE COUNTIES ONLY.
co = df1['COUNTY'].isin(['Cannon County', 'Clay County', 'Cumberland County', 'Dekalb County', 'Fentress County', 'Jackson County',
                        'Macon County', 'Overton County', 'Pickett County', 'Putnam County', 'Smith County', 'Van Buren County',
                         'Warren County', 'White County'])
tenn1 = df1[tenn & co]

county_options = []
for county in tenn1['COUNTY'].unique():
    county_options.append({'label': str(county), 'value': county})

# DATA FUNCTIONS AND VARIABLES

df[['date']] = df[["Date"]].apply(pd.to_datetime)
df['Year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['month'] = df['month'].astype(str)
df['month'] = df['month'].str.zfill(2)
df = df

rf = df.groupby('County')['Referrals'].count().reset_index()




app = Dash(__name__)
server = app.server

app.layout = html.Div([

            html.Div([
                html.Div([
                    html.Div([
                        html.H3('Empower Upper Cumberland', style = {"margin-bottom": "0px", 'color': 'white'}),
                    ]),
                ], className="six column", id="title"),

            ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

            html.Div([
                dcc.Graph(figure=px.histogram(rf, x=rf['County'], y=rf['Referrals']))
            ], className="create_container twelve columns"),


            html.Div([
                html.Div([

                    html.H3('Select County:', className='fix_label', style={'color': 'grey', 'margin-left': '1%'}),
                    dcc.Dropdown(id='county_dropdown',
                                 options=county_options,
                                 value=tenn1['COUNTY'].min()),

                    html.Br([]),
                    html.H5('Summary', style={'color': 'orange'}),
                    html.Hr(),
                    html.P(id="population", style={'color': 'orange'}),
                    html.P(id="households", style={'color': 'orange'}),
                    html.P(id="families", style={'color': 'orange'}),
                    html.P(id="snap", style={'color': 'orange'}),

                ], className="create_container four columns"),

                html.Div([
                    dcc.Graph(id='map_1',
                              config={'displayModeBar': 'hover'}),

                ], className="create_container 8 columns"),
            ], className="row flex-display"),

            html.Div([

                html.Div([
                    dcc.Graph(id='graph',
                              config = {'displayModeBar': 'hover'}),

                ], className="create_container 2 columns"),

                html.Div([
                    dcc.Graph(id='graph2'),

                ], className="create_container 2 columns"),

                html.Div([
                    dcc.Graph(id='graph3'),

                ], className="create_container 2 columns"),

                html.Div([
                    dcc.Graph(id='graph4'),

                ], className="create_container 2 columns"),

            ], className="row flex-display"),


], id="mainContainer", style={"display": "flex", "flex-direction": "column"})



@callback(
    Output('population', 'children'),
    Input('county_dropdown', 'value'))
def get_county(selected_county):
    tenn = df1[df1['STATE_NAME'] == ' Tennessee']
    population = tenn[tenn['COUNTY'] == selected_county]
    pop = population['POPULATION'].sum()
    return html.P('Population: {:,}'.format(pop))


@callback(Output('households', 'children'),
    Input('county_dropdown', 'value'))
def get_household_value(selected_county):
    tenn = df1[df1['STATE_NAME'] == ' Tennessee']
    filtered = tenn[tenn['COUNTY'] == selected_county]
    house = filtered['HOUSEHOLDS'].sum()
    return html.P('Households: {:,}'.format(house))
#
@callback(Output('families', 'children'),
    Input('county_dropdown', 'value'))
def get_family_value(selected_county):
    tenn = df1[df1['STATE_NAME'] == ' Tennessee']
    filtered = tenn[tenn['COUNTY'] == selected_county]
    fam = filtered['FAMILIES'].sum()
    return html.P('Families: {:,}'.format(fam))


@callback(Output('snap', 'children'),
          Input('county_dropdown', 'value'))
def get_snap_value(selected_county):
    tenn = df1[df1['STATE_NAME'] == ' Tennessee']
    filtered = tenn[tenn['COUNTY'] == selected_county]
    snap = filtered['SNAP'].sum()
    return html.P('On SNAP: {:,}'.format(snap))

# -----------------------------------------------------  REFERRALS GRAPH ------------ |
@callback(Output('graph', 'figure'),
    [Input('county_dropdown', 'value')])
def get_referrals(county_dropdown):
    ref = df[df['County'] == county_dropdown]
    mth_order = {'01': 'Jan',
                 '02': 'Feb',
                 '03': 'Mar',
                 '04': 'Apr',
                 '05': 'May',
                 '06': 'Jun',
                 '07': 'Jul',
                 '08': 'Aug',
                 '09': 'Sep',
                 '10': 'Oct',
                 '11': 'Nov',
                 '12': 'Dec'}

    new = ref.groupby('month')['Referrals'].count().reset_index()

    dave = pd.DataFrame(
        {
            'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            'month_desc': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        }
    )

    new['mth'] = new.month.map(mth_order)

    final = dave.merge(new, how='left', on='month').fillna('0')

    if county_dropdown is None:
        raise PreventUpdate
    else:
        month = final['month_desc']
        value = final['Referrals']

    fig = px.bar(final,
                 x=month,
                 y=value)

    return fig

# -----------------------------------------------------  ENROLLMENTS GRAPH ------------ |
@callback(Output('graph2', 'figure'),
    [Input('county_dropdown', 'value')])
def get_referrals(county_dropdown):
    ref = df[df['County'] == county_dropdown]
    mth_order = {'01': 'Jan',
                 '02': 'Feb',
                 '03': 'Mar',
                 '04': 'Apr',
                 '05': 'May',
                 '06': 'Jun',
                 '07': 'Jul',
                 '08': 'Aug',
                 '09': 'Sep',
                 '10': 'Oct',
                 '11': 'Nov',
                 '12': 'Dec'}

    new = ref.groupby('month')['Enrollments'].count().reset_index()

    dave = pd.DataFrame(
        {
            'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            'month_desc': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        }
    )

    new['mth'] = new.month.map(mth_order)

    final = dave.merge(new, how='left', on='month').fillna('0')

    if county_dropdown is None:
        raise PreventUpdate
    else:
        month = final['month_desc']
        value = final['Enrollments']

    fig = px.bar(final, x=month, y=value)

    return fig


# -----------------------------------------------------  SERVICES GRAPH ------------ |
@callback(Output('graph3', 'figure'),
    [Input('county_dropdown', 'value')])
def get_referrals(county_dropdown):
    ref = df[df['County'] == county_dropdown]
    mth_order = {'01': 'Jan',
                 '02': 'Feb',
                 '03': 'Mar',
                 '04': 'Apr',
                 '05': 'May',
                 '06': 'Jun',
                 '07': 'Jul',
                 '08': 'Aug',
                 '09': 'Sep',
                 '10': 'Oct',
                 '11': 'Nov',
                 '12': 'Dec'}

    new = ref.groupby('month')['Services'].count().reset_index()

    dave = pd.DataFrame(
        {
            'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            'month_desc': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        }
    )

    new['mth'] = new.month.map(mth_order)

    final = dave.merge(new, how='left', on='month').fillna('0')

    if county_dropdown is None:
        raise PreventUpdate
    else:
        month = final['month_desc']
        value = final['Services']

    fig = px.bar(final, x=month, y=value)

    return fig

# -----------------------------------------------------  SERVICES GRAPH ------------ |
@callback(Output('graph4', 'figure'),
    [Input('county_dropdown', 'value')])
def get_referrals(county_dropdown):
    ref = df[df['County'] == county_dropdown]
    mth_order = {'01': 'Jan',
                 '02': 'Feb',
                 '03': 'Mar',
                 '04': 'Apr',
                 '05': 'May',
                 '06': 'Jun',
                 '07': 'Jul',
                 '08': 'Aug',
                 '09': 'Sep',
                 '10': 'Oct',
                 '11': 'Nov',
                 '12': 'Dec'}

    new = ref.groupby('month')['Payments'].sum().reset_index()

    dave = pd.DataFrame(
        {
            'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            'month_desc': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        }
    )

    new['mth'] = new.month.map(mth_order)

    final = dave.merge(new, how='left', on='month').fillna('0')

    if county_dropdown is None:
        raise PreventUpdate
    else:
        month = final['month_desc']
        value = final['Payments']

    fig = px.bar(final, x=month, y=value)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)




#----  WORKING CODE
#
#
# from dash import Dash, html, dash_table, dcc, callback, Output, Input
# from dash import html
# from dash import dcc
# from dash.dependencies import Input, Output
# import plotly.graph_objs as go
# import plotly.express as px
# import pandas as pd
# from dash.exceptions import PreventUpdate
#
#
# # -- SOURCE DATA
# df1 = pd.read_csv('main.csv')
# df = pd.read_csv('euc_data.csv')
#
# tenn = df1[df1['STATE_NAME'] == 'Tennessee']
# county_dropdown = tenn['COUNTY'].unique()
#
# # dave = pd.DataFrame(
# #     {
# #         'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
# #         'month_desc': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# #     }
# # )
#
# # DATA FUNCTIONS AND VARIABLES
#
# df[['date']] = df[["Date"]].apply(pd.to_datetime)
# df['Year'] = df['date'].dt.year
# df['month'] = df['date'].dt.month
# df['month'] = df['month'].astype(str)
# df['month'] = df['month'].str.zfill(2)
# df = df
#
# rf = df.groupby('County')['Referrals'].count().reset_index()
# # x = rf['County']
# # y = rf['Referrals']
#
# state = df1['STATE_NAME'].unique()
#
#
#
# app = Dash(__name__, )
#
# app.layout = html.Div([
#
#             html.Div([
#                 html.Div([
#                     html.Div([
#                         html.H3('Empower Upper Cumberland', style = {"margin-bottom": "0px", 'color': 'white'}),
#                     ]),
#                 ], className="six column", id="title"),
#
#             ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),
#
#             html.Div([
#                 dcc.Graph(figure=px.histogram(rf, x=rf['County'], y=rf['Referrals']))
#             ], className="create_container 2 columns"),
#
#
#             html.Div([
#                 html.Div([
#                     #html.H3('Select State:', className='fix_label', style={'color': 'white'}),
#                     # dcc.Dropdown(id="state_dropdown",
#                     #              multi=False,
#                     #              clearable=True,
#                     #              disabled=False,
#                     #              style={'display': True},
#                     #              placeholder='Select State',
#                     #              options=[state_tenn], className='dcc_compon'),
#                     #             # options = [{'label': c, 'value': c}
#                     #             #            for c in state_tenn], className = 'dcc_compon'),
#
#                     html.H3('Select County:', className='fix_label', style={'color': 'white', 'margin-left': '1%'}),
#                     dcc.Dropdown(id="county_dropdown",
#                                  multi=False,
#                                  clearable=True,
#                                  disabled=False,
#                                  style={'display': True},
#                                  placeholder='Select County',
#                                  options=[{'label': c, 'value': c} for c in county_dropdown], className='dcc-compon'),
#                     html.Br([]),
#                     html.Hr(),
#                     html.P(id="population", style={'color': 'white'}),
#                     html.P(id="households", style={'color': 'white'}),
#                     html.P(id="families", style={'color': 'white'}),
#                     html.P(id="snap", style={'color': 'white'}),
#
#                 ], className="create_container four columns"),
#
#                 html.Div([
#                     dcc.Graph(id='map_1',
#                               config={'displayModeBar': 'hover'}),
#
#                 ], className="create_container 8 columns"),
#             ], className="row flex-display"),
#
#             html.Div([
#
#                 html.Div([
#                     dcc.Graph(id='graph'),
#
#                 ], className="create_container 2 columns"),
#
#                 html.Div([
#                     dcc.Graph(id='graph2'),
#
#                 ], className="create_container 2 columns"),
#
#                 html.Div([
#                     dcc.Graph(id='trend-payments'),
#
#                 ], className="create_container 2 columns"),
#
#                 html.Div([
#                     dcc.Graph(id='trend-services'),
#
#                 ], className="create_container 2 columns"),
#
#             ], className="row flex-display"),
#
#
# ], id="mainContainer", style={"display": "flex", "flex-direction": "column"})
#
#
# # CREATE CALLBACK TO GET UNIQUE COUNTY NAMES
# # @callback(
# #     Output('county_dropdown', 'options'),
# #     Input('state_dropdown', 'value'), prevent_initial_call=True)
# # def get_county_options(state_dropdown):
# #     filtered_state = df1[df1['STATE_NAME'] == state_dropdown]
# #     return [{'label': i, 'value': i} for i in filtered_state['COUNTY'].unique()]
#
# # CREATE CALLBACK FOR COUNTY DROPDOWN
# @callback(
#     Output('county_dropdown', 'options'),
#     Input('county_dropdown', 'value'), prevent_initial_call=True)
# def get_county_value(county_dropdown):
#     return [k['value'] for k in county_dropdown][0]
#
# @callback(Output('population', 'children'),
#     [Input('county_dropdown', 'value')],
#     [Input('state_dropdown', 'value')])
# def get_population_value(county_dropdown, state_dropdown):
#     filtered_data = df1[df1['STATE_NAME'] == state_dropdown]
#     population = filtered_data[filtered_data['COUNTY'] == county_dropdown]
#     pop = population['POPULATION'].sum()
#     return html.P('Population: {:,}'.format(pop))
#
# @callback(Output('households', 'children'),
#     [Input('county_dropdown', 'value')],
#     [Input('state_dropdown', 'value')])
# def get_population_value(county_dropdown, state_dropdown):
#     filtered_data = df1[df1['STATE_NAME'] == state_dropdown]
#     population = filtered_data[filtered_data['COUNTY'] == county_dropdown]
#     house = population['HOUSEHOLDS'].sum()
#     return html.P('Households: {:,}'.format(house))
#
# @callback(Output('families', 'children'),
#     [Input('county_dropdown', 'value')],
#     [Input('state_dropdown', 'value')])
# def get_population_value(county_dropdown, state_dropdown):
#     filtered_data = df1[df1['STATE_NAME'] == state_dropdown]
#     population = filtered_data[filtered_data['COUNTY'] == county_dropdown]
#     fam = population['FAMILIES'].sum()
#     return html.P('Families: {:,}'.format(fam))
#
# @callback(Output('snap', 'children'),
#     [Input('county_dropdown', 'value')],
#     [Input('state_dropdown', 'value')])
# def get_population_value(county_dropdown, state_dropdown):
#     filtered_data = df1[df1['STATE_NAME'] == state_dropdown]
#     population = filtered_data[filtered_data['COUNTY'] == county_dropdown]
#     snap = population['SNAP'].sum()
#     return html.P('SNAP: {:,}'.format(snap))
#
#
# @callback(Output('graph', 'figure'),
#     [Input('county_dropdown', 'value')])
# def get_referrals(county_dropdown):
#     ref = df[df['County'] == county_dropdown]
#     mth_order = {'01': 'Jan',
#                  '02': 'Feb',
#                  '03': 'Mar',
#                  '04': 'Apr',
#                  '05': 'May',
#                  '06': 'Jun',
#                  '07': 'Jul',
#                  '08': 'Aug',
#                  '09': 'Sep',
#                  '10': 'Oct',
#                  '11': 'Nov',
#                  '12': 'Dec'}
#
#     new = ref.groupby('month')['Referrals'].count().reset_index()
#
#     dave = pd.DataFrame(
#         {
#             'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
#             'month_desc': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#         }
#     )
#
#     new['mth'] = new.month.map(mth_order)
#
#     final = dave.merge(new, how='left', on='month').fillna('0')
#
#     if county_dropdown is None:
#         raise PreventUpdate
#     else:
#         month = final['month_desc']
#         value = final['Referrals']
#
#     fig = px.line(final, x=month, y=value)
#
#     return fig
#
#
# @callback(Output('graph2', 'figure'),
#     [Input('county_dropdown', 'value')])
# def get_referrals(county_dropdown):
#     ref = df[df['County'] == county_dropdown]
#     mth_order = {'01': 'Jan',
#                  '02': 'Feb',
#                  '03': 'Mar',
#                  '04': 'Apr',
#                  '05': 'May',
#                  '06': 'Jun',
#                  '07': 'Jul',
#                  '08': 'Aug',
#                  '09': 'Sep',
#                  '10': 'Oct',
#                  '11': 'Nov',
#                  '12': 'Dec'}
#
#     new = ref.groupby('month')['Enrollments'].count().reset_index()
#
#     dave = pd.DataFrame(
#         {
#             'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
#             'month_desc': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#         }
#     )
#
#     new['mth'] = new.month.map(mth_order)
#
#     final = dave.merge(new, how='left', on='month').fillna('0')
#
#     if county_dropdown is None:
#         raise PreventUpdate
#     else:
#         month = final['month_desc']
#         value = final['Enrollments']
#
#     fig = px.line(final, x=month, y=value)
#
#     return fig
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)

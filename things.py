import dash_bootstrap_components as dbc
from dash import dcc, html
from datetime import date


def drpd(idd):
    return dcc.Dropdown(id=idd,
            options=[{'label': 'Unit 1', 'value': 'one'}, {'label': 'Unit 2', 'value': 'two'}, {'label': 'Unit 3', 'value': 'three'},
            # {'label': 'Unit 4', 'value': 'four'},
             {'label': 'Unit 5', 'value': 'five'}, {'label': 'Unit 6', 'value': 'six'},
         {'label': 'Select Generating Unit', 'value': '8'}
                    ],
            optionHeight=35,                    #height/space between dropdown options
            value='8',                    #dropdown value selected automatically when page loads
            disabled=False,                     #disable dropdown value selection
            multi=False,                        #allow multiple dropdown values to be selected
            searchable=True,                    #allow user-searching of dropdown values
            search_value='',                    #remembers the value searched in dropdown
            placeholder='Please select...',     #gray, default text shown when no option is selected
            clearable=True,                     #allow user to removes the selected value
            style={'width':"100%"}             #use dictionary to define CSS styles of your dropdown
            # className='select_box',           #activate separate CSS document in assets folder
            # persistence=True,                 #remembers dropdown value. Used with persistence_type
            # persistence_type='memory'         #remembers dropdown value selected until...
            )

def datepick(start, idd):
    return dcc.DatePickerRange(
        id=idd,
        min_date_allowed=date(2000, 8, 5),
        max_date_allowed=date(2040, 9, 19),
        initial_visible_month=start,
        end_date=start,
        start_date=date(2019, 10, 19)

    )

def topRow(parameterss):
    return(
        dbc.Row(
            html.Hr(style={'borderWidth': "0.3vh", "width": "25%", "color": "#FFFFFF"})
                        ),
        dbc.Row([
                        
                        dbc.Row([
            dbc.Row(html.H5(children='Pick A Date Range:')),
                            
                        dbc.Col(datepick(date.today(),'dp1')),
                        ]
                        )
                        
                        ], justify='center', style = {  'margin-right': '150px',  'margin-left': '80px'}

                        ),
                        dbc.Row(
            html.Hr(style={'borderWidth': "0.3vh", "width": "25%", "color": "#FFFFFF"})
                        ),
            dbc.Row(html.Hr(style={'borderWidth': "0.3vh", "width": "25%", "color": "#FFFFFF"})),
           
        dbc.Col(
            # headerNamer('R1C1', 'HD2')
        ),
        dbc.Col(
            drpd('my_dropdown')
            # headerNamer('Unit no: 4', 'HD3')
        ),
        dbc.Col(id = 'R1C3', children=[
            
        ]
        ),
        dbc.Col(
            # headerNamer('R1C4', 'HD5')
        [dcc.RadioItems([parameterss['turb_g'], parameterss['gen_g'],
                parameterss['gen_t']], parameterss['gen_g'], id='radiob'),
        dbc.Button('show on chart: ', id='show1')
        ]


        )            
    )

def secondRow():
    return(
        
        dbc.Col(
            # headerNamer('R2C1', 'HD6')
    dbc.Spinner(
                        html.Div(children=[     
          
                        ], id = 'side11')
                         ),

             width=1
        ),
        dbc.Col(
                [
                    dbc.Row(
            html.Hr(style={'borderWidth': "0.3vh", "width": "25%", "color": "#FFFFFF"})
                ),
            dbc.Row(html.H2(id='headerN') , justify='center'),

            dbc.Row(
                dbc.Spinner(
            html.Div(children=[     
                ], id = 'lnch33'))


                
                , justify='center'),
                




                ]
                
            ),
        dbc.Col( 
            # R2C3
             width=1
        )
    )

def thirdRow():
    return(
                    dbc.Row(
        [
            dbc.Col(
                width=4
            ),
            dbc.Col(
                drpd('my_dropdown2'), width=2
            ),
            dbc.Col(
                drpd('my_dropdown3'), width=2
            ),
            dbc.Col(
                width=2
            ),
            dbc.Col(
        dbc.Button('Compare', id='show2')
        
            ),
        ]
    ),
    dbc.Row([
            dbc.Row(html.H5(children='Pick A Date Range:')),
                            
                        dbc.Col(datepick(date.today(),'dp2')),
                        ], style = {  'margin-right': '150px',  'margin-left': '80px'}
                        ),

    dbc.Row(html.H2(id='headerN2') , justify='center'),

                    dbc.Row([
                        dbc.Row([
                            
                        # dbc.Col(datepick(date(2022,10,21),'dp2')),
                        ]
                        ) 
                        
                        ], justify='center'
                        ),
                    dbc.Row(
                        dbc.Spinner(
                    html.Div(children=[     
                        ], id = 'lnch44'))
                        , justify='center')

    )
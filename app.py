
from tokenize import group
from dash import Dash, html, dcc, callback_context
import plotly.express as px
import pandas as pd
from datetime import date
import dash_bootstrap_components as dbc
from dateutil.parser import parse
import numpy as np
from dash.dependencies import Input, Output, State
# from models import setup_db, Unit, GGB, GTB, TGB
from flask_sqlalchemy import SQLAlchemy




app = Dash(__name__)
app.server.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:Mqhe23@localhost/zpckb"


app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app.server)



class Unit(db.Model):
    __tablename__ = 'unit'
    
    unit_id = db.Column(db.Integer, nullable=False, primary_key=True)
    capacityMW = db.Column(db.Integer, nullable=False)
    lastAM = db.Column(db.Date, nullable=False)
    
    def __init__(self, unit_id,capacityMW,lastAM):
        self.unit_id = unit_id
        self.capacityMW = capacityMW
        self.lastAM = lastAM
        
    def json(self):
        return {
            'unit_id':self.unit_id,
            'capacityMW': self.capacityMW,
            'lastAM': self.lastAM
        }
    
    
class GGB(db.Model):
    __tablename__ = 'gen_guide_bearing'
    
    id= db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Numeric, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, unit,value,date):
        self.unit = unit
        self.value = value
        self.date = date
        
    def json(self):
        return {
            'unit':self.unit,
            'value': self.value,
            'date': self.date
        }
    
class GTB(db.Model):
    __tablename__ = 'thrust_bearing'
    
    id= db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Numeric, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, unit,value,date):
        self.unit = unit
        self.value = value
        self.date = date
        
    def json(self):
        return {
            'unit':self.unit,
            'value': self.value,
            'date': self.date
        }
    
class TGB(db.Model):
    __tablename__ = 'turb_guide_bearing'
    
    id= db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Numeric, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, unit,value,date):
        self.unit = unit
        self.value = value
        self.date = date
        
    def json(self):
        return {
            'unit':self.unit,
            'value': self.value,
            'date': self.date
        }
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

def create_df_ggb(val):
    prices_shop = GGB.query.filter_by(unit=1)
#     prices_shop.json()
    p2 = [price_shop.json() for price_shop in prices_shop]
    p3 = pd.DataFrame(p2)
    p3 = p3.set_index('date')
    return p3


def create_df_tgb(val):
    prices_shop = TGB.query.filter_by(unit=val)
#     prices_shop.json()
    p2 = [price_shop.json() for price_shop in prices_shop]
    p3 = pd.DataFrame(p2)
    # print(p3)
    p3 = p3.set_index('date')
    return p3


def create_df_gtb(val):
    prices_shop = GTB.query.filter_by(unit=val)
#     prices_shop.json()
    p2 = [price_shop.json() for price_shop in prices_shop]
    p3 = pd.DataFrame(p2)
    # print(p3)
    p3 = p3.set_index('date')
    return p3

drpd = dcc.Dropdown(id='my_dropdown',
            options=[{'label': 'Unit 1', 'value': '1'}, {'label': 'Unit 2', 'value': '2'}, {'label': 'Unit 3', 'value': '3'},
            {'label': 'Unit 4', 'value': '4'}, {'label': 'Unit 5', 'value': '5'}, {'label': 'Unit 6', 'value': '6'},
            {'label': 'Unit 7', 'value': '7'}, {'label': 'Unit 8', 'value': '8'}
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

# BUILDING THE CHARTS #####################################################################


# BUILDING THE LAYOUTS ################################################################3
def headerNamer(itm, idd):
    return html.Div(children=[html.H1(children=itm)], id=idd)

def datepick(start, idd):
    return dcc.DatePickerRange(
        id=idd,
        min_date_allowed=date(2000, 8, 5),
        max_date_allowed=date(2040, 9, 19),
        initial_visible_month=start,
        end_date=start,
        start_date=date(2020, 10, 19)

    )


def lineChartt(df2, idd):
    # fig = px.line(df2, x="Fruit", y="Amount")
    fig = px.line(df2, x=df2['Date'], y="Gen Thrust Bearing Temperature", title='Generator Thrust Bearing Temperature 2003-2022')

    fig.update_layout(width=1200, height=600,plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)',yaxis=dict(showgrid=False))
    fig.update_traces(line_color='#ff00ff', line_width=1.5)
    return html.Div(className='some1', children=[ 
        dcc.Graph(
        id=idd,
        figure=fig
    )
    ])
def distinc(row):
#     print(row)
    return parse(row["Date"], dayfirst=True)
def dropdowns(vals, dflt, id):
    return html.Div([
    dcc.Dropdown(vals, dflt, id=id),
    html.Div(id='dd-output-container')
])

def fixComps(dfm,sdt,edt):
    # print(dfm)
    mask = (dfm.index > sdt) & (dfm.index < edt)
    dfm = dfm[mask]
    # dfm = dfm.set_index('indexx')
    # dfm = dfm.drop("Date",axis=1)
    return dfm



app.layout = html.Div(

    [
        dbc.Row(
            headerNamer('Proto Data Analytics App ZPC Kariba', 'HD1'), justify='center'
        ),

    dbc.Row(
        [
            
        dbc.Col(
            # headerNamer('R1C1', 'HD2')
        ),
        dbc.Col(
            drpd
            # headerNamer('Unit no: 4', 'HD3')
        ),
        dbc.Col(id = 'R1C3', children=[
            
        ]
        ),
        dbc.Col(
            # headerNamer('R1C4', 'HD5')
        )            
        ], justify='center'
    ),
    dbc.Row(
        [
        
        dbc.Col(
            # headerNamer('R2C1', 'HD6')
             width=1
        ),
        dbc.Col(
                [
                    dbc.Row(headerNamer('Gen Guide Bearing Temperature', 'HD15') , justify='center'),

                    dbc.Row([
                        dbc.Row([
                            
                        dbc.Col(datepick(date(2022,10,21),'dp1')),
                        ]
                        ) 
                        
                        ], justify='center'

                        ),
                    dbc.Row(
                        dbc.Spinner(
                    html.Div(children=[     
                        ], id = 'lnch33'))


                        # lineChartt(df2,'lnch1') 
                        
                        , justify='center')


                ]
                
            ),
        dbc.Col( 
            # R2C3
            # headerNamer('R2C3', 'HD8')
             width=1
        )
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                # headerNamer('R3C1', 'HD9')
            ),
            dbc.Col(
                [
                    dbc.Row(headerNamer('Gen Thrust Bearing Temperatures', 'HD17') , justify='center'),
                    dbc.Row(datepick(date(2022,10,21),'dp2'), justify='center'),
                    dbc.Row(
                         dbc.Spinner(
                        html.Div(children=[     
          
                        ], id = 'lnch22')
                         )
                         , justify='center'),
                    # dbc.Row(headerNamer('R3C2R2', 'HD11'))

                ]
            ),
            dbc.Col(
                # headerNamer('R3C3', 'HD13')
            )
        ]
    ),

        dbc.Row(
        [
            dbc.Col(
                # headerNamer('R4C1', 'HD18')
            ),
            dbc.Col(
                [
                    dbc.Row(headerNamer('Turbine Thrust Bearing Temperatures', 'HD19') , justify='center'),
                    dbc.Row(datepick(date(2022,10,21),'dp5'), justify='center'),
                    dbc.Row(
                    
                         dbc.Spinner(
                        html.Div(children=[     
          
                        ], id = 'lnch44')
                         )
                         , justify='center'),
                    # dbc.Row(headerNamer('R3C2R2', 'HD11'))

                ]
            ),
            dbc.Col(
                # headerNamer('R4C3', 'HD20')
            )
        ]
    )

    ]

)

def updateTGuide(dcp,dstrt,dend):

    dcp = fixComps(dcp,dstrt,dend)
    fig = px.scatter(dcp, x=dcp.index.values, y="value", title='Turbine Guide Bearing Temperature')
    fig.update_layout(width=1200, height=600,plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)',yaxis=dict(showgrid=False))
    fig.update_traces(line_color='#ff00ff', line_width=1.5)
    return         dcc.Graph(
        id='lnch2',
        figure=fig
    )

def updateGuide(dcp,dstrt,dend):

    dcp = fixComps(dcp,dstrt,dend)
    fig = px.scatter(dcp, x=dcp.index.values, y="value", title='Generator Guide Bearing Temperature')
    fig.update_layout(width=1200, height=600,plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)',yaxis=dict(showgrid=False))
    fig.update_traces(line_color='#ff00ff', line_width=1.5)
    return         dcc.Graph(
        id='lnch2',
        figure=fig
    )

def firstupdGGB(dfm):
    # print(dfm) v   
    fig = px.scatter(dfm, x=dfm.index.values, y="value", title='Generator Guide Bearing Temperature')
    fig.update_layout(width=1200, height=600,plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)',yaxis=dict(showgrid=False))
    fig.update_traces(line_color='#ff00ff', line_width=1.5)
    return         dcc.Graph(
        id='lnch2',
        figure=fig
    )

def firstupdTGB(dfm):
    # print(dfm) v   
    fig = px.scatter(dfm, x=dfm.index.values, y="value", title='Turbine Guide Bearing Temperature')
    fig.update_layout(width=1200, height=600,plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)',yaxis=dict(showgrid=False))
    fig.update_traces(line_color='#ff00ff', line_width=1.5)
    return         dcc.Graph(
        id='lnch2',
        figure=fig
    )


def firstupdGTB(dfm):
    fig = px.scatter(dfm, x=dfm.index.values, y="value", title='Generator Thrust Bearing Temperature')
    fig.update_layout(width=1200, height=600,plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)',yaxis=dict(showgrid=False))
    fig.update_traces(line_color='#ff00ff', line_width=1.5)
    return         dcc.Graph(
        id='lnch3',
        figure=fig
    )


def updateGThrust(dcp,dstrt,dend):
    # dcp = df2.copy()
    # print(dcp)
    dcp = fixComps(dcp,dstrt,dend)
    # print(dcp)
    fig = px.scatter(dcp, x=dcp.index.values, y="value", title='Generator Thrust Bearing Temperature')
    fig.update_layout(width=1200, height=600,plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)',yaxis=dict(showgrid=False))
    fig.update_traces(line_color='#ff00ff', line_width=1.5)
    return         dcc.Graph(
        id='lnch3',
        figure=fig
    )


@app.callback(
    [
    Output(component_id='R1C3', component_property='children'),
    Output(component_id='lnch33', component_property='children'),
    Output(component_id='lnch22', component_property='children'),
    Output(component_id='lnch44', component_property='children'),
    ],
        [
        Input(component_id='my_dropdown', component_property='value'),
        Input(component_id='dp2', component_property='start_date'),
        Input(component_id='dp2', component_property='end_date'),
        Input(component_id='dp1', component_property='start_date'),
        Input(component_id='dp1', component_property='end_date'),
        Input(component_id='dp5', component_property='start_date'),
        Input(component_id='dp5', component_property='end_date')
        ],
        prevent_initial_call=True

)

def getUnitData(dval,d2strt,d2end,d1strt,d1end,d3strt,d3end):
    ctx = callback_context
    # print(dval)
    prices_shop = Unit.query.filter_by(unit_id=dval).first()
    dval2 = 'Unit ' + dval + ': Last AM Date:' + prices_shop.json()['lastAM'].strftime('%d/%m/%Y')
    grph2 = None
    grph1 = None
    grph3 = None
    dfggb = create_df_ggb(dval)
    dfgtb = create_df_gtb(dval)
    dftgb = create_df_tgb(dval)

    if ctx.triggered[0]['prop_id'] == 'dp2.start_date' or ctx.triggered[0]['prop_id'] == 'dp2.end_date' or ctx.triggered[0]['prop_id'] == 'dp1.start_date' or ctx.triggered[0]['prop_id'] == 'dp1.end_date' or ctx.triggered[0]['prop_id'] == 'dp5.start_date' or ctx.triggered[0]['prop_id'] == 'dp5.end_date':
        grph2 = updateGThrust(dfgtb,d2strt,d2end)
        grph1 = updateGuide(dfggb,d1strt,d1end)
        grph3 = updateTGuide(dftgb,d3strt,d3end)

        return [headerNamer(dval2, 'HD4'),grph1,grph2, grph3]
    # print(dfggb)

    if grph1 == None:
        grph1 = firstupdGGB(dfggb)
    if grph2 == None:
        grph2 = firstupdGTB(dfgtb)
    if grph3 == None:
        grph3 = firstupdTGB(dftgb)

    return [headerNamer(dval2, 'HD4'),grph1,grph2, grph3]


# RUNNING THE SERVER ############################################################

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(debug=False, host='0.0.0.0',port='8050')

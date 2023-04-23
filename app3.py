
from tokenize import group
from dash import Dash, html, dcc, callback_context, dash_table
import plotly.express as px
import pandas as pd
from datetime import date
import dash_bootstrap_components as dbc
from dateutil.parser import parse
import numpy as np
from dash.dependencies import Input, Output, State
# from models import setup_db, Unit, GGB, GTB, TGB
from flask_sqlalchemy import SQLAlchemy
from things import topRow, drpd, secondRow, thirdRow, datepick

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

def create_df_ggb(val,ndt=False):
    prices_shop = GGB.query.filter_by(unit=val)
#     prices_shop.json()
    p2 = [price_shop.json() for price_shop in prices_shop]
    p3 = pd.DataFrame(p2)
    if ndt is False:
        p3 = p3.set_index('date')
    return p3


def create_df_tgb(val,ndt=False):
    prices_shop = TGB.query.filter_by(unit=val)
#     prices_shop.json()
    p2 = [price_shop.json() for price_shop in prices_shop]
    p3 = pd.DataFrame(p2)

    if ndt == False:
        p3 = p3.set_index('date')
    return p3


def create_df_gtb(val,ndt):
    prices_shop = GTB.query.filter_by(unit=val)
#     prices_shop.json()
    p2 = [price_shop.json() for price_shop in prices_shop]
    p3 = pd.DataFrame(p2)
    if ndt is False:
        p3 = p3.set_index('date')
    return p3


# BUILDING THE CHARTS #####################################################################

def make_table(dfm,s,e):
    dfm = fixComps(dfm,s,e)
    dfm.reset_index(inplace=True)
    dfm = dfm.rename(columns = {'index':'Date', 'value':"Max Temperature"})
    return dash_table.DataTable(dfm.to_dict('records'),
    [{'name':i,'id':i} for i in dfm.columns],
    page_size=20,
    style_data_conditional=[
        {
            'if': {
                'filter_query': '{Max Temperature} > 80',
                'column_id': 'Max Temperature'
            },
            'backgroundColor': 'tomato',
            'color': 'white'
        }
    ]
    )

# BUILDING THE LAYOUTS ################################################################3
def headerNamer(itm, idd,col='none'):
    if col == 'none':
        return html.Div(children=[html.H1(children=itm)], id=idd)
    elif col == 'med':
        return html.Div(children=[html.H1(children=itm, style={'color': '#FFBF00'})], id=idd)
    elif col == 'high':
        return html.Div(children=[html.H1(children=itm, style={'color': 'red'})], id=idd)



def lineChartt(df2, idd):
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
    return parse(row["Date"], dayfirst=True)
def dropdowns(vals, dflt, id):
    return html.Div([
    dcc.Dropdown(vals, dflt, id=id),
    html.Div(id='dd-output-container')
])

def fixComps(dfm,sdt,edt):
    mask = (dfm.index > sdt) & (dfm.index < edt)
    dfm = dfm[mask]

    return dfm

def fixComps2(dfm,sdt,edt):
    # dfm = dfm.set_index('date')
    mask = (dfm.index > sdt) & (dfm.index < edt)
    dfm = dfm[mask]

    return dfm

def makeinfo(u,dfm,dS,dE):
    # print(dfm)
    dfm = fixComps2(dfm,dS,dE)

    dfm = dfm.reset_index()

    patek = [     
        html.H2(u),
          html.H3('Min Temp: '+str(dfm['value'].min()) + ' at: ' +
          dfm.loc[dfm['value'] == dfm['value'].min()].iloc[0]['date'].strftime('%d/%m/%Y')

                    ),
          html.H3('Max Temp: '+str(dfm['value'].max()) + ' at: ' + 
                  dfm.loc[dfm['value'] == dfm['value'].max()].iloc[0]['date'].strftime('%d/%m/%Y')
                   ),
          html.H3('Most common reading: '+str(dfm['value'].mode()[0])),
          html.H3('Mediain reading: '+str(dfm['value'].median())),
                        ]
    return patek

parameterss = {
    'gen_g':'Generator Guide Bearing Temperature',
    'turb_g':'Turbine Guide Bearing Temperature',
    'gen_t':'Generator Thrust Bearing Temperature'
}

app.layout = html.Div(
    [
    dbc.Row(
            headerNamer('Proto Data Analytics App ZPC Kariba', 'HD1'), justify='center'
        ),
            dbc.Row(html.Hr(style={'borderWidth': "0.3vh", "width": "25%", "color": "#FFFFFF"})),

dbc.Tabs(
    [

             
        

    dbc.Tab([
                        
        dbc.Row(
        
            topRow(parameterss)
                       
        , justify='center'
    ),

    dbc.Row(
        
            secondRow()
        
        
    ),
    dbc.Row([
        dbc.Col( 
            # R2C3

dbc.Spinner( 
                        html.Div(id = 'side12')
                         ),
             width=6
        ),
        dbc.Col( 
            # R2C3
 
dbc.Spinner(
                        html.Div(id = 'side22')
                         ),
          width=6, align='right'
        )]
    )
    ,
                        dbc.Row(
                    html.Hr(style={'borderWidth': "0.3vh", "width": "25%", "color": "#FFFFFF"})
                        ),

    dbc.Row(
        dbc.Spinner(
                        html.Div(id = 'side23')
                         ), justify='center'
    )
                                        

],label='Singe Unit Stats'),

    dbc.Tab([
        
        dbc.Row(
        [
            dbc.Col(
                thirdRow()

            )
        ]
    )],label='2Unit Comparison')

    ]

    
)
]
)

def updateGuideComp(dcp,dstrt,dend,valuess):

    dcp = fixComps(dcp,dstrt,dend)
    fig = px.scatter(dcp, x=dcp.index.values, y="value", color='unit', title=valuess)
    fig.update_layout(width=1200, height=600,plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)',yaxis=dict(showgrid=False))
    fig.update_traces(line_color='#ffffff', line_width=1.5)
    return         dcc.Graph(
        id='lnch2',
        figure=fig
    )

def updateGuide(dcp,dstrt,dend,valuess):

    dcp = fixComps(dcp,dstrt,dend)
    fig = px.scatter(dcp, x=dcp.index.values, y="value", title=valuess)
    fig.update_layout(width=1200, height=600,plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)',yaxis=dict(showgrid=False))
    fig.update_traces(line_color='#ffffff', line_width=1.5)
    return         dcc.Graph(
        id='lnch2',
        figure=fig
    )

def firstupdGGB(dfm):
    fig = px.scatter(dfm, x=dfm.index.values, y="value", title='Generator Guide Bearing Temperature')
    fig.update_layout(width=1200, height=600,plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)',yaxis=dict(showgrid=False))
    fig.update_traces(line_color='#ff00ff', line_width=1.5)
    return         dcc.Graph(
        id='lnch2',
        figure=fig
    )

def firstupd(cond,dfm):
    fig = px.scatter(dfm, x=dfm.index.values, y="value", title=cond)
    fig.update_layout(width=1200, height=600,plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)',yaxis=dict(showgrid=False))
    fig.update_traces(line_color='#ff00ff', line_width=1.5)
    return         dcc.Graph(
        id='lnch2',
        figure=fig
    )

def createData(unt,condition):
    # print(unt)
    if condition == parameterss['turb_g']:
        outdf = create_df_tgb(unt,False)
    elif condition == parameterss['gen_g']:
        outdf = create_df_ggb(unt,False)
    elif condition == parameterss['gen_t']:
        outdf = create_df_gtb(unt,False)
    outgrph = firstupd(condition,outdf)
    return outgrph,outdf

def createJustData(unt,condition):
    if condition == parameterss['turb_g']:
        outdf = create_df_tgb(unt,False)
    elif condition == parameterss['gen_g']:
        outdf = create_df_ggb(unt,False)
    elif condition == parameterss['gen_t']:
        outdf = create_df_gtb(unt,False)
    return outdf

vals = {
    'one':1,
    'two':2,
    'three':3,
    'four':4,
    'five':5,
    'six':6
}

@app.callback(
    [
    Output(component_id='lnch44', component_property='children'),
    Output(component_id='headerN2', component_property='children')        
    ],
    [

        Input(component_id='show2', component_property='n_clicks')


    ],
    [
        State(component_id='dp2', component_property='start_date'),
        State(component_id='dp2', component_property='end_date'),
        State(component_id='radiob', component_property='value'),
        State(component_id='my_dropdown2', component_property='value'),
        State(component_id='my_dropdown3', component_property='value')

        
    ],

        prevent_initial_call=True

)
def compareUnits(clck,d1s,d1e,radval,u1,u2):

    dfm1 = createJustData(u1,radval)
    dfm2 = createJustData(u2,radval)
    # print(dfm2)
    frames = [dfm1, dfm2]
  
    dfm3 = pd.concat(frames)
    # print(dfm3)

    grph1 = updateGuideComp(dfm3,d1s,d1e,radval)

    comptxt = [html.H2('comparing unit: ' + str(vals[u1]) + ' with unit: ' + str(vals[u2])),
                html.H3('Parameter: ' + radval)]
    return grph1,comptxt

def numOfDays(date1, date2):
    return (date2-date1).days

@app.callback(
    [
    Output(component_id='R1C3', component_property='children'),
    Output(component_id='lnch33', component_property='children'),
    Output(component_id='side12', component_property='children'),
    Output(component_id='side22', component_property='children'),
    Output(component_id='side23', component_property='children'),
    Output(component_id='headerN', component_property='children'),
    ],
        [
        Input(component_id='my_dropdown', component_property='value'),
        Input(component_id='dp1', component_property='end_date'),
        Input(component_id='show1', component_property='n_clicks'),
        ],
        [
        State(component_id='dp1', component_property='start_date'),

            State(component_id='radiob', component_property='value')],
        prevent_initial_call=True
)

def getUnitData(dval,d1end, btn,d1strt, radval):

    # ctx = callback_context
    prices_shop = Unit.query.filter_by(unit_id=vals[dval]).first()
    amDays = numOfDays(prices_shop.json()['lastAM'],date.today())
    dval2 = 'Unit ' + dval + ': Days Since AM:' + str(amDays)
    # print(prices_shop.json()['lastAM'].strftime('%d/%m/%Y'))

    infos = []

    # if ctx.triggered[0]['prop_id'] == 'dp1.start_date' or ctx.triggered[0]['prop_id'] == 'dp1.end_date':
    for i in parameterss:
        if radval != parameterss[i]:
            dfm = createJustData(dval,parameterss[i])
            # print(parameterss[i])
            infos.append(makeinfo(parameterss[i],dfm,d1strt,d1end))
    dfmm = createJustData(dval,radval)
    grph1 = updateGuide(dfmm,d1strt,d1end,radval)
    
    if amDays < 320:
        return [headerNamer(dval2, 'HD4'),grph1,infos[0],infos[1],make_table(dfmm,d1strt,d1end),radval]
    elif amDays < 365:
        return [headerNamer(dval2, 'HD4','med'),grph1,infos[0],make_table(dfmm,d1strt,d1end),infos[1],radval]
    else:
        return [headerNamer(dval2, 'HD4','high'),grph1,infos[0],make_table(dfmm,d1strt,d1end),infos[1],radval]

    # return [headerNamer(dval2, 'HD4'),grph1,None,None,radval]


# RUNNING THE SERVER ############################################################

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(debug=False, host='0.0.0.0',port='8050')
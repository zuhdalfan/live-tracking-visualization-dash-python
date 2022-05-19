from tkinter.font import names
from turtle import color, width
from dash import Dash, dcc, html, callback_context
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from flask import Flask, request
import json
import plotly
import plotly.graph_objects as go

dataHistory = []
temp = {}
df = None
n_anchor = 0


# dcc.Graph(figure=fig)
server = Flask(__name__)
app = Dash(__name__,server=server)
@server.route('/data', methods=['POST'])
def get_data():
    global dataHistory, df, n_anchor
    data =  request.get_json()
    data = data["POS"]
    # print(data)
    #{'x':1,'y':1,'z':2}
    dataHistory.append([data.get('x'),data.get('y'),data.get('z'),'path',5])
    # print(dataHistory)
    dataHistory[-1][3] = 'live'
    dataHistory[-1][4] = 20

    dataHistory.append([0,0,2,'anchor',10])
    dataHistory.append([8,0,2,'anchor',10])
    dataHistory.append([8,2.4,2,'anchor',10])
    dataHistory.append([0,2.4,2,'anchor',10])

    df = pd.DataFrame(dataHistory,columns=['x','y','z','type','marker-size'])
    

    
    # print(dataHistory)
    # data = pd.DataFrame.from_dict(data, orient='index')
    # data = data.transpose()
    df.x = df.x.astype(float)
    df.y = df.y.astype(float)
    df.z = df.z.astype(float)


    dataHistory.pop(-1)
    dataHistory.pop(-1)
    dataHistory.pop(-1)
    dataHistory.pop(-1)
    # print(df)
    # print(f"{data}")
    # dataHistory = pd.concat([dataHistory,data],ignore_index=True,axis=0)
    # dataHistory = dataHistory.append(data)


    dataHistory[-1][3] = 'path'
    dataHistory[-1][4] = 5

    print(dataHistory)


    # print(temp)
    # print(f">>> success")
    return 'success'


app.layout = html.Div([
    dcc.Graph(
        id='live-graph',
        # animate=True,
        # animation_options={"frame":{"redraw":True},"transition":{"duration":10}}
        # figure=fig
    ),
    dcc.Interval(
            id='graph-update',
            interval=100),
    html.Button('Reset', id='btn-reset', n_clicks=0,style={'marginTop':20, 'marginLeft':20}),
])

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')],
)

def update_graph_scatter(input_data):
    fig = px.scatter(
        df,
        x='x',
        y='y',
        orientation='h',
        range_x=[-2,10],
        range_y=[-2,4],
        width=900,
        height=900,
        color='type',
        size='marker-size')
        
    return fig

@app.callback(Output('btn-reset', 'n_clicks'),
              [Input('btn-reset', 'n_clicks')],
)
def update(reset):
    dataHistory.clear()

if __name__ == '__main__':
    app.run_server(debug=True,port=8033)



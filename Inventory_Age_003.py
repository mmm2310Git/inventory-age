#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Created for uploading to render.com
#dependencies :pandas, dash, plotly and pickle
# import xlwings as xw # Removed after using pickle
import pandas as pd
import dash
from dash import dcc,html
from dash import Dash, dash_table, dcc, html, callback 
from dash.dependencies import Input, Output, State
# import plotly.graph_objs as go
import plotly.express as px 
# from plotly.subplots import make_subplots
import re
import dash_bootstrap_components as dbc
# import numpy as np
import pickle


# In[ ]:


# # Run this cell only once...and comment it. 
# # next cell directly reads df.pickle saved ..
# df = pd.read_excel(io="Inventory_AgeAnalysis16Mar.xlsx", sheet_name="Base Data")
# orig_names = [x for i,x in enumerate(df.columns)]
# cols = [f'c{i}' for i, x in enumerate(df.columns)]
# clist = [[cols[i],orig_names[i]] for i,x in enumerate(cols)]
# cDict = {cols[i]:orig_names[i] for i,x in enumerate(cols)}
# # cDict['c0'] will return 'Inventory Type'
# #replace column Names with 'c0', 'c1' etc
# df.columns = cols
# # print(cols[1])
# # print(orig_names[1])
# # a= list(zip(cols,orig_names))
# # type(a[0])
# df.loc[df['c13'].isna(), 'c13'] = 'N' # Closed
# df.loc[df['c14'].isna(), 'c14'] = 'N' # Cancelled
# df.loc[df['c15'].isna(), 'c15'] = 'N' # On Hold
# df.loc[df['c1'].isna(),'c1']='Desc Missing' #Item Desc
# df.loc[df['c2'].isna(),'c2']='UNPEGGED' # Project
# df.loc[df['c3'].isna(),'c3']='UNPEGGED' #Business Partner
# df.loc[df['c12'].isna(),'c12']='WAS BLANK' #category
# # Replace '/' with '_' in Project and category
# df['c3'] = df['c3'].str.replace('/', '_')
# df['c12'] = df['c12'].str.replace('/', '_')
# # Column C8 is Value in Cr
# df['c8'] = pd.to_numeric(df['c8'])
# df = df.sort_values(by=['c8'], ascending=False)
# #df is as read from Excel file..Before filtering, make a copy
# dff=df.copy()
# print(f"No of Records before filter:{len(dff)=}")
# dff = dff[dff.c13=='N']
# dff = dff[dff.c14=='N']
# dff = dff[dff.c15=='N']
# dff = dff[dff.c4!='L&T HYDROCARBON ENGINEERING LTD.']
# dff = dff.sort_values(by=['c8'], ascending=False)
# df_all = dff
# import pickle
# with open("df.pickle", 'wb') as f:
#     pickle.dump(df,f)
    


# In[ ]:


operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]
# Define function to break filter Query..
def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]
                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part
                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value
    return [None] * 3
#for Passthro : BusinessPartner (c4) = L&T HYDROCARBON ENGINEERING LTD.

# counts, bins = np.histogram(df.c10, bins=range(0, 3000, 60))
# print(f"Length of:{counts=} and {len(bins)=} \n {bins}")
# bins = 0.5 * (bins[:-1] + bins[1:])
# print(bins)

# fighb = px.histogram(dff,x='c10', y='c8',  nbins= 50, color='c5', range_x=xrange, histfunc="sum", text_auto=True )
# fighb.update_layout(bargap=0.1)
# print(fighb)
# fighb.show(renderer='browser')

# SCreen size 1263  x 657 : 1263-593 =    SunBurst 590 x 590 r2c1 = 595 x 595; r2c2 = 668 x 595
# 


# In[ ]:


with open('df.pickle', 'rb') as f:
    df = pickle.load(f)
# fl=open("./dataS.txt","w+")
# fl.write(f"No of rows in record is :{len(df)} \n")
dff = df.copy()
dff = dff[dff.c13=='N']
dff = dff[dff.c14=='N']
dff = dff[dff.c15=='N']
dff = dff[dff.c4!='L&T HYDROCARBON ENGINEERING LTD.']
dff = dff.sort_values(by=['c8'], ascending=False)
df_all = dff.copy()
# fl.write(f"No of rows in record is :{len(dff)} \n")
mTitle = "Inventory Weighted Value-Days Analysis :Data 16-Mar-2023:" # Meeting Title
cData = {}
col2list =['c5','c4','c3','c12','c1','c10','c8','c16']
col2Name ={'c5':'PBU','c4':'Business Partner','c3':'Project', 'c12':'Inv Category',
           'c1':'Item Description','c10':'Days', 'c8':'Value(cr)','c16':'ValDays'}


# print(f"No of Records After filter:{len(dff)=}")

xrange=[0,3000]

exclText="(Excl. OnHold & P'Thro Proj)"
def updateFig(dff):
    
    
    fig = px.sunburst(dff,path=['c11','c5', 'c3','c12'],values='c8',height=590, width=590,maxdepth=2,
                      color_discrete_sequence=['rgba(0,50,102,1)', 'rgba(0,102,0,1)', 'rgba(128,0,128,1)',
                                               'rgba(0,0,0,1)', 'rgba(128,0,0,1)', 'rgba(0,0,204,1)'])
    hover_temp = "<b>%{label}:</b><br><i><b>Total Inv : %{value} Cr</b></i><br>Path:%{id}"
    text_temp = "<b>%{label}<br>%{value:.2f} Cr: %{percentParent}</b>"
    
    fig.data[0]['insidetextorientation'] = 'radial'
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    fig.update_traces(hovertemplate=hover_temp, texttemplate=text_temp)
    #fl.write(f"Fig Generated is ..:\n {fig} \n")
    # fl.write(f"Updatingfig len:{len(dff)=} \n {fig} \n")
    return fig
fig=updateFig(dff)
# fl.write("Fig Updated from Main...\n")

def updateTable(dataT):
    table =dash_table.DataTable(
            #dict(id='a', name='Fixed', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)) 'format' : 'Format(precision=2, scheme=Scheme.fixed)'
            columns=[{'id': c, 'name': col2Name[c], 'type':'numeric', 'format': {'specifier': '.3f'}} if (c== 'c8' or c=='c16') 
                     else {'id': c, 'name': col2Name[c], 'type':'text'} for c in col2list],
            data=dataT,
            style_data={'width': '20px', 'minWidth': '20px',  'maxWidth': '100px',#'maxWidth': 0,
                'overflow': 'hidden','textOverflow': 'ellipsis',},
                #'whiteSpace': 'normal','height': 'auto', 'lineHeight': '15px',},
            style_table={'width':'665px'},
            style_data_conditional=[
                {'if': {'row_index': 'odd'},'backgroundColor': 'rgb(220, 220, 220)',}],
            style_header={'backgroundColor': 'rgb(210, 210, 210)',
                'color': 'black','fontWeight': 'bold',},
            style_cell={'fontFamily': 'Arial','fontSize': '12px','font-weight':'bold',
                'color': 'rgb(0,0,204)','font-style': 'italic'},
            filter_action='native',
            page_size=8,id = 'my_table')
    # fl.write(f"UpdateTable len :{len(dataT)=} \n")
    return table
def make_fighb(a, b, c):
    fighb = px.histogram(dff,x=a, y=b, histfunc="sum", nbins=100, color = c, text_auto=True, height=175,
                         color_discrete_sequence=['rgba(0,50,102,1)', 'rgba(0,102,0,1)', 'rgba(128,0,128,1)',
                                               'rgba(0,0,0,1)', 'rgba(128,0,0,1)', 'rgba(0,0,204,1)'])
    fighb.update_layout(bargap=0.1)
    fighb.update_layout(xaxis_title='', yaxis_title='')
    fighb.update_layout(margin=dict(t=25,r=0,l=0,b=20,pad=0), showlegend=False)
    fighb.update_xaxes(showline=True,linecolor='black', linewidth = 2, mirror=True, automargin=False)
    fighb.update_yaxes(showline=True,linecolor='black', linewidth = 2, mirror=True, automargin=True) 
    fighb.update_layout(xaxis=dict( showgrid=True, gridcolor='navy', gridwidth=1))
    fighb.update_layout(yaxis=dict( showgrid=True, gridcolor='navy', gridwidth=1))
    # fighb.update_coloraxes(colorscale='Hot')
    return fighb   

fighb = make_fighb('c10','c8', 'c11')
table = updateTable(dff[col2list].to_dict('records'))
status= html.Label(id='filter_lable',children="Now showing Data for :", style={'font-size':'14px' })
totalInv = html.P(id='total_inv',children=f"Total Inventory :___ Cr", 
                      style={'font-size':'18px'}                   ) #
lb = html.Br()
userFilter = html.P(id='user_filter',children=f"Filtered Data Inventory :___ Cr", style={'margin':'0'})
pCategory = "All Categories"
horBar = html.Div(dcc.Graph(id='horbar', figure=fighb), style={'margin':'0'} )

def weightedInv():
    invValue = dff.c8.sum()
    valDays = dff.c16.sum()
    weightedDays = valDays/invValue
    return weightedDays

app = dash.Dash(__name__)
server=app.server
app.layout = dbc.Container([    
    dbc.Row([
            dbc.Col(id='r1c1',children=[html.Label(id='lnt_logo', 
                        children=["Larsen & Toubro LIMITED,", html.Br(),"AMN Heavy Engg Complex"])], class_name='r1c1'),
            dbc.Col(id='r1c2',children=[html.Label(id='proj_title', children=mTitle + pCategory)], class_name='r1c2'),
            dbc.Col(id='r1c3',children=[
                dcc.Dropdown(id='status-dropdown',
            options=[
                #html.Span(['Montreal'], style={'color': 'Gold', 'font-size': 20})
                {'label': 'Closed', 'value': 'closed'},
                {'label': html.Span(['Cancelled'], style={'color': 'red', 'font-size': 12}), 'value': 'cancelled'},
                {'label': html.Span(['Running'], style={'color': 'blue', 'font-size': 14}), 'value': 'running'},
                {'label': 'PassThrough', 'value': 'passthro'},
                {'label': 'On Hold', 'value': 'onhold'}],
            value='running')], class_name='r1c3'),], class_name='r1 g-0'),
    dbc.Row([dbc.Col(id='r2c1',children=[ # Add Sunburst
    dcc.Graph(id='sunburst-chart', figure=fig),], class_name='r2c1'),
            dbc.Col(id='r2c2',children=[ # add Datatable
            totalInv, status,  table, userFilter, horBar], class_name='r2c2')],class_name='r2 g-0'),
                ],class_name='container')

@app.callback( #1 to 3
    Output('my_table', 'data'), #Dash DataTable
    Output('filter_lable','children'), # What is being filtered
    Output('total_inv','children'), #Total Inventory
    Output('sunburst-chart','figure'), # SunBurst fig
    Output('user_filter', 'children'), # INventory filtered by user
    Output('proj_title','children'), # Top Title : Description of which type of projects are getting displayed
    Output('horbar','figure'),
    [Input('sunburst-chart', 'clickData'), 
     State('my_table', 'data'),Input('my_table', 'filter_query'),
     Input('status-dropdown','value')])
def update_All(clickData, Data, filter, ddown):
    global dff, cData, col3F, col5F, col1F,col6F, pCategory , df_all
    #fl.write(f"Callback Fired :{dash.callback_context.triggered} \n and \
    #         triggered ID :{dash.callback_context.triggered_id} and {dash.callback_context.triggered[0]['prop_id']}\n")
    if dash.callback_context.triggered_id == None:
        tblData = dff[col2list].to_dict('records')
        filter_lable = 'Now showing Data for : HEIC'
        wd = weightedInv()
        userFilter = f"User Filter Inventory: {dff.c8.sum():.4f} Cr & WeightedDays :{wd:.0f}"
        # fl.write(f"Callback Triggered None (Initialized) \n")
        return tblData, filter_lable, f"Total Inventory: {dff.c8.sum():.4f} Cr & WeightedDays :{wd:.0f}", \
               dash.no_update, userFilter, dash.no_update, dash.no_update 
        pass
    elif dash.callback_context.triggered_id == 'sunburst-chart':
        filter_lable = "Showing..."
        # fl.write(f"Callback Triggered from Sunburst Clickdata\n")
        if clickData is None:
            # fl.write(f"ClickData is None....\n")
            filter_lable = "Now showing Data for : HEIC"
            wd= weightedInv()      
            userFilter = f"User Filter Inventory: {dff.c8.sum():.4f} Cr & WeightedDays :{wd:.0f}"
            return dff[col2list].to_dict('records'),filter_lable , \
            f"Total Inventory: {dff.c8.sum():.4f} Cr & WeightedDays :{wd:.0f}" \
                ,dash.no_update, userFilter, dash.no_update, dash.no_update 
        cData = clickData
        string = cData['points'][0]['id']
        try:
            entry_from = clickData['points'][0]['entry']
        except:
            # fl.write(f"Check Entry :{cData=} \n")
            entry_from=''
            # fl.write(f"ClickData is :{len(dff.to_dict('records'))=}\n")
            filter_lable = "Now showing Data for : HEIC"
            dff = df_all
            #dfp = dfm[dfm['PBU'] == 'HEIC']
            fighb = make_fighb('c10','c8', 'c5')# px.histogram(dff,x='c10', y='c8',  nbins= 50, color='c5', range_x=xrange, histfunc="sum", text_auto=True )
            # fighb.update_layout(bargap=0.1)
            fighb.layout.title.text = "Inventory History :HEIC" + exclText
            # for i in range(len(fighb['data'])):
            #     fighb['data'][i]['x'] = dfp[fighb['data'][i]['name']]
            #     fighb['data'][i]['y'] = dfp['Month']
            wd= weightedInv()     
            userFilter = f"User Filter Inventory: {dff.c8.sum():.4f} Cr & WeightedDays :{wd:.0f}"
            return dff[col2list].to_dict('records'),filter_lable \
            , f"Total Inventory: {dff.c8.sum():.4f} Cr & WeightedDays :{wd:.0f}" \
                ,dash.no_update, userFilter, dash.no_update, fighb
        try:
            current_path = clickData['points'][0]['currentPath']
        except:
            # fl.write(f"Check Current Path :{cData=} \n")
            current_path=''
        #fl.write(f"id is :{string} and Current Path :{current_path} and parent:{clickData['points'][0]['parent']} entered from {clickData['points'][0]['entry']} \n")
        dff = df_all
        strA = str(string)
        c11F=''; c5F='';c3F = '';c12F='';
        if strA.endswith(entry_from):
            #fl.write(f"strA :{strA} ends With {entry_from} \n") 
            strA = strA.replace(entry_from,'')
            if strA.endswith('/'):
                strA= strA[:-1]
            #fl.write(f"Modified StrA :{strA} \n")
        if strA == '':
            #col3F = '';col5F='';col1F='';col6F='';
            c11F=''; c5F='';c3F = '';c12F='';
            dff = df_all
            filter_lable = "Now showing Data for : HEIC"
            # fl.write('StrA is Blank and Now removing filter from col3.. \n')
            userFilter = f"User Filter Inventory: {dff.c8.sum():.4f} Cr"
            tblData = dff[col2list].to_dict('records')
            fighb = make_fighb('c10','c8', 'c5')
            # fighb = px.histogram(dff,x='c10', y='c8',  nbins= 50, color='c5', range_x=xrange, histfunc="sum", text_auto=True )
            # fighb.update_layout(bargap=0.1)
            fighb.layout.title.text = "Inventory History :HEIC" + exclText
            # for i in range(len(fighb['data'])):
            #     fighb['data'][i]['x'] = dfp[fighb['data'][i]['name']]
            #     fighb['data'][i]['y'] = dfp['Month']
            wd= weightedInv()     
            userFilter = f"User Filter Inventory: {dff.c8.sum():.4f} Cr & WeightedDays :{wd:.0f}"
            
            # dfp = dfm[dfm['PBU'] == 'HEIC']
            # fighb.layout.title.text = "Inventory History :HEIC" + exclText
            # for i in range(len(fighb['data'])):
            #     fighb['data'][i]['x'] = dfp[fighb['data'][i]['name']]
            #     fighb['data'][i]['y'] = dfp['Month']
            return tblData, filter_lable, f"Total Inventory: {dff.c8.sum():.4f} Cr & WeightedDays :{wd:.0f} ", \
                dash.no_update, userFilter, mTitle+pCategory, fighb
        else:
            #fl.write(f"strA is:{strA} and type :{type(strA)} \n")    
            matches = [(match.group(), match.start()) for match in re.finditer('/', strA)]
            
            filter_lable = "Showing Data.."
            if len(matches) == 0 :
                c11F = strA[:]
                dff = dff[dff.c11==c11F]
                filter_lable = f"Showing Filtered Data:Cat->{c11F}"
                # dfp = dfm[dfm['PBU'] == col3F]
                wd= weightedInv() 
                fighb = make_fighb('c10','c8', 'c5')
                # fighb = px.histogram(dff,x='c10', y='c8',  nbins= 50, color='c5', range_x=xrange, histfunc="sum", text_auto=True )
                # fighb.update_layout(bargap=0.1)
                fighb.layout.title.text = "Inventory History :" + c11F + exclText
                # for i in range(len(fighb['data'])):
                #     fighb['data'][i]['x'] = dfp[fighb['data'][i]['name']]
                #     fighb['data'][i]['y'] = dfp['Month']
                # fl.write(f"Level 0 :Now showing data of Catg:{c11F} on Sunburst and HorBar \n")
            elif len(matches) == 1 :
                c11F = strA[:matches[0][1]]
                c5F = strA[matches[0][1]+1:]
                dff = dff[dff.c11==c11F]
                dff = dff[dff.c5==c5F]
                wd= weightedInv() 
                #dfp = dfm[dfm['PBU'] == col3F]
                fighb = make_fighb('c10','c8', 'c3')
                # fighb = px.histogram(dff,x='c10', y='c8',  nbins= 50, color='c5', range_x=xrange, histfunc="sum", text_auto=True )
                # fighb.update_layout(bargap=0.1)
                fighb.layout.title.text = "Inventory History :" + c11F +  "->" + c5F +  exclText
                # for i in range(len(fighb['data'])):
                #     fighb['data'][i]['x'] = dfp[fighb['data'][i]['name']]
                #     fighb['data'][i]['y'] = dfp['Month']
                filter_lable = f"Showing Filtered Data:Category:{c11F} ->{c5F}"
                # fl.write(f"Level 1:Now showing data of Catg:{c11F} and  {c5F} \n")
            elif len(matches) == 2:
                c11F = strA[:matches[0][1]]
                c5F = strA[matches[0][1]+1:matches[1][1]]
                c3F = strA[matches[1][1]+1:]
                dff = dff[dff.c11==c11F]
                dff = dff[dff.c5==c5F]
                dff = dff[dff.c3==c3F]
                wd= weightedInv() 
                filter_lable = f"Showing Filtered Data:Category:{c11F} ->{c5F}->{c3F}"
                fighb = make_fighb('c10','c8', 'c12')
                # fighb = px.histogram(dff,x='c10', y='c8',  nbins= 50, color='c5', range_x=xrange, histfunc="sum", text_auto=True )
                # fighb.update_layout(bargap=0.1)
                fighb.layout.title.text = f"Inventory History :{c11F}->{c5F}->{c3F} {exclText}"
                # fl.write(f"Level 2:Now showing data of :{c11F} ->{c5F}->{c3F} \n")
                #print(f"Level 2: Filters Col3:{col3F},col5:{col5F},col1{col1F}")
                #print(f"Filter col3:{col3F},col5:{col5F} and col1:{col1F} dff Len:{len(dff)}\n matches {matches}")
                #strA[matches[0][1]+1:matches[1][1]]
            elif len(matches) == 3:
                c11F = strA[:matches[0][1]]
                c5F = strA[matches[0][1]+1:matches[1][1]]
                c3F = strA[matches[1][1]+1:matches[2][1]]
                c12F = strA[matches[2][1]+1:]
                dff = dff[dff.c11==c11F]
                dff = dff[dff.c5==c5F]
                dff = dff[dff.c3==c3F]
                dff = dff[dff.c12==c12F]
                wd= weightedInv() 
                filter_lable = f"Showing Filtered Data:{c11F} ->{c5F}->{c3F}->{c12F}"
                fighb = make_fighb('c10','c8', 'c12')
                # fighb = px.histogram(dff,x='c10', y='c8',  nbins= 50, color='c5', range_x=xrange, histfunc="sum", text_auto=True )
                # fighb.update_layout(bargap=0.1)
                fighb.layout.title.text = f"Inventory History :{c11F}->{c5F}->{c3F}->{c12F} {exclText}"
                # fl.write(f"Level 3:Now showing data of :{c11F} ->{c5F}->{c3F}->{c12F} \n")

                #print(f"Level 3: Filters Col3:{col3F},col5:{col5F},col1{col1F},col6{col6F}")
                #print(f"Filter col3 on {col3F}, col5 on :{col5F}, and col1 on:{col1F} and col6 on:{col6F}")
            elif len(matches) == 4:
                # Not planned Only 3 Levels
                c11F = strA[:matches[0][1]]
                c5F = strA[matches[0][1]+1:matches[1][1]]
                c3F = strA[matches[1][1]+1:matches[2][1]]
                c12F = strA[matches[2][1]+1:matches[3][1]]
                filter_lable = f"Showing Filtered Data: col1={c11F}, col6={c5F}"
                dff = dff[dff.c11==c11F]
                dff = dff[dff.c5==c5F]
                dff = dff[dff.c3==c3F]
                dff = dff[dff.c12==c12F]
                wd= weightedInv() 
                fighb = make_fighb('c10','c8', 'c12')
                # fighb = px.histogram(dff,x='c10', y='c8',  nbins= 50, color='c5', range_x=xrange, histfunc="sum", text_auto=True )
                # fighb.update_layout(bargap=0.1)
                fighb.layout.title.text = f"Inventory History :{c11F}->{c5F}->{c3F}->{c12F} {exclText}"
                # fl.write(f"Level 4:Cant reach here...(Upto 3 Max..Now showing data of :{c11F} ->{c5F}->{c3F}->{c12F} \n")
                fighb.layout.title.text = "Inventory History :" + c11F + exclText
            dff = dff.sort_values(by=['c8'], ascending=False) 
            tblData = dff[col2list].to_dict('records')
            userFilter = f"User Filter Inventory: {dff.c8.sum():.4f} Cr"
            return tblData, filter_lable, f"Total Inventory: {dff.c8.sum():.4f} Cr & WeightedDays :{wd:.0f}", \
                dash.no_update, userFilter, mTitle+pCategory, fighb
            
    elif dash.callback_context.triggered_id == 'my_table':
            fdf = dff.copy()
            # fl.write(f"Callback for Table data or Filter triggered \n")
            if filter != None:
                #print(f"Entered Filter Query :{filter} and length :{len(filter)} sum :{fdf.c4.sum()}")
                # fl.write(f"Entered with Filter Query :{filter} \n")    
                filtering_expressions = filter.split(' && ')
                #dff = df
                for filter_part in filtering_expressions:
                    col_name, operator, filter_value = split_filter_part(filter_part)
                    if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                        # these operators match pandas series operator method names
                        fdf = fdf.loc[getattr(fdf[col_name], operator)(filter_value)]
                    elif operator == 'contains':
                        fdf = fdf.loc[fdf[col_name].str.contains(filter_value)]
                    elif operator == 'datestartswith':
                        # this is a simplification of the front-end filtering logic,
                        # only works with complete fields in standard format
                        fdf = fdf.loc[fdf[col_name].str.startswith(filter_value)]
                tblData = fdf[col2list].to_dict('records')
                # wd= weightedInv() 
                invValue = fdf.c8.sum()
                valDays = fdf.c16.sum()
                wd = valDays/invValue
                userFilter = f"User Filter Inventory: {fdf.c8.sum():.4f} Cr & WeightedDays :{wd:.0f}"
                return tblData, dash.no_update, f"Total Inventory: {dff.c8.sum():.4f} Cr ", \
                    dash.no_update, userFilter, mTitle+pCategory, dash.no_update
            pass
    elif dash.callback_context.triggered_id =='status-dropdown':
        #print(f"DropDown Callback Fired")
        dff= df.copy()
        if ddown == 'closed':
            #print("Closed Projects")
            dff = dff[dff.c13=='Y']
            dff = dff[dff.c14=='N'] #Cancelled
            dff = dff[dff.c15=='N'] #Hold
            dff = dff[dff.c4!='L&T HYDROCARBON ENGINEERING LTD.']
            df_all = dff.copy()
            pCategory = "Only Closed Projects"
        elif ddown == 'cancelled':
            dff = dff[dff.c13=='N']
            dff = dff[dff.c14=='Y']
            dff = dff[dff.c15=='N']
            dff = dff[dff.c4!='L&T HYDROCARBON ENGINEERING LTD.']
            df_all = dff.copy()
            pCategory = "Only Cancelled Projects"
        elif ddown == 'running':
            dff = dff[dff.c13=='N']
            dff = dff[dff.c14=='N']
            dff = dff[dff.c15=='N']
            dff = dff[dff.c4!='L&T HYDROCARBON ENGINEERING LTD.']
            pCategory = "All Running Projects"
            #print("Only Running Projects")
            df_all = dff.copy()
            pass
        elif ddown == 'passthro':
            dff = dff[dff.c4=='L&T HYDROCARBON ENGINEERING LTD.']
            dff = dff[dff.c13=='N']
            dff = dff[dff.c14=='N']
            dff = dff[dff.c15=='N']
            pCategory = "Only PassThro Projects"
            df_all = dff.copy()
            pass
        elif ddown == 'onhold':
            dff = dff[dff.c13=='N']
            dff = dff[dff.c14=='N']
            dff = dff[dff.c15=='Y']
            dff = dff[dff.c4!='L&T HYDROCARBON ENGINEERING LTD.']
            pCategory = "On Hold Projects"
            df_all = dff.copy()
            pass
        dff = dff.sort_values(by=['c8'], ascending=False)
        fig = updateFig(dff)
        tblData = dff[col2list].to_dict('records')
        userFilter = f"User Filter Inventory: {dff.c8.sum():.4f} Cr"
        wd= weightedInv() 
        fighb = make_fighb('c10','c8', 'c5')
        # fighb = px.histogram(dff,x='c10', y='c8',  nbins= 50, color='c5', range_x=xrange, histfunc="sum", text_auto=True )
        # fighb.update_layout(bargap=0.1)
        fighb.layout.title.text = f"Inventory History :{c11F}->{c5F}->{c3F}->{c12F} {exclText}"
        # fl.write(f"Level 4:Cant reach here...(Upto 3 Max..Now showing data of :{c11F} ->{c5F}->{c3F}->{c12F} \n")
        # fighb.layout.title.text = "Inventory History :" + c11F + exclText
# ADd for figHB here and check below

        return tblData, dash.no_update, f"Total Inventory: {dff.c8.sum():.4f} Cr ", \
            fig, userFilter, mTitle+pCategory, fighb
        pass
    # print(f"Should not reach here !!")
    return dash.no_update, dash.no_update, dash.no_update, \
            dash.no_update, dash.no_update, dash.no_update, dash.no_update
# # Suppress Werkzeug logging output
# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR) 
# app = dash.Dash(__name__)
if __name__ == "__main__":
    app.run_server(port=8888 ,debug=False)
    # app.run(use_reloader=False)

# fl.close()
# print("File Closed and Success !")


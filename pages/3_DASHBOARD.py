import pandas as pd
import streamlit as st 
import os
import numpy as np
import random
import time
from pathlib import Path
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
     page_title= 'ACTIVITY DASHBOARD'
)
# st.write('BEING UPDATED, WILL RETURN AFTER THE NEW BUDGETS')
# st.stop()
cola,colb,colc = st.columns([1,2,1])
cola.write('')
colb.markdown("<h4><b>ACTIVITIES DASHBOARD</b></h4>", unsafe_allow_html=True)
colc.write('')
current_time = time.localtime()
k = time.strftime("%V", current_time)
t = int(k) + 13

cola,colb,colc = st.columns([1,2,1])
cola.write(f'**CALENDAR WEEK IS: {k}**')
colc.write(f'**SURGE WEEK IS: {t}**')
try:
     conn = st.connection('gsheets', type=GSheetsConnection)     
     dfb = conn.read(worksheet='DONE', usecols=list(range(12)), ttl=5)
     dfb = dfb.dropna(how='all')
except:
     st.write(f"**Your network is poor, couldn't connect to the google sheet**")
     st.write(f"**TRY AGAIN WITH BETTER INTERNET**")
     st.stop()
dfb= dfb[['CLUSTER','DISTRICT', 'AREA','ACTIVITY', 'DONE', 'WEEK','FACILITY', 'ID', 'AMOUNT','DATE OF SUBMISSION']].copy()
dfb[['DISTRICT','FACILITY', 'ACTIVITY']]  = dfb[['DISTRICT','FACILITY', 'ACTIVITY']].astype(str)

dfb['DONE'] = pd.to_numeric(dfb['DONE'], errors='coerce')
dfb['ID'] = pd.to_numeric(dfb['ID'], errors='coerce')
# dfb[['DONE','ID']] = dfb[['DONE','ID']].apply(pd.to_numeric, errors='coerce')
dfb = dfb.drop_duplicates(subset = ['ID','DONE','DISTRICT', 'FACILITY', 'ACTIVITY'], keep = 'first')

file = r'PLANNED.csv'
dfa = pd.read_csv(file)

dfa= dfa[['DISTRICT', 'AREA','ACTIVITY', 'PLANNED', 'AMOUNT']]

dfb['WEEK'] = pd.to_numeric(dfb['WEEK'], errors='coerce')

dfb['DISTRICT'] = dfb['DISTRICT'].astype(str)
dfb['AREA'] = dfb['AREA'].astype(str)
dfb['ACTIVITY'] = dfb['ACTIVITY'].astype(str)
dfb['DONE'] = pd.to_numeric(dfb['DONE'], errors = 'coerce')

dfa['DISTRICT'] = dfa['DISTRICT'].astype(str)
dfa['AREA'] = dfa['AREA'].astype(str)
dfa['ACTIVITY'] = dfa['ACTIVITY'].astype(str)
dfa['PLANNED'] = dfa['PLANNED'].astype(int)

st.sidebar.subheader('Filter from here ')
district = st.sidebar.multiselect('Pick a district', dfa['DISTRICT'].unique())

if not district:
    dfa2 = dfa.copy()
    dfb2 = dfb.copy()
else:
    dfa2 = dfa[dfa['DISTRICT'].isin(district)]
    dfb2 = dfb[dfb['DISTRICT'].isin(district)]

#create for district
area = st.sidebar.multiselect('Choose a thematic area', dfa2['AREA'].unique())
if not area:
    dfa3 = dfa2.copy()
    dfb3 = dfb2.copy()
else:
    dfa3 = dfa2[dfa2['AREA'].isin(area)]
    dfb3 = dfb2[dfb2['AREA'].isin(area)]
 
#for facility
activity = st.sidebar.multiselect('Choose an activity', dfa3['ACTIVITY'].unique())

#Filter Week, District, Facility
if not district and not area and not activity:
    filtered_dfa = dfa
    filtered_dfb = dfb
elif not area and not activity:
    filtered_dfa = dfa[dfa['DISTRICT'].isin(district)].copy()
    filtered_dfb = dfb[dfb['DISTRICT'].isin(district)].copy()
elif not district and not activity:
    filtered_dfa = dfa[dfa['AREA'].isin(area)].copy()
    filtered_dfb = dfb[dfb['AREA'].isin(area)].copy()
elif area and activity:
     #
    filtered_dfa = dfa3[dfa3['AREA'].isin(area)& dfa3['ACTIVITY'].isin(activity)].copy()
     #
    filtered_dfb = dfb3[dfb3['AREA'].isin(area)& dfb3['ACTIVITY'].isin(activity)].copy()
elif district and activity:
     #
    filtered_dfa = dfa3[dfa3['DISTRICT'].isin(district)& dfa3['ACTIVITY'].isin(activity)].copy()
     #
    filtered_dfb = dfb3[dfb3['DISTRICT'].isin(district)& dfb3['ACTIVITY'].isin(activity)].copy()
elif district and area:
     #
    filtered_dfa = dfa3[dfa3['DISTRICT'].isin(district)& dfa3['AREA'].isin(area)].copy()
     #
    filtered_dfb = dfb3[dfb3['DISTRICT'].isin(district)& dfb3['AREA'].isin(area)].copy()
elif activity:
    filtered_dfa = dfa3[dfa3['ACTIVITY'].isin(activity)].copy()
    filtered_dfb = dfb3[dfb3['ACTIVITY'].isin(activity)].copy()
else:
    filtered_dfa = dfa3[dfa3['DISTRICT'].isin(district) & dfa3['AREA'].isin(area)&dfa3['ACTIVITY'].isin(activity)].copy()
    filtered_dfb = dfb3[dfb3['DISTRICT'].isin(district) & dfb3['AREA'].isin(area)&dfb3['ACTIVITY'].isin(activity)].copy()
#################################################################################################
cols,cold = st.columns(2)
dist = '.'.join(filtered_dfb['DISTRICT']. unique())
if not district:
    pass
elif len(dist) == 0:
    cols.write(f'**No data for this district**')
else:
    cols.write(f'**You are viewing data for: {dist}**')

ar = '.'.join(filtered_dfb['AREA']. unique())
if len(ar) == 0:
    cold.write(f'**No data for the thematic area(s) chosen**')
elif len(ar)>1:
     pass
elif len(ar)==1:
     cold.write(f'**The data set is filtered by: {ar} thematic area(s)**')

act = '.'.join(filtered_dfb['ACTIVITY']. unique())

if not activity:
    st.write(f'**No specific activity has been chosen**')
elif len(act) == 0:
    st.write(f'**No data for the the activity chosen**')
else:
    st.write(f'**ACTIVITIES INCLUDED ARE: {act}**')

plan = filtered_dfa['PLANNED'].sum()
conducted = filtered_dfb['DONE'].sum()
notdone = plan - conducted
if plan ==0:
     perc =0
else:
    perc = round((conducted/plan)*100)

if conducted>plan:
    st.warning(f"SOMETHING IS WRONG, IT SEEMS ACTIVITIES DONE ARE MORE THAN THOSE THAT WERE PLANNED FOR!!")
     
expe = round(((int(t)-13)/13)*100)  #dividing by 13 weeks coz this Q has 13 weeks
col1,col2,col3,col4,col5 = st.columns(5, gap='large')

# with col1:
#     st.metric(label='**PLANNED**', value=f'{plan:,.0f}')
# with col2:
#     st.metric(label='**CONDUCTED**', value=f'{conducted:,.0f}')
# with col3:
#     st.metric(label='**%-AGE**', value=f'{int(perc)} %')
# with col4:
#     st.metric(label='**EXPECTED**', value=f'{int(expe)} %')
# with col5:
#     st.metric(label='**NOT DONE**', value=f'{notdone:,.0f}')
##################################################################################
filtered_dfa['AMOUNT'] = pd.to_numeric(filtered_dfa['AMOUNT'], errors='coerce')
filt = filtered_dfa[filtered_dfa['AMOUNT']>0].copy()
dfplan = filt.copy()
plana = filt['AMOUNT'].sum()
conducteda = filtered_dfb['AMOUNT'].sum()
dfspent = filtered_dfb.copy()
notdonea = plana - conducteda
pers = int((conducteda/plana)*100)
     
#with st.expander('**CLICK HERE TO SEE EXPENDITURE**'):
col1,col2,col3,col4 = st.columns(4)#,
with col1:
    st.metric(label='**BUDGETED**', value=f'{plana:,.0f}')
with col2:
    st.metric(label='**SPENT**', value=f'{conducteda:,.0f}')
with col3:
    st.metric(label='**%SPENT**', value=f'{pers:,.0f} %')
with col4:
    st.metric(label='**BALANCE**', value=f'{notdonea:,.0f}')

#######################################################################################################
#PIE CHART
#st.divider()
col1, col2,col3 = st.columns([1,4,1])
labels = ['DONE', 'NOT DONE']
# Values
values = [conducted, notdone]
colors = ['blue', 'red']
# Creating the pie chart with specified colors and hole
fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+value', 
                             insidetextorientation='radial', marker=dict(colors=colors), hole=0.4)])

# Updating the layout for better readability
fig.update_traces(textposition='inside', textfont_size=20)
fig.update_layout(title_text='DONE vs NOT DONE', title_x=0.2)

# col1, col2,col3 = st.columns([1,4,1])
# with col2:
#      st.plotly_chart(fig, use_container_width=True)
#############################################################################################
#LINE GRAPH
st.divider()

grouped = filtered_dfb.groupby('WEEK').sum(numeric_only=True).reset_index()
fig2 = px.line(grouped, x='WEEK', y='DONE', title='WEEKLY TRENDS',
               markers=True)

fig2.update_layout(xaxis_title='WEEK', yaxis_title='TOTAL DONE',
                    width=800,  # Set the width of the plot
                     height=400,  # Set the height of the plot
                     xaxis=dict(showline=True, linewidth=1, linecolor='black',tickmode='linear',tick0=25,dtick=1,),  # Show x-axis line
                     yaxis=dict(showline=True, linewidth=1, linecolor='black'))  # Show y-axis line)

st.plotly_chart(fig2, use_container_width=True)
# dists = filtered_dfb['DISTRICT'].unique()
# facys = filtered_dfb['FACILITY'].unique()
# areas = filtered_dfb['AREA'].unique()
dfplan['AMOUNT'] = pd.to_numeric(dfplan['AMOUNT'], errors='coerce')
dfplan = dfplan[dfplan['AMOUNT']>0].copy()

areas = dfplan['AREA'].unique()

for area in areas:
     col1,col2, col3 = st.columns(3)
     col2.markdown(f'<h4><b><u style="color: green;">{area}</u></b></h4>', unsafe_allow_html=True)
     dfplana = dfplan[dfplan['AREA']== area].copy()
     dfspenta = dfspent[dfspent['AREA']== area].copy()
     activities = dfplana['ACTIVITY'].unique()
     
     for activity in activities:
               st.markdown(f'<h4><b><u style="color: red;">{activity}</u></b></h4>', unsafe_allow_html=True) 
               dfplanb = dfplana[dfplana['ACTIVITY']== activity].copy()
               dfspentb = dfspenta[dfspenta['ACTIVITY']== activity].copy()
               districts = dfplanb['DISTRICT'].unique()
               col1, col2, col3,col4 = st.columns(4)
               col1.markdown('**DISTRICT**')
               col2.markdown('**PLANNED**')
               col3.markdown('**SPENT**')
               col4.markdown('**BALANCE**')
               for district in districts:
                    dfplanc = dfplanb[dfplanb['DISTRICT']== district].copy()
                    dfspentc = dfspentb[dfspentb['DISTRICT']== district].copy()
                    try:
                         dfplanc['AMOUNT'] = pd.to_numeric(dfplanc['AMOUNT'], errors='coerce')
                         dfspentc['AMOUNT'] = pd.to_numeric(dfspentc['AMOUNT'], errors='coerce')
                         planc = dfplanc['AMOUNT'].sum()
                         spentc =  dfspentc['AMOUNT'].sum()
                         balc = planc - spentc
                         if balc <0:
                             st.warning('**ERROR**')
                    except:
                         spentc = 0
                         planc = 0
                         balc = 0
                 
                    col1, col2, col3,col4 = st.columns(4)
                    # col1.markdown('**DISTRICT**')
                    # col2.markdown('**PLANNED**')
                    # col3.markdown('**SPENT**')
                    # col4.markdown('**BALANCE**')
                    col1.markdown(f"**{district}**")
                    col2.markdown(f'{planc:,.0f}')
                    col3.markdown(f'{spentc:,.0f}')
                    col4.markdown(f'{balc:,.0f}')
              
                    

# chec = len(dists)

# for ary in areas:
#      allya = filtered_dfb[filtered_dfb['AREA']==ary] 
#      allyf = filtered_dfa[filtered_dfa['AREA']==ary]  
#      if chec>1:
#           st.divider()
#           st.markdown(f'<h4><b><u style="color: green;">DISTRICT PERFORMANCE IN {ary}</u></b></h4>', unsafe_allow_html=True)
#          # st.write(f'**DISTRICT PERFORMANCE IN {ary}**')
#           cola, colb, colc, cold = st.columns([2,1,1,1])
#           cola.write('**DISTRICT**')
#           colb.write('**PLANNED**')
#           colc.write('**DONE**')
#           cold.write('**BALANCE**')
#           for district in dists:
#                ally = allya[allya['DISTRICT']==district]
#                allyp = allyf[allyf['DISTRICT']==district]
#                plan = allyp['PLANNED'].sum()
#                conducted = ally['DONE'].sum()
#                notdone = plan - conducted
#                cola.write(f'**{district}**')
#                colb.write(f'**{plan}**')
#                colc.write(f'**{conducted}**')
#                cold.write(f'**{notdone}**')
#      elif chec==1:
#           st.divider() 
#           disy = ','.join(district)
#           st.markdown(f'<h5><b><u style="color: green;">FACILITY PERFORMANCE IN {ary} ACTIVITIES IN {disy}</u></b></h5>', unsafe_allow_html=True)
#           #st.write(f'**FACILITY PERFORMANCE IN {ary} IN {district}**')
#           st.divider()
#           cola, colb, colc = st.columns([2,1,1])
#           cola.write('**FACILITY**')
#           colc.write('**DONE**')
#           for fact in facys:
#                dists = allya['DISTRICT'].unique()
#                allyg = allya[allya['DISTRICT'].isin(dists)]
#                ally = allyg[allyg['FACILITY']==fact]
#                conducted = ally['DONE'].sum()
#                cola.write(f'**{fact}**')
#                colc.write(f'**{conducted}**')
#      else:
#          pass                 
                          

filtered_dfc= filtered_dfb[['CLUSTER','DISTRICT','FACILITY' ,'AREA','ACTIVITY', 'DONE', 'WEEK', 'AMOUNT','ID','DATE OF SUBMISSION']]
with st.expander(f'**CLICK HERE TO SEE FULL DATA SET**'):
    st.dataframe(filtered_dfc.reset_index(drop=True))
    csv_data = filtered_dfc.to_csv(index=False)
    st.download_button(
                        label=" DOWNLOAD THIS DATA SET",
                        data=csv_data,
                        file_name="ACTIVITIES.csv",
                        mime="text/csv")
    

#!/usr/bin/env python
# coding: utf-8

# # KAUSTAV BORA
# 
# INFO 250
# 
# Cricket T20 analysis

# In[1]:


import numpy as np


# In[2]:


import pandas as pd


# In[3]:


import os


# In[5]:


import chart_studio.plotly as py


# In[6]:


from plotly import tools


# In[17]:


from plotly.offline import init_notebook_mode,iplot
init_notebook_mode(connected=False)


# In[18]:


import plotly.figure_factory as ff


# In[19]:


import plotly.graph_objs as go


# In[20]:


print(os.listdir("/Users/kaustavbora/Desktop/Info250"))


# In[21]:


deliveries = pd.read_csv('/Users/kaustavbora/Desktop/Info250/deliveries.csv')


# In[22]:


matches = pd.read_csv('/Users/kaustavbora/Desktop/Info250/matches.csv')


# In[23]:


#Since umpire3 contains all null values we can omit the column
matches.drop('umpire3',axis = 1, inplace=True)


# MATCHES EVERY SEASON

# In[24]:


matches['season'].value_counts().head(3)


# In[42]:


data = [go.Histogram(x=matches['season'], marker=dict(color='#EB89B5'),opacity=0.75)]
layout = go.Layout(title='Matches In Every Season ',xaxis=dict(title='Season',tickmode='linear'),
                    yaxis=dict(title='Count'),bargap=0.2)

fig = go.Figure(data=data, layout=layout)
iplot(fig)


# The year 2013 has most number of matches.
# May be due to super over (super over occurs when there is a tie in the score)
# 
# Moreover there are 10 teams in 2011, 9 in 2012 and 2013

# Matches Played vs Wins by Each Team

# In[26]:


matches_played=pd.concat([matches['team1'],matches['team2']])
matches_played=matches_played.value_counts().reset_index()
matches_played.columns=['Team','Total Matches']
matches_played['wins']=matches['winner'].value_counts().reset_index()['winner']

matches_played.set_index('Team',inplace=True)


# In[27]:


matches_played.reset_index().head(8)


# In[28]:


win_percentage = round(matches_played['wins']/matches_played['Total Matches'],3)*100
win_percentage.head(3)


# In[29]:


trace1 = go.Bar(x=matches_played.index,y=matches_played['Total Matches'],
                name='Total Matches',opacity=0.4)

trace2 = go.Bar(x=matches_played.index,y=matches_played['wins'],
                name='Matches Won',marker=dict(color='red'),opacity=0.4)

trace3 = go.Bar(x=matches_played.index,
               y=(round(matches_played['wins']/matches_played['Total Matches'],3)*100),
               name='Win Percentage',opacity=0.6,marker=dict(color='gold'))

data = [trace1, trace2, trace3]

layout = go.Layout(title='Match Played, Wins And Win Percentage',xaxis=dict(title='Team'),
                   yaxis=dict(title='Count'),bargap=0.2,bargroupgap=0.1)

fig = go.Figure(data=data, layout=layout)
iplot(fig)


# Mumbai indians have most number of wins with most number of matches
# Lets analyze Win Ratio of teams
# 
# So MI is at top in winning matches
# And KXIP is at last

# Venue of Most Matches

# In[30]:


venue_matches=matches.groupby('venue').count()[['id']].sort_values(by='id',ascending=False).head()
ser = pd.Series(venue_matches['id']) 
ser


# In[31]:


venue_matches=matches.groupby('venue').count()[['id']].reset_index()

data = [{"x": venue_matches['id'],"y": venue_matches['venue'], 
          "marker": {"color": "lightblue", "size": 12},
         "line": {"color": "red","width" : 2,"dash" : 'dash'},
          "mode": "markers+lines", "name": "Women", "type": "scatter"}]

layout = {"title": "Stadiums and Matches", 
          "xaxis": {"title": "Matches Played", }, 
          "yaxis": {"title": "Stadiums"},
          "autosize":False,"width":900,"height":1000,
          "margin": go.layout.Margin(l=340, r=0,b=100,t=100,pad=0)}

fig = go.Figure(data=data, layout=layout)
iplot(fig)


# So Eden Gardens, M Chinnaswamy, Wankhede and Feroz Shah Kotla are statiums with most matches
# 
# Since Moslty eliminators, qualifiers and final of each season was here

# # Favorite Umpire

# In[32]:


ump=pd.concat([matches['umpire1'],matches['umpire2']])
ump=ump.value_counts()
umps=ump.to_frame().reset_index()


# In[33]:


ump.head()


# In[34]:


data = [go.Bar(x=umps['index'],y=umps[0],opacity=0.4)]

layout = go.Layout(title='Umpires in Matches',
                   yaxis=dict(title='Matches'),bargap=0.2)

fig = go.Figure(data=data, layout=layout)
iplot(fig)


# S ravi and HDPK Dhrmasena are most popular umpires in IPL

# Runs per Season

# Average and Total Runs

# In[38]:


batsmen = matches[['id','season']].merge(deliveries, left_on = 'id', right_on = 'match_id', how = 'left').drop('id', axis = 1)
season=batsmen.groupby(['season'])['total_runs'].sum().reset_index()

avgruns_each_season=matches.groupby(['season']).count().id.reset_index()
avgruns_each_season.rename(columns={'id':'matches'},inplace=1)
avgruns_each_season['total_runs']=season['total_runs']
avgruns_each_season['average_runs_per_match']=avgruns_each_season['total_runs']/avgruns_each_season['matches']


# In[39]:


fig = {"data" : [{"x" : season["season"],"y" : season["total_runs"],
                  "name" : "Total Run","marker" : {"color" : "lightblue","size": 12},
                  "line": {"width" : 3},"type" : "scatter","mode" : "lines+markers" },
        
                 {"x" : season["season"],"y" : avgruns_each_season["average_runs_per_match"],
                  "name" : "Average Run","marker" : {"color" : "brown","size": 12},
                  "type" : "scatter","line": {"width" : 3},"mode" : "lines+markers",
                  "xaxis" : "x2","yaxis" : "y2",}],
       
        "layout" : {"title": "Total and Average run per Season",
                    "xaxis2" : {"domain" : [0, 1],"anchor" : "y2",
                    "showticklabels" : False},"margin" : {"b" : 111},
                    "yaxis2" : {"domain" : [.55, 1],"anchor" : "x2","title": "Average Run"},                    
                    "xaxis" : {"domain" : [0, 1],"tickmode":'linear',"title": "Year"},
                    "yaxis" : {"domain" :[0, .45], "title": "Total Run"}}}

iplot(fig)


# In[40]:


avgruns_each_season.sort_values(by='total_runs', ascending=False).head(2)


# We see crest at 2012,2013 years (this is beacuse increase in no. of matches)
# Average runs per match increase over years

# Run Distribution Over Years

# In[43]:


Season_boundaries=batsmen.groupby("season")["batsman_runs"].agg(lambda x: (x==6).sum()).reset_index()
fours=batsmen.groupby("season")["batsman_runs"].agg(lambda x: (x==4).sum()).reset_index()
Season_boundaries=Season_boundaries.merge(fours,left_on='season',right_on='season',how='left')
Season_boundaries=Season_boundaries.rename(columns={'batsman_runs_x':'6"s','batsman_runs_y':'4"s'})


# In[44]:


Season_boundaries['6"s'] = Season_boundaries['6"s']*6
Season_boundaries['4"s'] = Season_boundaries['4"s']*4
Season_boundaries['total_runs'] = season['total_runs']


# In[45]:


trace1 = go.Bar(
    x=Season_boundaries['season'],
    y=Season_boundaries['total_runs']-(Season_boundaries['6"s']+Season_boundaries['4"s']),
    name='Remaining runs',opacity=0.6)

trace2 = go.Bar(
    x=Season_boundaries['season'],
    y=Season_boundaries['4"s'],
    name='Run by 4"s',opacity=0.7)

trace3 = go.Bar(
    x=Season_boundaries['season'],
    y=Season_boundaries['6"s'],
    name='Run by 6"s',opacity=0.7)


data = [trace1, trace2, trace3]
layout = go.Layout(title="Run Distribution per year",barmode='stack',xaxis = dict(tickmode='linear',title="Year"),
                                    yaxis = dict(title= "Run Distribution"))

fig = go.Figure(data=data, layout=layout)
iplot(fig)


# Just slight increase in runs by boundaries over year

# Target of 200 Runs or More

# In[48]:


high_scores=deliveries.groupby(['match_id', 'inning','batting_team','bowling_team'])['total_runs'].sum().reset_index() 
high_scores=high_scores[high_scores['total_runs']>=200]
high_scores.nlargest(10,'total_runs')


#  How many times each Team scored > 200

# In[49]:


high_scores=high_scores.groupby(['inning','batting_team']).count().reset_index()
high_scores.drop(["bowling_team","total_runs"],axis=1,inplace=True)
high_scores.rename(columns={"match_id":"total_times"},inplace=True)

high_scores_1 = high_scores[high_scores['inning']==1]
high_scores_2 = high_scores[high_scores['inning']==2]


# In[50]:


high_scores_1.sort_values(by = 'total_times',ascending=False).head(2)


# In[53]:


trace1 = go.Bar(x=high_scores_1['batting_team'],y=high_scores_1['total_times'],name='Ist Innings')
trace2 = go.Bar(x=high_scores_2['batting_team'],y=high_scores_2['total_times'],name='IInd Innings')

fig = tools.make_subplots(rows=1, cols=2, subplot_titles=('At Ist Innings','At IInd Innings'))

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 2)

iplot(fig)


# RCB followed by CSK are at top in creating targets of score greater than 200
# KXIP and CSK is at top in IInd innings while chasing target

# In[61]:


trace0 = go.Pie(labels=labels, values=slices,
              hoverinfo='label+value')

layout=go.Layout(title='200 score chased ?')
fig = go.Figure(data=[trace0], layout=layout)
iplot(fig)


# its hard to achieve this target only 17 out 100 target > 200 chased successfully

# In[ ]:





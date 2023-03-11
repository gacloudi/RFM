import numpy as np
import math as m
import pandas as pd
import streamlit as st
#from pandas_profiling import ProfileReport
from datetime import datetime, date
import bisect
import plotly.graph_objects as go
#from mlxtend.frequent_patterns import apriori
#from mlxtend.frequent_patterns import association_rules
st.header("RFM Analysis")
st.subheader("About the App")
st.write("*This App performs RFM Analysis.")
st.write("*User need to input excel invoice file and choose appropriate columns")
st.write("*User also need to input threshold days for Active/Inactive Calculation")
st.write("---------------------------")
def fn(x):
    res = True
# using try-except to check for truth value
    try:
      #datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S")
      res = bool(datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S"))
      return datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S").date()

    except ValueError:
      x=x.replace('/','-')
      return datetime.strptime(str(x), "%m-%d-%Y %H:%M").date()
def fn2(x,Amt_quartile):
  
  idx=bisect.bisect(Amt_quartile,x)
  if(idx>4):
    idx=4
  return(idx)
def fn3(x):
  if(x>=4):
   x=1
  elif(x==3):
   x=2
  elif(x==2):
   x=3
  else:
    x=4
  return(x)   
def fn4(x):
  if(x>=48):
   seg='Loyal'
  elif(x>=30 and x<=47):
   seg='Passive'
  elif(x>=11 and x<=29):
   seg='Super Passive'
  else:
   seg='Lost'
  return(seg) 
def fn5(x):
  if(x<=t):
   return('Active')
  else:
    return('InActive')
def fn_v(df1):
  df1['S1']=df1["Segments"].astype(str) +"-"+ df1["Active_Flag"]
  values1=df1.S1.value_counts()
  df_v1=values1.to_frame()
  values2=df1.Segments.value_counts()
  df_v2=values2.to_frame()
  values3=df1.Active_Flag.value_counts()
  df_v3=values3.to_frame()
  fig = go.Figure(
  go.Pie(
  labels = df_v1.index.tolist(),
  values = df_v1['S1'],
  hoverinfo = "label+percent",
  textinfo = "value"
  ))
  fig1 = go.Figure(
  go.Pie(
  labels = df_v2.index.tolist(),
  values = df_v2['Segments'],
  hoverinfo = "label+percent",
  textinfo = "value"
  ))
  fig2 = go.Figure(
  go.Pie(
  labels = df_v3.index.tolist(),
  values = df_v3['Active_Flag'],
  hoverinfo = "label+percent",
  textinfo = "value"
  ))

  st.write("-------------------------")
  
  st.subheader("Segments")
  st.plotly_chart(fig1,use_container_width=True)
  st.write("-------------------------")
  
  st.subheader("Active vs InActive")
  st.plotly_chart(fig2)
  st.write("-------------------------")
  st.subheader("Combination of Active & Segments ")
  st.plotly_chart(fig)
  st.write("-------------------------")

text_file=st.file_uploader("Upload a Invoice file")
st.write("-------------------------")
if text_file is not None:
  df=pd.read_excel(text_file)
  df=df.dropna()
  dd_list=df.columns
  #dd_list=dd_list.append('NA')
  #st.write(df.info)
  st.write("-------------------------")
  cols1,cols2=st.columns(2)
  
  with cols1:
    InvoiceDate = st.selectbox(
    'Select the InvoiceDate Column',
    dd_list)
    InvoiceNo = st.selectbox(
    'Select the InvoiceNo Column',
    dd_list)
    CustomerID = st.selectbox(
    'Select the Customer Column',
    dd_list)
  with cols2:
    Product = st.selectbox(
      'Select the Product Column',
      dd_list)
    Price = st.selectbox(
      'Select the Price Column',
      dd_list)
    Unit = st.selectbox(
      'Select the Unit Column',
      dd_list)
  st.write("-------------------------")
  cv1,cv2=st.columns(2)
  with cv1:
    t=st.number_input("Enter the threshold(in days) for Active Customers",value=15)
  st.write("-------------------------")
  def des(df):
    df[InvoiceDate]=df[InvoiceDate].apply(lambda x:fn(x))
    #st.write("DDD")
    li = list(df[CustomerID].value_counts())
    dc=len(li)
    li2 = list(df[InvoiceNo].value_counts())
    tt=len(li2)
    
    li3 = list(df[Product].value_counts())
    dp=len(li3)
    
    df['trans_amount']=df[Price]*df[Unit]
    df2=df['trans_amount']
    #st.write(df2)
    GMV=df2.sum()
    
    APV=m.ceil(GMV/tt)
    APF=m.ceil(tt/dc)
   
    df=df.groupby(CustomerID).agg(min=(InvoiceDate,'min'),max=(InvoiceDate,'max'))
    df['Diff']=df['max']-df['min']
    df["Diff"] = df["Diff"].dt.days
    ACL=m.ceil(df['Diff'].mean()/30)
    c1,c2=st.columns(2)
    with c1:
      st.write("Distinct Customer:",dc)
      st.write("Total Transaction:",tt)
      st.write("Distinct Products:",dp)
      st.write("GMV:",m.ceil(GMV))
    with c2:
      st.write("Average Customer Lifetime:",ACL)
      st.write("Average Purchase Value:",APV)
      st.write("Average Purchase Frequency:",APF)
      st.write("Customer Lifetime Value:",APV*ACL*APF)

  col1, col2 = st.columns(2)
  #st.write("-------------------------")
  with col1:
    RFM=st.button("   RFM    ")
  with col2:
    Des=st.button("Descriptive Analytics")
  #with col3:
   #MBA=st.button("MBA")
  st.write("-------------------------")
  if RFM:
    df[InvoiceDate]=df[InvoiceDate].apply(lambda x:fn(x))
    df[InvoiceNo]=df[InvoiceNo].apply(lambda x:str(x))
    df[CustomerID]=df[CustomerID].apply(lambda x:int(x))
    #st.write(type(InvoiceDate))
    #st.write(type(Unit))
    df1=df[[CustomerID,Price,Unit,InvoiceDate,InvoiceNo]]
    #st.write(df1)
    #li = list(df.CustomerID.value_counts())
    df1['trans_amount']=df1[Price]*df1[Unit]
    df1=df1.groupby(CustomerID).agg(Total_Amount=('trans_amount', 'sum'), Total_Transaction=(InvoiceNo, 'count'),min=(InvoiceDate,'min'),max=(InvoiceDate,'max'))
    df1['Diff']=df1['max']-df1['min']
    df1['Recency']=date.today() - df1['max']
    df1["Diff"] = df1["Diff"].dt.days
    #st.write(df1['Diff'].mean())
    df1["Recency"] = df1["Recency"].dt.days
    df1.index.rename('A', inplace=True)
    #df1['CustomerID']=df1['CustomerID'].apply(lambda x:int(x))
    df1['Active_Flag']=df1['Recency'].apply(lambda x:fn5(x))
    Amt_quartile=np.quantile(df1['Total_Amount'],[0,0.25,0.5,0.75,1])
    Tra_quartile=np.quantile(df1['Total_Transaction'],[0,0.25,0.5,0.75,1])
    Rec_quartile=np.quantile(df1['Recency'],[0,0.25,0.5,0.75,1])
    df_q=pd.DataFrame(Amt_quartile,columns=['Amt_Quartile'],index=['min','q1','q2','q3','max'])
    df_q['Trans_Quartile']=Tra_quartile
    df_q['Rec_Quartile']=Rec_quartile
    #st.write(df_q)
    df1['r_score']=df1['Recency'].apply(lambda x:fn2(x,Rec_quartile))
    df1['r_score']=df1['r_score'].apply(lambda x:fn3(x))
    df1['f_score']=df1['Total_Transaction'].apply(lambda x:fn2(x,Tra_quartile))
    df1['m_score']=df1['Total_Amount'].apply(lambda x:fn2(x,Amt_quartile))
    df1['rfm_score']=df1['r_score'] * df1['f_score'] * df1['m_score']
    df1['Segments']=df1['rfm_score'].apply(lambda x:fn4(x))
    df1=df1[['Total_Amount','Total_Transaction','Active_Flag','Recency','r_score','f_score','m_score','rfm_score','Segments']]
    st.dataframe(df1)
    fn_v(df1)
  if Des:
    des(df)
    #st.write(type(InvoiceDate))
    #st.write(type(Unit))
  
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
 
df=pd.read_csv('cleaned_data.csv')

def top_revenue(df):
    top_5_revenu=df.sort_values(by='revenue',ascending=False).head(5)
    plt.figure(figsize=(10,6))
    sns.barplot(data=top_5_revenu,x='name',y='revenue',weights=0.1)
    plt.gca().yaxis.set_major_formatter('{x:,.0f}')
    plt.xlabel('Company Name',fontsize=15)
    plt.ylabel('Revenue_(in billions)',fontsize=15)
    plt.xticks(rotation=25,ha='right')
    plt.title('Top 5 Revenue Companies',fontsize=20,fontweight='bold')
    plt.tight_layout()
    plt.savefig('outputs/top_5_revenue.png')
    st.pyplot(plt)
    plt.close()
#########################################################################
def top_profit(df):
    top_5_profit=df.sort_values(by='profit',ascending=False).head(5)
    plt.figure(figsize=(10,6))
    sns.barplot(data=top_5_profit,x='name',y='profit',weights=0.1)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x * 1e-9)}B")) #AI
    plt.xlabel('company name',fontsize=15)
    plt.ylabel('profit_(in billions)',fontsize=15)
    plt.xticks(rotation=25,ha='right')
    plt.title('Top 5 Profit Companies',fontsize=20,fontweight='bold')
    plt.tight_layout()
    plt.savefig('outputs/top_5_profit.png')
    st.pyplot(plt)
    plt.close()
#########################################################################
def companies_by_country(df):
    # print(df.groupby('country')['name']).value_counts()
    count_of_country=df.groupby('country')['name'].count()
    # print(companies_by_country)
    fig,(fig1,fig2)=plt.subplots(1,2,figsize=(10,6))
    sns.countplot(data=df,y='country',order=count_of_country.sort_values(ascending=False).index,ax=fig1)
    fig1.set_title('company counts by country')
    fig1.set_ylabel('Country',fontsize=15)
    fig1.set_xlabel('Number of Companies',fontsize=15)
    fig1.grid(alpha=0.3)
    fig2.pie(count_of_country,labels=count_of_country.index,autopct='%1.0f%%',rotatelabels=True,startangle=90)
    fig2.set_title('Percentage of company counts by country')
    plt.tight_layout()
    fig.savefig('outputs/companies_by_country.png')
    st.pyplot(plt)
    plt.close()
#########################################################################
def company_by_industry(df):
    count_of_industry=df.groupby('industry')['name'].count()
    # print(count_of_industry)
    plt.figure(figsize=(10,6))
    plt.hist(df['industry'],len(count_of_industry),edgecolor='black')
    plt.xticks(rotation=20,ha='right')
    plt.title('company counts by industry')
    plt.xlabel('Industry')
    plt.ylabel('Number of Companies')
    plt.tight_layout()
    plt.savefig('outputs/company_by_industry.png')
    st.pyplot(plt)
    plt.close()
#########################################################################
def average_revenue_profit_by_industry(df):
    column_extraction=df[['industry','revenue','profit']]
    column_extraction=pd.melt(column_extraction,
                            id_vars='industry',
                            value_vars=['revenue','profit'],
                            var_name='financial_metric',
                            value_name='amount')
    grouped=column_extraction.groupby(['industry','financial_metric'])['amount'].mean()
    # print(column_extraction)

    fig=px.bar(grouped.reset_index(),
            x='industry',
            y='amount',
            color='financial_metric',
            barmode='group',)

    fig.update_layout(title=dict(text='Average revenue and profit by industry',x=0.5,
                    font=dict(size=50,family='bold')),
                    legend=dict(x=0.5,y=0.995,orientation='v'),
                    xaxis_title='Industry',
                    yaxis_title='Amount')
    
    fig.update_traces(texttemplate='$%{y:.4~s}B',textposition='outside')
    fig.update_xaxes(title='industry',tickangle=45,showgrid=True)
    fig.write_html('outputs/average_revenue_profit_by_industry.html')

    st.plotly_chart(fig)
    print(type(fig))
#########################################################################
def relationship_between_revenue_and_profit(df):
    fig=px.scatter(df,x='revenue',y='profit',color='industry',trendline='ols')
    fig.update_layout(title=dict(text='relationship revenue and profit by industry',x=0.5,
                        font=dict(size=50,family='bold')),
                        legend=dict(x=1,y=0.995,orientation='v'))

    fig.update_xaxes(title=dict(text='revenue',font=dict(size=20)),
                     type='log',
                     showgrid=True)

    fig.update_yaxes(title=dict(text='profit',font=dict(size=20)),
                     
                     showgrid=True)

    fig.update_layout(margin=dict(t=100),annotations=[dict(text='يوضح هذا الرسم أن هناك علاقة طردية بين الإيرادات والأرباح،<br>'
                 'حيث أن الشركات التي تحقق أرباحاً أكثر تميل إلى الأعلى.<br>'
                 'ويوضح هذا الرسم أن أعلى المجالات أرباحاً هما information technology & finance،<br>'
                 'ومجال retail هو الأعلى من حيث الإيرادات ولكن نسبة الأرباح به قليلة بالنسبة للإيرادات.<br>'
                 'وقد تكون هناك عوامل أخرى تؤثر على الأرباح مثل التكاليف والاستثمارات.',
                                        x=0.15,y=1,yref='paper',xref='paper',
                                        font=dict(size=20,family='bold',color='purple'))])
    st.plotly_chart(fig)
    fig.write_html('outputs/Relationship Revenue vs Profit by Industry.html')
#########################################################################
def relationship_between_employees_and_revenue(df):
    fig=px.scatter(df,x='employees',y='revenue',color='industry',
                hover_name='name',hover_data='industry',size='employees',size_max=30,
                trendline='ols',trendline_scope='overall')

    fig.update_xaxes(type='log',title_text='employees count',showgrid=True)
    fig.update_yaxes(type='log',title_text='revenue',showgrid=True)

    fig.update_layout(title=dict(text='relationship between employees and revenue',x=0.5,
                            font=dict(size=50,family='bold')))

    fig.update_layout(margin=dict(t=60,r=35),annotations=[dict(text='يوضح هذا الرسم أن هناك علاقة طردية بين عدد الموظفين والإيرادات،<br>'
                    'حيث أن الشركات التي لديها عدد أكبر من الموظفين تمثل علي نسبه من الايرادات',
                    x=-0.05,y=1.07,yref='paper',xref='paper',showarrow=False,
                    font=dict(size=20,family='bold',color='purple'))])
    st.plotly_chart(fig)
    fig.write_html('outputs/relationship_between_employees_and_revenue.html')
#########################################################################
def comparison_profit_margin_and_revenu_per_employee(df):

    fig=px.scatter(df,x='revenue_per_employee',y='net_profit',
                color='industry',hover_name='name',
                hover_data=['revenue','profit','country'],size='net_profit',size_max=40)

    fig.update_xaxes(type='log',title_text='Revenue Per Employee',showgrid=True)
    fig.update_yaxes(title_text='Profit Margin %',showgrid=True)

    fig.update_layout(title=dict(text='Profit Margin vs Revenue Per Employee by Industry',x=0.5,
                            font=dict(size=50,family='bold')))

    fig.update_layout(margin=dict(t=150,r=35),
                    annotations=[dict(text='توضح هذه المقارنه ان اغلب الشركات تتركز عند العائد لكل موظف اقل من مليون و تحقق هامش ربح بنسبه %20 <br>'
                    'ويوضح الرسم ان هناك بعض الشركات تحقق عائد  لكل موظف اكبر من 100 مليون و تحقق هامش ربح اقل من %20 <br>' 
                    'و يوجد بعض الشركات التي تحقق قيمه ربح بين 40% / 60% و تحقق عائد لكل موظف اقل من مليون<br>' ,
                    x=0.6,y=1.09,yref='paper',xref='paper',showarrow=False,
                    font=dict(size=20,family='bold',color='purple'))])
    st.plotly_chart(fig)
    fig.write_html('outputs/comparison_profit_margin_and_revenu_per_employee.html')
#########################################################################
def outliers_analysis(df):
    pd.set_option('display.max_rows', None)
    q1=df['net_profit'].quantile(0.25)
    q3=df['net_profit'].quantile(0.75)
    iqr=q3-q1
    lower=q1-1.5*iqr
    upper=q3+1.5*iqr
    outliers=df[(df['net_profit']<lower) | (df['net_profit']>upper)]
    cleaned_data=df[(df['net_profit']>lower) & (df['net_profit']<upper)]

    fig1=px.box(cleaned_data,y='net_profit',x='industry',color='industry',points='all',hover_name='name',hover_data=['revenue','profit','country'])
    fig1.update_layout(title=dict(text='Box plot of net profit by industry',x=0.5,
                                font=dict(size=20,family='bold')))
    fig1.update_yaxes(title_text='Net Profit',showgrid=True)
    fig1.update_xaxes(title_text='Industry',showgrid=True)
    fig1.write_html('outputs/box_plot_net_profit_by_industry.html')
    st.plotly_chart(fig1)

    # Q1=df['revenue_per_employee'].quantile(0.25)
    # Q3=df['revenue_per_employee'].quantile(0.75)
    # IQR=Q3-Q1
    # lower=Q1-1.5*IQR
    # upper=Q3+1.5*IQR
    # outliers2=df[(df['revenue_per_employee']<lower) | (df['revenue_per_employee']>upper)]
    # cleaned_data2=df[(df['revenue_per_employee']>lower) & (df['revenue_per_employee']<upper)]
    # fig2=px.violin(outliers2,x='revenue_per_employee',
##################################################################3######
def additional_business_analysis(df):
# country with highest revenue
    new_data=df.groupby('country')['revenue'].sum().reset_index()
    fig=px.pie(new_data,names='country',values='revenue',title='Country with Highest Revenue',hole=0.3,color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textinfo='percent+label',textposition='inside')
    fig.update_layout(title=dict(text='Country with Highest Revenue',x=0.1,
                                font=dict(size=50,family='bold')))
    fig.write_html('outputs/country_with_highest_revenue.html')
    st.plotly_chart(fig)





comparison_profit_margin_and_revenu_per_employee(df)

relationship_between_employees_and_revenue(df)





 
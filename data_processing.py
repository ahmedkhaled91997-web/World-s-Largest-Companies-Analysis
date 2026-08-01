import numpy as np
import pandas as pd


#  التحقق من البيانات 
def data_examination(data_frame):
    pd.set_option('display.max_rows',None)
    pd.set_option('display.max_columns',None)

    print(data_frame.info())
    print("="*20)
    print(data_frame.describe(include="all").T)
    print("="*20)
    print(data_frame.isnull().sum())
    print("="*20)
    print(data_frame.isnull())
    print("="*20)
    print(data_frame.duplicated().sum())

original=pd.read_csv('data_collection.csv')
copy =original.copy()

# نقل البيانات التي تم ترحيلها  
country_values_in_employees = copy['Employees'].isin(['Taiwan','China','United States'])
copy['Headquarters[note 1]']=np.where(country_values_in_employees,copy['Employees'],copy['Headquarters[note 1]'])
copy['Employees']=np.where(country_values_in_employees,copy['Profit'],copy['Employees'])
copy['Profit']=np.where(country_values_in_employees,copy['Revenue'],copy['Profit'])
copy['Revenue']=np.where(country_values_in_employees,copy['Industry'],copy['Revenue'])
copy['Industry']=np.where(country_values_in_employees,np.nan,copy['Industry'])

erorr_value=copy['Headquarters[note 1]'].isin(['[10]'])
copy['Headquarters[note 1]']=np.where(erorr_value,np.nan,copy['Headquarters[note 1]'])
copy['Employees']=np.where(erorr_value,copy['Profit'],copy['Employees'])
copy['Profit']=np.where(erorr_value,copy['Revenue'],copy['Profit'])
copy['Revenue']=np.where(erorr_value,copy['Industry'],copy['Revenue'])
copy['Industry']=np.where(erorr_value,np.nan,copy['Industry'])

########################################################################################

copy.drop('Unnamed: 0',axis=1,inplace=True)
copy.columns=[col.lower() for col in copy.columns]
copy=copy.rename(columns={'headquarters[note 1]':'country'})


for col in copy.columns:
    copy[col] = copy[col].astype(str).str.strip().replace(r'[",]', '', regex=True)

copy['employees']=copy['employees'].apply(pd.to_numeric,errors='coerce').astype('Int64')
copy['profit']=copy['profit'].apply(pd.to_numeric,errors='coerce').astype('float64')
copy['revenue']=copy['revenue'].apply(pd.to_numeric,errors='coerce').astype('float64')
copy['revenue']=copy['revenue']*1_000_000_000
copy['profit']=copy['profit']*1_000_000_000


copy['country']=copy['country'].ffill()
copy['industry']=copy['industry'].ffill()
copy['profit']=copy['profit'].fillna(copy['profit'].min())

################################################################################

#  انشاء عمود يمثل نسبه الربح
copy['net_profit']=(copy['profit']/copy['revenue']*100).round(2)

#  انشاء عمود يمثل الإيرادات لكل موظف 
copy['revenue_per_employee']=(copy['revenue']/copy['employees']).round(2)


#  قائمه شروط select
list_of_conditions=[(copy['employees']>copy['employees'].mean()),
                    (copy['employees']<copy['employees'].mean())
                    &(copy['employees']>copy['employees'].quantile(0.25)),
                    (copy['employees']<copy['employees'].quantile(0.25)),]
values_list=['large','medium','small ']
#  انشاء عمود يمثل حجم الشركه بناءً علي عدد الموظفين 
copy['company_size']=np.select(list_of_conditions,values_list,default='unknown')

copy.to_csv('cleaned_data.csv',index=False)
data_examination(copy)

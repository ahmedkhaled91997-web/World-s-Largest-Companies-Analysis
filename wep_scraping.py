from bs4 import BeautifulSoup
import pandas as pd
import time
import requests

def main():
    link = "https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue"
    user = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}  
    response = requests.get(link, headers=user)

    print(response)
    response = response.content
    soup = BeautifulSoup(response, "html.parser")
    

    colum=soup.find_all('th',{'scope':'col'})
    data=soup.find('tbody',{'id':'mwKg'}).find_all('tr')[2:]
    get_country=soup.find('tbody',{'id':'mwA6o'}).find_all('tr')[1:]

    index_list=[]

    data_dictionary={colum[1].text.strip():[],
                     colum[2].text.strip():[],
                     colum[3].text.strip():[],
                     colum[6].text.strip():[],
                     colum[4].text.strip():[],
                     colum[5].text.strip():[],}

    for i in range(len(data)):
        print(i)
        indexx=data[i].find_all('th')[0].text.strip()
        time.sleep(2)
        name=data[i].find_all('td')[0].text.strip()
        time.sleep(2)
        industry=data[i].find_all('td')[1].text.strip()
        time.sleep(2)
        revenue=data[i].find_all('td')[2].text.strip()
        time.sleep(2)
        country=data[i].find_all('td')[5].text.strip()
        time.sleep(2)
        profit=data[i].find_all('td')[3].text.strip()
        time.sleep(2)
        employees=data[i].find_all('td')[4].text.strip()
        time.sleep(2)
        
        data_dictionary[colum[1].text.strip()].append(name)
        data_dictionary[colum[2].text.strip()].append(industry)
        data_dictionary[colum[3].text.strip()].append(revenue)
        data_dictionary[colum[6].text.strip()].append(country)
        data_dictionary[colum[4].text.strip()].append(profit)
        data_dictionary[colum[5].text.strip()].append(employees)
        index_list.append(indexx)


    df=pd.DataFrame(data_dictionary,index=index_list)
    df.to_csv('data_collection.csv')
      


main()

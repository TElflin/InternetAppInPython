import requests
from bs4 import BeautifulSoup
import pandas
import datetime


data = requests.get('https://www.money.pl/gielda/gpw/akcje/')
soup = BeautifulSoup(data.text, 'html.parser')
rows = soup.find_all('div', attrs={'role':'rowgroup'})


records =[]
for row in rows:
    firstColumn = row.find('div', attrs={'style': 'text-overflow:ellipsis;overflow:hidden'}).text.replace(u'\xa0', u'').replace(',', '.')
    secondColumn = row.find('div', attrs={'style': 'text-align:right;font-weight:bolder'}).text.replace(u'\xa0', u'').replace(',', '.')
    thirdColumn = row.contents[0].contents[2].text.replace(u'\xa0', u'').replace(',', '.')
    fewColumns = row.find_all('div', attrs={'style': 'text-align:right'})
    forthColumn = fewColumns[0].text.replace(u'\xa0', u'').replace(',', '.')
    fifthColumn = fewColumns[1].text.replace(u'\xa0', u'').replace(',', '.')
    sixthCoulmn = fewColumns[2].text.replace(u'\xa0', u'').replace(',', '.')

    seventhCoulmn = fewColumns[3].text
    seventhCoulmn = seventhCoulmn.replace(u'\xa0', u'').replace(',', '.')

    eighthCoulmn = fewColumns[4].text
    eighthCoulmn = eighthCoulmn.replace(u'\xa0', u'').replace(',', '.')
    records.append((firstColumn, secondColumn, thirdColumn, forthColumn, fifthColumn, sixthCoulmn, seventhCoulmn,
                    eighthCoulmn))

df = pandas.DataFrame(records, columns=['Nazwa', 'Kurs(PLN)', 'Zmiana(%)', 'Otwarcie', 'Min', 'Max', 'Obrot(szt)',
                                    'Obrot(PLN)'])

output_filename = datetime.date.today().strftime('listaAkcji-%Y-%m-%d.csv')
df.to_csv(output_filename, index = False, encoding = 'utf-8')





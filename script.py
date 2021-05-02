#!/env/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams as rc
import seaborn as sns
import requests
from bs4 import BeautifulSoup

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def scrape_data():
    print('Scraping data...')
    url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    print('Scarpe successful...')
    table = soup.find('table', class_='t-chart')
    print('Converting to DataFrame...')
    row_head = table.findAll('th')
    row_data = table.findAll('td')
    thead, cells, rows = [], [], []
    for col_name in row_head:
        thead.append(col_name.string)
    for cell in row_data:
        cells.append(cell.string)
    rows = list(chunks(cells, 13))
    df = pd.DataFrame(rows)
    df.columns = thead
    print('Conversion complete.')
    return df
    
def recent_figs(filename):
    data = scrape_data()
    x1 = data.iloc[0][1:].to_list() # Least recent yield this month
    x2 = data.iloc[-1][1:].to_list() # Most recent yield this month
    y = data.columns[1:].to_list() # Dates
    plt.style.use('seaborn-darkgrid')
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(20,5))
    ax1.plot(x1, y, 'o-', color='green')
    ax1.set_title('Least Recent US Treassury Yield Curves of the Month')
    ax1.set_xlabel('Yield Percentages - Least Recent')
    ax1.set_ylabel('Yield Periods')
    ax2.plot(x2, y, 'o-', color='purple')
    ax2.set_title('Most Recent US Treassury Yield Curves of the Month')
    ax2.set_xlabel('Yield Percentages - Most Recent')
    ax2.set_ylabel('Yield Periods')
    plt.savefig(f'charts/{filename}.png')
    print(f'File {filename}.png saved in charts folder.')

def main():
    recent_figs('recent_figs')

if __name__ == '__main__':
    main()

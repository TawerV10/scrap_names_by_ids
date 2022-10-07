from selenium import webdriver
import pandas as pd
import time
import csv

path = 'data/test_csv.csv'
df = pd.read_csv(path)

lst = []
count = 1
for i in range(0, df.shape[0]):
    cell = df.iloc[i, 0]

    # print(f'{count}. {cell}')
    # count += 1

    lst.append(str(int(cell)))

def get_driver():
    ChromeOptions = webdriver.ChromeOptions()
    ChromeOptions.add_argument('--headless')

    browser = webdriver.Chrome(options=ChromeOptions)

    return browser

def getHandles(user_IDs=None):
    browser = get_driver()

    count = 1
    for user_id in user_IDs:

        url = "https://twitter.com/i/user/" + str(user_id)
        browser.get(url)

        while True:
            if "https://twitter.com/i/user/" not in browser.current_url:
                break

        endingslash = (str(browser.current_url).split("/"))[-1]

        _closeBrowserWindow(browser)

        if endingslash != user_id:
            name = endingslash
            print(f"{count}. {user_id} - {name}")
        else:
            name = None
            print("No username retrieved")

        count += 1

        if name != '404':
            with open('output.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    user_id, f'@{name}'
                ])
        else:
            with open('output.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    user_id, ''
                ])

def _closeBrowserWindow(browser):
    try:
        browser.close
    except:
        print("Couldn't close this headless browser window")

if __name__ == '__main__':
    t0 = time.time()

    print('start')
    with open('output.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'user_id', 'user_name'
        ])

    getHandles(lst[:100])
    print(time.time() - t0)
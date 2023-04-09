import time
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

url = "https://www.bseindia.com/corporates/ann.html"
bsePriceUri = "https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?flag=0&type=ETF"
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
category = "Corp. Action"


def printResult(link, data, fromDate):
    resultarr = []
    resultarr.append(link.text.split("-")[0])
    resultarr.append(link.text.split("-")[1])
    resultarr.append(fromDate)
    firstrec = data[0].split(',')
    resultarr.append(firstrec[0])
    lastrec = data[len(data) - 1].split(',')
    resultarr.append(lastrec[0])
    resultarr.append(firstrec[1])
    resultarr.append(lastrec[4])
    resultarr.append(str(float(lastrec[4]) - float(firstrec[1])))
    resultarr.append(str(((float(lastrec[4]) - float(firstrec[1])) * 100) / float(firstrec[1])))
    resultarr.append(str((((float(lastrec[4]) - float(firstrec[1])) * 100) / float(firstrec[1])) * 100))
    print(",".join(resultarr))


def updateCorpPage(driver, fromDate):
    xpathfordate = "//a[@data-date='{0}']".format(int(fromDate.split('-')[0]))
    txtFromDt = driver.find_element(By.ID, "txtFromDt")
    txtFromDt.click()
    txtFromDtDatePickerMonth = Select(driver.find_element(By.CLASS_NAME, "ui-datepicker-month"))
    txtFromDtDatePickerMonth.select_by_visible_text('Mar')
    driver.find_element(By.XPATH, xpathfordate).click()

    txtToDt = driver.find_element(By.ID, "txtToDt")
    txtToDt.click()
    txtToDtDatePickerMonth = Select(driver.find_element(By.CLASS_NAME, "ui-datepicker-month"))
    txtToDtDatePickerMonth.select_by_visible_text(fromDate.split('-')[1])
    driver.find_element(By.XPATH, xpathfordate).click()

    ddlPeriod = driver.find_element(By.ID, "ddlPeriod")
    ddlPeriod.send_keys(category)
    select = Select(driver.find_element(By.ID, "ddlPeriod"))
    select.select_by_visible_text(category)

    ddlPeriod = driver.find_element(By.NAME, "submit").click()
    time.sleep(5)
    return driver


def updateCheckPrice(soup, fromDate):
    datetime_object = datetime.strptime(fromDate, '%d-%b-%Y')
    bsePricestartdt = datetime.strftime(datetime_object + timedelta(days=1), '%d-%b-%Y')
    bsePriceEndDt = datetime.strftime(datetime_object + timedelta(days=5), '%d-%b-%Y')
    xpathforbsePricestartdt = "//a[@data-date='{0}']".format(int(bsePricestartdt.split('-')[0]))
    xpathforbsePriceenddt = "//a[@data-date='{0}']".format(int(bsePriceEndDt.split('-')[0]))

    for link in soup.find_all('a', class_='ng-binding'):
        if "Dividend" in link.text:
            bsePriceDriver = webdriver.Chrome(chrome_options=chrome_options)
            bsePriceDriver.get(bsePriceUri)
            bsePriceDriver.fullscreen_window()
            bsePriceDriver.find_element(By.ID, "ContentPlaceHolder1_rad_no1").click()
            #bsePriceDriver.find_element(By.ID, "ContentPlaceHolder1_smartSearch").clear()
            code = link.text.split("-")[1]
            code = code.strip()
            if not code.isnumeric():
                code = link.text.split("-")[2]
                code = code.strip()

            bsePriceDriver.find_element(By.ID, "ContentPlaceHolder1_smartSearch").send_keys(code)
            bsePriceDriver.find_element(By.XPATH, "//*[@id=\"ulSearchQuote2\"]/li/a").click()

            bsePriceTxtFromDt = bsePriceDriver.find_element(By.ID, "ContentPlaceHolder1_txtFromDate")
            bsePriceTxtFromDt.click()
            bsePriceTxtFromDtDatePickerMonth = Select(bsePriceDriver.find_element(By.CLASS_NAME, "ui-datepicker-month"))
            bsePriceTxtFromDtDatePickerMonth.select_by_visible_text(bsePricestartdt.split('-')[1])
            bsePriceDriver.find_element(By.XPATH, xpathforbsePricestartdt).click()

            bsePriceTxtToDate = bsePriceDriver.find_element(By.ID, "ContentPlaceHolder1_txtToDate")
            bsePriceTxtToDate.click()
            bsePriceTxtToDateDatePickerMonth = Select(bsePriceDriver.find_element(By.CLASS_NAME, "ui-datepicker-month"))
            bsePriceTxtToDateDatePickerMonth.select_by_visible_text(bsePriceEndDt.split('-')[1])
            bsePriceDriver.find_element(By.XPATH, xpathforbsePriceenddt).click()

            element = bsePriceDriver.find_element(By.ID, "ContentPlaceHolder1_btnSubmit").click()

            time.sleep(5)
            data = []
            bsePriceSoup = BeautifulSoup(bsePriceDriver.page_source, "html.parser")
            for trdata in bsePriceSoup.find_all('tr', class_='TTRow'):
                sindta = []
                i = 0
                for tddata in trdata.find_all_next('td'):
                    sindta.append(tddata.text.replace(',', ''))
                    i = i + 1
                    if i == 13:
                        break

                data.append(','.join(sindta))

            printResult(link, data, fromDate)
            bsePriceDriver.close()


if __name__ == "__main__":
    lastDay = "05-Mar-2023"

    for i in range(31):
        print('execution started')
        datetime_object = datetime.strptime(lastDay, '%d-%b-%Y')
        fromDate = datetime.strftime(datetime_object + timedelta(days=i), '%d-%b-%Y')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        driver.fullscreen_window()
        updateCorpPage(driver, fromDate)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
        updateCheckPrice(soup, fromDate)
        print('completed execution')
    exit(0)

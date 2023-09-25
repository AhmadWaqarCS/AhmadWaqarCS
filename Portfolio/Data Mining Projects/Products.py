from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import mysql.connector


options = Options()
options.headless = False
options.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

driver = webdriver.Chrome(
    options=options,
    executable_path='chromedriver.exe')

mydb = mysql.connector.connect(host='localhost',
                               database='starttraffic',
                               user='root',
                               password='')

driver.execute_script("window.open('about:blank','tab8');")
driver.maximize_window()


def mainWeb(cat_url, cat_id):
    try:
        print(cat_url)
        print(cat_id)

        driver.switch_to.window("tab8")
        driver.get(cat_url)
        driver.implicitly_wait(10)

        products = driver.find_elements_by_css_selector("li.ajax_block_product")
        print(len(products))
        for pro in products:
            cloned = pro.find_element_by_css_selector("a.product_img_link").get_attribute("href")
            #model_id = pro.find_element_by_tag_name('p').get_attribute("innerHTML").split(':')[1]
            print(cloned)
            sql = "INSERT INTO products (category_id, status, feed_status, cloned_url) VALUES (%s, %s, %s, %s)"
            args = (cat_id, "Yes", "Yes", cloned)
            mycursor = mydb.cursor()
            mycursor.execute(sql, args)
            mydb.commit()
            print(mycursor.rowcount, "record(s) affected")
            print("1 record inserted, ID:", mycursor.lastrowid)
        try:
            a_next = driver.find_element_by_css_selector('li.pagination_next')
            link = a_next.find_element_by_tag_name('a').get_attribute("href")
            mainWeb(link, cat_id)
        except Exception as e:
           print(e)
           pass

    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
     mycursor1 = mydb.cursor()
     sql1 = "SELECT category_id, cloned_url FROM `category` where cloned=0"
     mycursor1.execute(sql1)
     results = mycursor1.fetchall()
     for result in results:

        result = list(result)
        cat_url = result[1]
        cat_id = result[0]

        mainWeb(cat_url, cat_id)

        sql = "UPDATE category SET cloned = %s WHERE category_id = %s"
        val = (1, cat_id)
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")



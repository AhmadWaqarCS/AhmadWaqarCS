from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import mysql.connector

options = Options()
options.headless = False
options.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

driver = webdriver.Chrome(
    # profile,
    # firefox_profile=fp,
    # capabilities=caps,
    options=options,
    executable_path='chromedriver.exe')

mydb = mysql.connector.connect(host='localhost',
                               database='starttraffic',
                               user='root',
                               password='')

driver.execute_script("window.open('about:blank','tab8');")
driver.maximize_window()


def mainWeb(pro_url, pro_id):
    try:
        print(pro_url)
        print(pro_id)
        driver.switch_to.window("tab8")
        driver.get(pro_url)
        driver.implicitly_wait(10)


        #model_id = driver.find_element_by_id('product_code2').get_attribute('innerHTML')
        pname = driver.find_element_by_css_selector("div.pb-center-column").find_element_by_tag_name('h1').get_attribute("innerHTML")

        #price = driver.find_element_by_id('our_price_display').get_attribute('innerHTML').replace('£', '').replace(' ', '')
        description = driver.find_element_by_css_selector('div#short_description_block').get_attribute('innerHTML')
        stock = 0
        try:
            stock = driver.find_element_by_css_selector('span#quantityAvailable').get_attribute('innerHTML')
        except:
            pass

        feature_image = driver.find_element_by_id("bigpic").get_attribute("src")

        sql = "update products set product_name=%s, product_description=%s, meta_title=%s, meta_description=%s, stock_availability=%s, image_url=%s, feed_status=%s, IsHome=%s, IsFeature=%s, IsSpecial=%s, cloned=%s where product_id=%s"
        args = (pname, description, pname, pname, stock, feature_image, "Yes", "Yes", "Yes", "Yes", 1, pro_id)

        mycursor = mydb.cursor()
        mycursor.execute(sql, args)

        mydb.commit()

        print(mycursor.rowcount, "record(s) affected")
        print("1 record inserted, ID:", mycursor.lastrowid)

        print(pname)
        print("------------")
        print(feature_image)
        print("=--------------")
        print(description)
        print("---------------------")


        try:
            img_ = driver.find_element_by_css_selector('ul#thumbs_list_frame').find_elements_by_tag_name('li')
            for im in img_:
                image_name = im.find_element_by_tag_name('a').get_attribute("href")
                print (image_name)
                sql = "insert into products_images set product_id=%s, image_url=%s"
                args = (pro_id, image_name)
                mycursor = mydb.cursor()
                mycursor.execute(sql, args)
                mydb.commit()
                print(mycursor.rowcount, "record(s) affected")
        except Exception as e:
            print(e)
            pass
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
     mycursor1 = mydb.cursor()
     sql1 = "SELECT product_id, cloned_url, cloned FROM products where cloned=0"
     mycursor1.execute(sql1)
     results = mycursor1.fetchall()
     for result in results:
        result = list(result)
        pro_url = result[1]
        pro_id = result[0]
        mainWeb(pro_url, pro_id)



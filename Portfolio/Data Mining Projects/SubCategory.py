from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import mysql.connector

options = Options()
options.headless = False
options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'

driver = webdriver.Chrome(
    options=options,
    executable_path='chromedriver.exe')

mydb = mysql.connector.connect(host='localhost',
                               database='firepro',
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
        subcats = driver.find_elements_by_css_selector("div.subcategory-box")
        print(len(subcats))
        for subcat in subcats:
            try:
                #cloned_url=pro.find_element_by_tag_name("a").get_attribute("innerHTML")
                cloned = subcat.find_element_by_css_selector("div.title").find_element_by_tag_name("a").get_attribute("href")

                print(cloned)
                heading = subcat.find_element_by_css_selector("div.title").find_element_by_tag_name("a").get_attribute("innerHTML")
                image = subcat.find_element_by_css_selector("div.image").find_element_by_tag_name("img").get_attribute("src")
                print("----------------")
                print(heading)
                print("----------------")
                print(image)
                print("----------------")
                cursor = mydb.cursor()
                cursor.execute('SELECT cloned_url FROM category')
                results = cursor.fetchall()
                lest = []
                for result in results:
                    lest.append(result[0])
                if not cloned in lest:
                    sql = "INSERT INTO category (category_name, meta_title, meta_description, parent, cloned_url, image_url) VALUES (%s, %s, %s, %s, %s, %s)"
                    args = (heading, heading, heading, cat_id, cloned, image)

                    mycursor = mydb.cursor()
                    mycursor.execute(sql, args)

                    mydb.commit()

                    print(mycursor.rowcount, "record(s) affected")
                    print("1 record inserted, ID:", mycursor.lastrowid)
                else:
                    pass

            except Exception as e:
                print(e)
                pass
        '''
        try:
            a_next = driver.find_element_by_css_selector(".next")
            if a_next:
                mainWeb(a_next.get_attribute("href"))
        except Exception as e:
            print(e)
        '''
    except Exception as e:
        print(e)
        pass

if __name__ == '__main__':
     mycursor1 = mydb.cursor()
     sql1 = "SELECT category_id, cloned_url FROM `category`"
     mycursor1.execute(sql1)
     results = mycursor1.fetchall()
     for result in results:
        result = list(result)
        cat_url = result[1]
        cat_id = result[0]
        mainWeb(cat_url, cat_id)



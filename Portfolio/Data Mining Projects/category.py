from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import mysql.connector

options = Options()
options.add_argument("--headless")
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

def mainWeb(cat_sub_title_A):
    try:
        driver.switch_to.window("tab8")
        driver.get(cat_sub_title_A)
        driver.implicitly_wait(10)
        categories = driver.find_element_by_css_selector("ul.sf-menu").find_elements_by_tag_name('li')
        print(len(categories))
        for category in categories:
            try:
                catUrl = category.find_element_by_tag_name("a").get_attribute("href")
                catName= category.find_element_by_tag_name("a").get_attribute("innerHTML")
                #feature_image = category.find_element_by_css_selector("div.image").find_element_by_tag_name("img").get_attribute("src")
                print(catUrl)
                print("----------------")
                print(catName)
                print("----------------")
                sql = "INSERT INTO category (category_name, meta_title, meta_description, status, IsHome, IsMenu, parent, cloned_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                args = (catName, catName, catName, "Yes", "Yes", "Yes", 0, catUrl,)

                mycursor = mydb.cursor()
                mycursor.execute(sql, args)

                mydb.commit()

                print(mycursor.rowcount, "record(s) affected")
                print("1 record inserted, ID:", mycursor.lastrowid)
                mainid = mycursor.lastrowid
                try:
                    driver.execute_script("window.open('about:blank','tab9');")
                    driver.switch_to.window("tab9")
                    driver.get(catUrl)
                    driver.implicitly_wait(10)
                    subcats1 = driver.find_elements_by_xpath("//body[1]/div[3]/div[2]/div[1]/div[3]/div[2]/div[2]/ul[1]/li")[:-1]
                    for subcat1 in subcats1:
                        try:
                            subcatUrl = subcat1.find_element_by_tag_name("a").get_attribute("href")
                            subcatName = subcat1.find_element_by_css_selector("a.subcategory-name").get_attribute("innerHTML")
                            feature_image1 = subcat1.find_element_by_tag_name("a").find_element_by_tag_name("img").get_attribute("src")
                            print (feature_image1)
                            print(subcatUrl)
                            print("2nd Level------------")
                            print(subcatName)
                            print("-------------")
                            sql = "INSERT INTO category (category_name, meta_title, meta_description, status, IsHome, IsMenu, parent, cloned_url, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            args = (subcatName, subcatName, subcatName, "Yes", "Yes", "Yes", mainid, subcatUrl, feature_image1)

                            mycursor = mydb.cursor()
                            mycursor.execute(sql, args)

                            mydb.commit()

                            print(mycursor.rowcount, "record(s) affected")
                            print("1 record inserted, ID:", mycursor.lastrowid)
                            subid = mycursor.lastrowid

                            try:
                                driver.execute_script("window.open('about:blank','tab10');")
                                driver.switch_to.window("tab10")
                                driver.get(subcatUrl)
                                driver.implicitly_wait(10)
                                subcats2 = driver.find_elements_by_xpath("//body[1]/div[3]/div[2]/div[1]/div[3]/div[2]/div[2]/ul[1]/li")[:-1]
                                for subcat2 in subcats2:
                                    try:
                                        subcatUrl1 = subcat2.find_element_by_tag_name("a").get_attribute("href")
                                        subcatName1 = subcat2.find_element_by_css_selector("a.subcategory-name").get_attribute("innerHTML")
                                        feature_image2 = subcat2.find_element_by_tag_name("a").find_element_by_tag_name("img").get_attribute("src")
                                        print(subcatUrl1)
                                        print("Third Level------------")
                                        print(subcatName1)
                                        print("-------------")
                                        sql = "INSERT INTO category (category_name, meta_title, meta_description, status, IsHome, IsMenu, parent, cloned_url, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                        args = (subcatName1, subcatName1, subcatName1, "Yes", "Yes", "Yes", subid, subcatUrl1, feature_image2)

                                        mycursor = mydb.cursor()
                                        mycursor.execute(sql, args)

                                        mydb.commit()

                                        print(mycursor.rowcount, "record(s) affected")
                                        print("1 record inserted, ID:", mycursor.lastrowid)

                                    except Exception as e:
                                        print(e)
                            except Exception as e:
                                print(e)

                        except Exception as e:
                            print(e)

                        driver.switch_to.window("tab9")
                except Exception as e:
                    print(e)

                driver.switch_to.window("tab8")

            except Exception as e:
                print(e)
        driver.quit()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    cat_sub_title_A = "https://activewindowfilms.co.uk/"
    mainWeb(cat_sub_title_A)



import sys
import base64
import traceback

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


# Keep the Browser open even after the auto run
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


# Globals
URL = "https://contentsecurity.mcafee.com/"
username = "santee"
password = "R1ROQ1Mhd="


def downloader():
    # Install and use the appropriate Chrome Driver
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chrome_options
    )
    driver.get(URL)
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(
        base64.b64decode(password).decode("utf-8")
    )
    # Login
    driver.find_element_by_xpath(
        "/html/body/div[1]/div[6]/div/div/div/div/form/div[3]/input"
    ).click()

    # Download the ISO files
    xpaths = (
        "/html/body/div[1]/div[6]/div/div/table/tbody/tr/td[1]/div/div[3]/table/tbody/tr[2]/td[7]/a",
        "/html/body/div[3]/div[3]/div/button[1]/span",
        "/html/body/div[3]/div[3]/div/button[2]/span",
        "/html/body/div[1]/div[6]/div/div/table/tbody/tr/td[1]/div/div[4]/table/tbody/tr[2]/td[7]/a",
        "/html/body/div[5]/div[3]/div/button[1]/span",
        "/html/body/div[5]/div[3]/div/button[2]/span",
    )
    for i in xpaths:
        driver.find_element_by_xpath(i).click()

    # Display the list of iso files downloaded
    iso_files = []
    for i in driver.find_elements_by_class_name("modal-link"):
        file_name = i.get_attribute("href").split("/")[-1]
        if ".iso" in file_name:
            iso_files.append(file_name)
    print("Downloaded iso files:")
    for i in set(iso_files):
        print(i)

    # Logout after the download request
    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/a[2]").click()


if __name__ == "__main__":
    try:
        downloader()
    except Exception as e:
        print("Processor exit with: {}".format(e))
        traceback.print_exc()
        sys.exit(1)  # exit with error

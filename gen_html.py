from selenium import webdriver
import os


def get_html(url):

    from selenium.webdriver.chrome.options import Options

    opt = Options()
    opt.add_argument("--headless")

    wd = webdriver.Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"), options=opt)
    wd.get(url[0])

    file = open("./static/"+url[1]+".html", "w")

    file.write(wd.page_source)
    file.close()
    return

URLs = [
    ["https://www.cnn.com/","cnn"],
    ["https://www.bbc.com/", "bbc"],
    ["https://www.wikihow.com/Main-Page", "wiki"],

]

if __name__ == "__main__":

    for URL in URLs:
        get_html(URL)


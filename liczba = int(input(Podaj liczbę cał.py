import csv
import os

from huggingface_hub.cli import jobs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



url = "https://realpython.github.io/fake-jobs/"


def find_brave_path():
    possible_paths = [
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
        os.path.expanduser(r"~\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe")
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def open_browser():

    if not(find_brave_path()):
        print("Browser not found")
    browser_path = find_brave_path()
    options = webdriver.ChromeOptions()
    options.binary_location=browser_path

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(url)

    liczba = 0
    cards = driver.find_elements(By.CLASS_NAME, "card-content")

    jobs =  []
    for card in cards:
        liczba += 1
# ściąganie nazwy pracy
        try:

            title = card.find_element(By.CSS_SELECTOR, "h2.title.is-5").text
        except:
            print("cos zjebałem")
            break
#ściąganie firmy

        try:
            firma= card.find_element(By.CLASS_NAME, "company").text
        except:
            print("zjebalem coś w firmie")
            break
#ściąganie lokalizacji
        try:
            location = card.find_element(By.CLASS_NAME, "location").text
        except:
            print("cos zjebaem w location")
            break
#ściąganie linku
        try:
            link = card.find_element(By.LINK_TEXT, "Apply").get_attribute("href")
        except:
            print("cos zjebaem w link")
            break

        jobs.append({
            "title": title,
            "company": firma,
            "location": location,
            "link": link
        })
    print(f"Znaleziono {liczba} prac")
    print(jobs)
    return jobs


if __name__ == "__main__":
    jobs = open_browser()
    with open("zapis.csv", "w+", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter( file, fieldnames=["title", "company", "location", "link"])
        writer.writeheader()
        writer.writerows(jobs)

    input("press any key to exit")
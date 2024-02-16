
"""Importing Libaries"""
import bs4
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd

"""functions"""
def git_folder_name(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a")[5:]
    folder_names = [link.text for link in links]
    

    return folder_names

def download_if_not_exists(file_name, url):
    img_l = []
    failed_img_l = []
    
    try:
        response = requests.get(url)
        sours = response.content
        x = BeautifulSoup(sours, "lxml")
        path = os.getcwd()
        path = os.path.join(path, file_name)

        os.makedirs(path, exist_ok=True)
        td_elements = x.find_all("td")

        downloaded_images = os.listdir(path)

        for td in td_elements:
            a_elements = td.find_all("a")
            for a in a_elements:
                href = a.get("href")
                if href:
                    img_url = url + href
                    img_name = img_url.split("/")[-1]
                    file_path = os.path.join(path, img_name)
                    if img_name not in downloaded_images:
                        img_l.append(img_url)

        for img in img_l:
            file_name = os.path.join(path, img.split("/")[-1])
            try:
                with open(file_name, "wb") as f:
                    f.write(requests.get(img).content)
            except Exception as e:
                print("Failed to download:", img)
                failed_img_l.append(img)

    except Exception as e:
        print("An error occurred:", e)

    return failed_img_l




def download_from_url(sub_folder, url):
    # img_l = []
    failed_img_l = []  
    try:
        results = requests.get(url)
        sours = results.content
        x = BeautifulSoup(sours, "lxml")
        path = os.getcwd()
        path = os.path.join(path, sub_folder)

        os.makedirs(path, exist_ok=True)
        exist_files = os.listdir(path)
        td_elements = x.find_all("td")

        for td in td_elements:
            a_elemnts = td.find_all("a")
            for a in a_elemnts:
                href = a.get("href")
                if href and href not in exist_files:
                    img_l = url + href

                    sub_folder = os.path.join(path, img_l.split("/")[-1])
                    try:
                        with open(sub_folder, "wb") as f:
                            f.write(requests.get(img_l).content)
                            print(href + " Downloaded succesfully")
                    except Exception as e:
                        print("Failed to download:", img_l)
                        failed_img_l.append(img_l)


                elif href in exist_files:
                    print(href + " exist")

        # for img in img_l[1:]:
        #     sub_folder = os.path.join(path, img.split("/")[-1])
        #     try:
        #         with open(sub_folder, "wb") as f:
        #             f.write(requests.get(img).content)
        #     except Exception as e:
        #         print("Failed to download:", img)
        #         failed_img_l.append(img)

    except Exception as e:
        print("An error occurred:", e)
    
    return failed_img_l
"""save the links for imgs doesnt downloaded"""

failed_downloads = download_from_url("example_folder", "https://example.com/")
print("Failed downloads:", failed_downloads)
df = pd.DataFrame({'failed_images': failed_downloads})
csv_file_path = "failed_images.csv"
df.to_csv(csv_file_path, index=False)




base_url = "http://soest-hcc1.hcc.hawaii.edu/scheduled_received/quicklooks/"        

sub_folders = git_folder_name(base_url)

for sub_folder in sub_folders:
    url = base_url + sub_folder
    download_from_url(sub_folder, url)



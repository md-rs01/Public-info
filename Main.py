"""
Author: BoyFromBd
Telegram: @heartcraft
"""

import requests
from fake_useragent import UserAgent


def get_valid_input():
    while True:
        user_input = input("Enter a NidNo/MobileNO/BirthRegNO here: ")
        user_input = ''.join(filter(str.isdigit, user_input))  # Filter out non-digit characters
        if user_input:
            if len(user_input) in [10,11, 13, 17]:
                return user_input
            else:
                print("Error: Input length must be 10, 13, or 17 digits.")
        else:
            print("Error: Input must contain at least one digit.")



# Function to generate a random user agent
def user_agent():
    ua = UserAgent()
    user_agent = ua.random
    return user_agent



# Define the request parameters
url = "https://admin.comillalg.gov.bd/api/check/exiting/application"
headers = {
    "Host": "admin.comillalg.gov.bd",
    "User-Agent": user_agent(),  # Call user_agent function to get a random user agent
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Csrf-Token": "5yEU22jwocMkhdniJ5pgxReaJhwSLS4Hl7ANvnNj",
    "Origin": "https://smartup.comillalg.gov.bd",
    "Referer": "https://smartup.comillalg.gov.bd/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Te": "trailers",
}
no = get_valid_input()
data = {
    "searchData": no,
    "applicationType": "1",
    "call_from": "checking",
}



# Send the POST request
def send_request(url, headers, data):
    response = requests.post(url, headers=headers, data=data)
    res = response.json()
    uid = get_union_id(res)  # Call the function to extract Union ID from the response
    data1 = modify_data(uid, data)  # Call the function to modify the data with Union ID
    final_response = requests.post(url, headers=headers, data=data1)
    return final_response.json()
  
  
    
# Function to extract Union ID from the response
def get_union_id(res):
    data_dict = res   
    # Check is union id available or not    
    if data_dict.get('status') == 'error':
        a = "dum"
    else:
        union_id = data_dict['data']['union_id']
        return union_id



# Function to modify data with Union ID
def modify_data(uid, data):
    new_data = {"unionId": uid}
    data.update(new_data)  # Update data dictionary with Union ID
    return data


# Generate name for the File to save All credientials 
def gen_name(info):
    if info.get('status') == 'error':
        return "notfound"
    else:
        name = info['data']['name_bn']
        file_name = name + ".txt"
        return file_name


# Call the Main function of this Program. 
info = send_request(url, headers, data)
name = gen_name(info)
with open(name, 'a', encoding='utf-8') as file:
    file.write(str(info))  # Write data to the file

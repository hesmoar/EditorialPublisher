import gazu
import os
import keyring

#TODO: This will no longer be necessary

#kitsu_url = os.getenv("KITSU_URL")
#kitsu_email = os.getenv("KITSU_EMAIL")
#kitsu_password = os.getenv("KITSU_PASSWORD")
#
#if kitsu_url and kitsu_url.startswith("https://"):
#    print("Warning your KITSU_URL is using https instead of http")
## Login
#
#def connect_to_kitsu():
#    gazu.client.set_host(kitsu_url)
#    logged_in = gazu.log_in(kitsu_email, kitsu_password)
#    if logged_in:
#        print("Kitsu Login successful!")
#    else:
#        print("Login failed.")

def kitsu_auto_login():
    url = keyring.get_password("kitsu", "url")
    email = keyring.get_password("kitsu", "email")
    password = keyring.get_password("kitsu", "password")
    gazu.client.set_host(url)
    logged_in = gazu.log_in(email, password)
    if logged_in:
        print("Kitsu Login successful!")
    else:
        raise Exception("Kitsu Login failed!")


#connect_to_kitsu()
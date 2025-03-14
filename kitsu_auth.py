import gazu
import os

kitsu_url = os.getenv("KITSU_URL")
kitsu_email = os.getenv("KITSU_EMAIL")
kitsu_password = os.getenv("KITSU_PASSWORD")

if kitsu_url and kitsu_url.startswith("https://"):
    print("Warning your KITSU_URL is using https instead of http")
# Login
def connect_to_kitsu():
    gazu.client.set_host(kitsu_url)
    logged_in = gazu.log_in(kitsu_email, kitsu_password)
    if logged_in:
        print("Login successful!")
    else:
        print("Login failed.")


connect_to_kitsu()
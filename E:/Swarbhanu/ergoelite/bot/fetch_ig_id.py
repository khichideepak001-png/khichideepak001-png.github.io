import requests

# We will put the user's new token here
USER_TOKEN = "EAAVBQC1NZBLMBR9upR5GmXHV2uf1A1Q69y8NJ4pXo7epIZA66lIHYnovuuezUPNeP6FjdBSGyTakMGeU7KY6oJt9Ccr0dpUUJrxjHDf6K4BHV8xAih7veC8KL3LxmknQfLfjQQnzPbQ1d4GDxmse1Eoknkg1UNWqQiAeaZBvDREzZCjChUVukGLk5miqmsKweo2saPotNpPWhEOgmy8JIAwE4xozRgiahjIXssX3ZBnn3JQlFS8jZCP341d5lHrrzVj9F5aeLCndEZD"
PAGE_ID = "1194101490449490"  # Extracted from the user's screenshot

def get_page_and_ig_tokens():
    print("--- Step 1: Fetching Page Access Token ---")
    url_page = f"https://graph.facebook.com/v19.0/{PAGE_ID}?fields=access_token&access_token={USER_TOKEN}"
    res_page = requests.get(url_page).json()
    
    if 'access_token' not in res_page:
        print("Error getting Page Access Token:", res_page)
        return
        
    PAGE_ACCESS_TOKEN = res_page['access_token']
    print("Success! Page Access Token retrieved.")
    
    print("\n--- Step 2: Fetching Instagram Business Account ID ---")
    url_ig = f"https://graph.facebook.com/v19.0/{PAGE_ID}?fields=instagram_business_account&access_token={PAGE_ACCESS_TOKEN}"
    res_ig = requests.get(url_ig).json()
    
    if 'instagram_business_account' not in res_ig:
        print("Error getting Instagram ID. Is the Instagram account linked to the Facebook Page?", res_ig)
        return
        
    IG_ID = res_ig['instagram_business_account']['id']
    print("Success! Instagram ID retrieved:", IG_ID)
    
    print("\n=============================================")
    print("FINAL CONFIGURATION FOR post_meta_api.py:")
    print(f"ACCESS_TOKEN = '{PAGE_ACCESS_TOKEN}'")
    print(f"IG_USER_ID = '{IG_ID}'")
    print("=============================================")

if __name__ == "__main__":
    if USER_TOKEN != "TO_BE_FILLED":
        get_page_and_ig_tokens()
    else:
        print("Waiting for User Token...")

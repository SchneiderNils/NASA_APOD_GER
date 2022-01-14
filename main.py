# Erstellt von: Nils Schneider
# Twitter: @OfenkaeseTV
# Twitter Bot: @NASA_APOD_GER

# Version: v1.0
# Erstellt am 14.01.2022


# Import
import tweepy, requests, os, urllib.request, deepl, schedule, time
from dotenv import load_dotenv
from datetime import date

def job():

    # Lädt .env Datei
    load_dotenv()

    # Key abfragen aus .env Datei

    # NASA API
    nasa_api_key = os.getenv('NASA_API_KEY')

    # DeepL API
    deepl_api_key = os.getenv('DEEPL_API_KEY')

    # Twitter API
    api_key = os.getenv('API_KEY')
    api_key_secret = os.getenv('API_KEY_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    # Bild des Tages abfragen und Downloaden(NASA APOD API)
    res = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}')
    pod = res.json()

    datum = date.today()

    urllib.request.urlretrieve(f"{pod['hdurl']}", f"pic/{datum.strftime('%d.%m.%Y')}.jpg")

    # Title übersetzen (DeepL)

    translator = deepl.Translator(deepl_api_key) 
    result = translator.translate_text(pod['title'], target_lang="DE") 
    translated_text = result.text


    # Twitter Bot
    authenticator = tweepy.OAuthHandler(api_key, api_key_secret)
    authenticator.set_access_token(access_token, access_token_secret)

    api = tweepy.API(authenticator, wait_on_rate_limit=True)

    def upload_media(text, filename):
        media = api.media_upload(filename)
        api.update_status(text, media_ids = [media.media_id_string])

    upload_media(f"{translated_text}", f"pic/{datum.strftime('%d.%m.%Y')}.jpg")
    api.update_profile_banner(f"pic/{datum.strftime('%d.%m.%Y')}.jpg")

    print("Twitte am " + datum.strftime('%d.%m.%Y') + " versendet!")
    print("Title: " + translated_text)
    print("Dateiname: " + datum.strftime('%d.%m.%Y') + ".jpg")

schedule.every().day.at("12:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
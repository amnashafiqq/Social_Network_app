import requests
from dateutil.parser import parse as date_parse
from authentication.models import User
import holidays

API_ENDPOINT = 'https://ipgeolocation.abstractapi.com/v1'
API_KEY = '44795dede54942f682b687848f291002' 


def enrich_user_geolocation(user_id):
    user = User.objects.get(id=user_id)
    ip_address = user.last_login.ip_address 
    url = f'{API_ENDPOINT}/?api_key={API_KEY}&ip_address={ip_address}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        country = data.get('country', {}).get('name')
        signup_date = date_parse(user.date_joined.date())

        is_holiday = check_holiday(signup_date, country)

        user.country = country
        user.is_holiday = is_holiday
        user.save()

def check_holiday(date, country):
    country_holidays = holidays.CountryHoliday(country)

    if date in country_holidays:
        return True
    else:
        return False
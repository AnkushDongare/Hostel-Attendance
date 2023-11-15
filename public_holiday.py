import requests
import tkinter as tk
from tkcalendar import Calendar  # Install it using: pip install tkcalendar

def get_public_holidays(year, country_code='IN'):
    url = f'https://public-holiday.p.rapidapi.com/{year}/{country_code}'
    headers = {
        'X-RapidAPI-Host': 'public-holiday.p.rapidapi.com',
        'X-RapidAPI-Key': 'YOUR_RAPIDAPI_KEY'  # Replace with your actual RapidAPI key
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        holidays = response.json()
        return holidays
    except requests.exceptions.RequestException as e:
        print(f"Error fetching public holidays: {e}")
        return None

def show_calendar(year):
    holidays = get_public_holidays(year)

    root = tk.Tk()
    root.title(f"Public Holidays {year}")

    cal = Calendar(root, selectmode="day", year=year, month=1, day=1, locale='en_US')

    for holiday in holidays:
        date_parts = holiday['date']['iso'].split('-')
        day = int(date_parts[2])
        month = int(date_parts[1])
        cal.calevent_create(day, month, 'Public Holiday', 'Public Holiday', 'event', 'holiday')

    cal.pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    show_calendar(2023)

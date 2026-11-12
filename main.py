import requests
from datetime import datetime, timedelta
import sys

def get_location_from_ip():
    """Fetches the user's city and country based on their IP address."""
    try:
        url = "https://ipinfo.io/json"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("city"), data.get("country")
    except requests.exceptions.RequestException:
        return None, None

def fetch_prayer_data(city, country=""):
    """Fetches live prayer times and date info from the Aladhan API."""
    url = "http://api.aladhan.com/v1/timingsByCity"
    params = {
        "city": city,
        "country": country,
        "method": 1  # University of Islamic Sciences, Karachi
    }
    
    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()  # Check for HTTP errors
    data = response.json()
    
    # We now return the whole 'data' block to access both 'timings' and 'date'
    return data["data"]

def calculate_next_prayer(data_block, city):
    """Prints the schedule, Hijri date, and calculates the time remaining until the next prayer."""
    timings = data_block["timings"]
    hijri = data_block["date"]["hijri"]
    
    now = datetime.now()
    current_time_str = now.strftime("%H:%M")
    
    prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
    next_prayer = None
    min_time_diff = float('inf')
    
    # Format and print the Header and Hijri Date
    print(f"\nPrayer Times for {city.title()}")
    print(f"Hijri Date: {hijri['day']} {hijri['month']['en']} {hijri['year']} {hijri['designation']['abbreviated']}")
    print("-" * 35)
    
    for prayer in prayers:
        prayer_time = timings[prayer]
        
        # Convert 24h string to 12h for printing
        pt_obj = datetime.strptime(prayer_time, "%H:%M")
        print(f"{prayer:10}: {pt_obj.strftime('%I:%M %p')}")
        
        # Compare times to find the next prayer today
        if prayer_time > current_time_str:
            fmt = "%H:%M"
            tdelta = datetime.strptime(prayer_time, fmt) - datetime.strptime(current_time_str, fmt)
            diff_minutes = tdelta.total_seconds() / 60
            
            if diff_minutes < min_time_diff:
                min_time_diff = diff_minutes
                next_prayer = prayer
                time_remaining = tdelta
                
    print("-" * 35)
    
    # If a prayer is still left today
    if next_prayer:
        hours, remainder = divmod(time_remaining.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        print(f"Next prayer is {next_prayer} in {hours} hours and {int(minutes)} minutes.")
    
    # If all prayers today are done, calculate time until tomorrow's Fajr
    else:
        fmt = "%H:%M"
        fajr_time_today = datetime.strptime(timings["Fajr"], fmt)
        current_time_obj = datetime.strptime(current_time_str, fmt)
        
        # Add 1 day (24 hours) to Fajr time to represent tomorrow
        fajr_tomorrow = fajr_time_today + timedelta(days=1)
        tdelta = fajr_tomorrow - current_time_obj
        
        hours, remainder = divmod(tdelta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        print(f"All prayers for today are done. Next is Fajr tomorrow in {hours} hours and {int(minutes)} minutes.")
        
    print("-" * 35)
    print()

if __name__ == "__main__":
    city = ""
    country = ""
    
    # The Interactive Menu Loop
    while True:
        print("\n" + "="*35)
        print("Welcome to PraySync")
        print("="*35)
        print("1. Enter a specific city manually")
        print("2. Use my current location (Auto-detect)")
        
        choice = input("\nPlease select an option (1 or 2): ").strip()
        
        if choice == "1":
            city = input("Enter city name (e.g., Karachi): ").strip()
            country = input("Enter country name (optional, press Enter to skip): ").strip()
            break # Exit the menu loop because we got valid input
            
        elif choice == "2":
            print("\nAuto-detecting location from your IP address...")
            city, country = get_location_from_ip()
            
            if not city:
                print("Error: Could not detect location. Please try again using Option 1.")
                continue # Go back to the top of the menu loop
            else:
                print(f"Location detected: {city}, {country}")
                break # Exit the menu loop
                
        else:
            print("Invalid choice! Please enter exactly 1 or 2.")
            # The loop will automatically restart here

    # Once the loop is broken, fetch and display the data
    try:
        api_data = fetch_prayer_data(city, country)
        calculate_next_prayer(api_data, city)
    except requests.exceptions.RequestException as e:
        print(f"\nError connecting to the API: {e}")
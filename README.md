# PraySync

**PraySync** is an interactive, lightweight Python Command Line Interface (CLI) application that fetches live, accurate daily Salah (prayer) timings for any location in the world and calculates a real-time countdown to the next prayer.

## Features

- **Interactive Menu:** A menu-driven terminal interface to navigate the app.
- **Auto-Location Detection:** Automatically detects your city and country using your IP address.
- **Manual City Search:** Allows you to input any city globally to fetch its specific prayer schedule.
- **Smart Countdown Timer:** Accurately calculates the hours and minutes remaining until the next prayer. It even handles the late-night edge case, calculating the exact time until the next day's Fajr after Isha has passed.
- **Hijri Date Display:** Fetches and displays the current Islamic date alongside the timings.
- **Live API Integration:** Powered by the reliable Aladhan API and ipinfo.io.

## Sample Output

```text
===================================
Welcome to PraySync
===================================
1. Enter a specific city manually
2. Use my current location (Auto-detect)

Please select an option (1 or 2): 2

Auto-detecting location from your IP address...
Location detected: Karachi, PK

Prayer Times for Karachi
Hijri Date: 28 Jumada Al-Awwal 1448 AH
-----------------------------------
Fajr      : 05:25 AM
Dhuhr     : 12:15 PM
Asr       : 03:30 PM
Maghrib   : 05:45 PM
Isha      : 07:00 PM
-----------------------------------
Next prayer is Fajr tomorrow in 5 hours and 23 minutes.
-----------------------------------
```

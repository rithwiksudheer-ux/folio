# Pulse-Daily summariser bot
# Fetches-weather(wttr.in) + quotes(zenquotes.io)
# Runs everyday at 8am via github actions

import requests
from datetime import date


def get_weather(city="Kannur"):
    url = f"http://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()  # remove trailing newline
    except Exception as e:
        return f"Weather data unavailable: {e}"


def get_quote():
    """Fetches a random quote from zenquotes
    """
    try:
        url = "https://zenquotes.io/api/random"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()  # json-list
        quote = data[0]['q']
        author = data[0]['a']
        return f'"{quote}" - {author}'
    except Exception as e:
        return f"Quote unavailable: {e}"


def build_summary():
    """Assemble the full daily summary from all data sources
    """
    today = date.today().strftime("%A , %d %B %Y")
    weather = get_weather()
    quote = get_quote()
    summary = f"""
    =============================
    Pulse Daily Summary
    {today}
    =============================
    
    Weather
      {weather}

    Todays Quote
        {quote}

    ==============================
    """
    return summary


def run():
    """"Main entry point caused by github actions
    """
    summary = build_summary()
    print(summary)  # shows in actions logs

    # save to a file (uploaded as downloadable artifact)
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    print("Pulse ran successfully")


if __name__ == "__main__":
    run()

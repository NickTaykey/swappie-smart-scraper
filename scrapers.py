from constants import SWAPPIE_SCRAPING_URL, APPLE_SCRAPING_URL, VALID_COLORS, VALID_CONDITIONS, MODELS_STILL_SOLD_BY_APPLE
from helpers import generic_input_handler, validate_iPhone_model_name, sanitize_iPhone_model_name
from bs4 import BeautifulSoup
import requests
import re


def _get_soup(url):
    return BeautifulSoup(requests.get(url).text, "html.parser")


def fetch_swappie_iPhones_data(model_name, testing=False):
    model_name = model_name.lower()
    soup = _get_soup(f"{SWAPPIE_SCRAPING_URL}/iphone-{model_name.lower()}")
    spans, divs = soup.select("span"), soup.select("div")
    prices = [
        float((t.get_text()[2:]).replace(" ", "0").replace(",", "."))
        if len(t.get_text()) - 2 < 7 else float(
            (t.get_text()[2:]).replace(" ", "").replace(",", "."))
        for t in spans if "€" in t.get_text()
    ][0:-4]
    try:
        next((s for s in divs if s.get_text().lower() == "in saldo!"))
    except:
        pass
    else:
        prices = prices[1::]
    if not len(prices):
        if not testing:
            print("404 Model not found on Swappie!")
            return fetch_swappie_iPhones_data(
                generic_input_handler("Insert iPhone model",
                                      "Invalid model!",
                                      validator=validate_iPhone_model_name,
                                      sanitizer=sanitize_iPhone_model_name))
        return None
    else:
        colors = tuple(t.get_text() for t in spans
                       if t.get_text().lower() in VALID_COLORS and "Colore"
                       and not t.previous_sibling)
        storages = tuple((t.get_text() for t in spans
                          if "GB" in t.get_text() and "|" not in t.get_text()
                          and not re.search(r"\s", t.get_text())))
        conditions = tuple((t.get_text() for t in spans
                            if t.get_text().lower() in VALID_CONDITIONS))[3::]
        return tuple(({
            "price":
            x,
            "conditions":
            conditions[i],
            "color":
            colors[i],
            "storage":
            storages[i],
            "link":
            f"https://swappie.com/it/iphone/iphone-{model_name}/iphone-{model_name}-{storages[i].lower()}-{colors[i].lower().replace(' ', '-')}"
        } for i, x in enumerate(prices)))


def fetch_latest_iPhone_price(model_name, testing=False):
    if model_name in MODELS_STILL_SOLD_BY_APPLE or model_name[0:2] == "se":
        url = f"{APPLE_SCRAPING_URL}/iphone-{model_name[0:2]}"
        if "pro" in model_name:
            url = f"{url}/iphone-{model_name if model_name[len(model_name) - 3: len(model_name)] != 'max' else model_name[0:len(model_name) - 4]}"
        soup = _get_soup(url)
        prices = [
            x.get_text() for x in soup.select("span") if "€" in x.get_text()
        ]
        clean_price_regexp = r"\\n+|€|\s+|(,0+)|\."
        if "pro" in model_name or "mini" in model_name or model_name[
                0:2] == "se":
            return int(re.sub(clean_price_regexp, "", prices[0]))
        elif "max" in model_name or model_name[
                0:2] != "se" and model_name.isnumeric() and int(model_name):
            return int(re.sub(clean_price_regexp, "",
                              prices[len(prices) // 2]))
    elif not testing:
        print("Invalid model name")
    else:
        return None

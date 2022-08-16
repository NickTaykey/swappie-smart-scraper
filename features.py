from helpers import generic_input_handler, sanitize_iPhone_model_name, print_search_results, menu_handler, validate_iPhone_model_name
from constants import VALID_STORAGE_OPTIONS, VALID_CONDITIONS, MODELS_STILL_SOLD_BY_APPLE
from scrapers import fetch_latest_iPhone_price, fetch_swappie_iPhones_data
from functools import partial


def calc_cumulative_savings():
    model_name = generic_input_handler(
        "Insert the latest iPhone model name for which you would like to calc. the cumulative savings",
        f"\nInvalid model choose from this list:\n: {', '.join(MODELS_STILL_SOLD_BY_APPLE[0:-1])} e {MODELS_STILL_SOLD_BY_APPLE[-1]}\n",
        validator=lambda m: m in MODELS_STILL_SOLD_BY_APPLE or m[0:2] == "se",
        sanitizer=sanitize_iPhone_model_name)
    ncys = int(
        generic_input_handler("How frequently (years) would you change iPhone",
                              "Invalid number", lambda i: int(i) > 0))
    tot_years = int(
        generic_input_handler(
            "For how many youe would you like to calculate savings",
            "Invalid number", partial(lambda ncys, val: int(val) >= ncys,
                                      ncys)))
    lip = fetch_latest_iPhone_price(model_name)
    used_iPhones_prices = fetch_swappie_iPhones_data(
        f"{int(model_name[0:2])-1 if model_name[0:2].isnumeric() else model_name}{ '-' if model_name != model_name[0:2] and 'se' not in model_name  else ''}{model_name[3::].replace(' ', '-') if 'se' not in model_name else '' }"
    )
    prices_sum = sum((x["price"] for x in used_iPhones_prices))
    cuip = prices_sum / len(used_iPhones_prices)
    standard_expense = tot_years / ncys * lip
    resellers_expense = tot_years * (lip - cuip)
    cumulative_savings = round(standard_expense - resellers_expense, 2)
    print(
        f"\nIn {tot_years} year You would save: €{cumulative_savings}\nIf instead of changing iPhone every {ncys} years for {tot_years} years\nYou bought the latest model and sold your previous iPhone on Swappie\n\n*** to maximize your savings you should buy iPhones in the same price range ***\n"
    )


def filter_results(iPhones, iPhone_name):
    def storage_filter(iPhones, iPhone_name):
        value = generic_input_handler(
            "Storage: ",
            f"Invalid value choose from: {', '.join([x[0:2] if len(x) < 5 else x[0:3] for x in VALID_STORAGE_OPTIONS[0:-1] ])} E {VALID_STORAGE_OPTIONS[-1][0:4]}",
            lambda v: v.lower(
            ) in VALID_STORAGE_OPTIONS or v + 'gb' in VALID_STORAGE_OPTIONS,
            sanitizer=lambda v: f"{v}gb" if "gb" not in v.lower() else v)
        print_search_results(
            [i for i in iPhones if i["storage"][0:-2] == value[0:-2]],
            iPhone_name,
            focus_key="storage",
            context=f"storage_filter{value}")

    def color_filter(iPhones, iPhone_name):
        available_colors = tuple(set((i["color"].lower() for i in iPhones)))
        value = generic_input_handler(
            "Color:",
            f"Invalid value, choose from: {', '.join(available_colors[0:-1])} and {available_colors[-1]}",
            lambda v: v.lower() in available_colors)
        print_search_results(
            [i for i in iPhones if i["color"].lower() == value],
            iPhone_name,
            focus_key="color",
            context=f"color_filter{value}")

    def conditions_filter(iPhones, iPhone_name):
        value = generic_input_handler(
            "Condition",
            f"Invalid value, choose from: {', '.join(VALID_CONDITIONS[0:-1])} and {VALID_CONDITIONS[-1]}",
            lambda v: v.lower() in VALID_CONDITIONS)
        print_search_results(
            [i for i in iPhones if i["conditions"].lower() == value],
            iPhone_name,
            focus_key="conditions",
            context=f"conditions_filter{value}")

    return menu_handler(
        "\FILTER FOR:\n\n1 - Storage\n2 - Color\n3 - Conditions\n4 - Back\n9 - Quit\n",
        ({
            "command": "1",
            "function": partial(storage_filter, iPhones, iPhone_name)
        }, {
            "command": "2",
            "function": partial(color_filter, iPhones, iPhone_name)
        }, {
            "command": "3",
            "function": partial(conditions_filter, iPhones, iPhone_name)
        }))


def sort_results(iPhones, iPhone_name):
    conditions_sort_order = {k: i for i, k in enumerate(VALID_CONDITIONS)}
    order = generic_input_handler(
        "Order of the results (c: ascending o d: descending)",
        "Ordine non valido", lambda v: v.lower() == "d" or v.lower() == "c")
    return menu_handler(
        "\nSort search results for:\n\n1 - Price\n2 - Storage\n3 - Conditions\n4 - Back\n9 - Quit\n",
        ({
            "command":
            "1",
            "function":
            partial(print_search_results,
                    sorted(iPhones,
                           key=lambda i: i["price"],
                           reverse=order == "d"),
                    iPhone_name,
                    focus_key="price",
                    context=f"sort_by_price_{order}")
        }, {
            "command":
            "2",
            "function":
            partial(print_search_results,
                    sorted(iPhones,
                           key=lambda i: int(i["storage"][0:3] if len(i[
                               "storage"]) == 5 else i["storage"][0:2]),
                           reverse=order == "d"),
                    iPhone_name,
                    focus_key="storage",
                    context=f"sort_by_storage_{order}")
        }, {
            "command":
            "3",
            "function":
            partial(print_search_results,
                    sorted(iPhones,
                           key=lambda i: conditions_sort_order[i["conditions"].
                                                               lower()],
                           reverse=order == "d"),
                    iPhone_name,
                    focus_key="conditions",
                    context=f"sort_by_conditions_{order}")
        }))


def find_cheapest_iPhone():
    cheapest_iPhone = min(fetch_swappie_iPhones_data(
        generic_input_handler("Insert iPhone model",
                              "Invalid model!",
                              validator=validate_iPhone_model_name,
                              sanitizer=sanitize_iPhone_model_name)),
                          key=lambda i: i["price"])
    print(
        f"Cheapest model on Swappie at €{cheapest_iPhone['price']}, link: '{cheapest_iPhone['link']}'"
    )


def find_better_iPhone():
    iPhone_name = generic_input_handler("iPhone model:",
                                        "Invalid model!",
                                        validator=validate_iPhone_model_name,
                                        sanitizer=sanitize_iPhone_model_name)
    iPhones = fetch_swappie_iPhones_data(iPhone_name)
    return menu_handler(
        "\FIND THE BEST IPHONE FOR YOU BY:\n\n1 - Show every iPhone of this type\n2 - Sort search results\n3 - Filter results\n4 - Back\n9 - Quit\n",
        ({
            "command": "1",
            "function": partial(print_search_results, iPhones, iPhone_name)
        }, {
            "command": "2",
            "function": partial(sort_results, iPhones, iPhone_name)
        }, {
            "command": "3",
            "function": partial(filter_results, iPhones, iPhone_name)
        }))

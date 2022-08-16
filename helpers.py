from constants import SWAPPIE_SCRAPING_URL
import requests
import csv
import sys
import re
import os


def sanitize_iPhone_model_name(model_name):
    model_name = re.sub(
        r"\s+", "-",
        re.sub(r"iphone", "",
               model_name.lower().strip()).strip())
    return "se-2020" if model_name == "se" else model_name


def save_data_to_csv_file(iPhones_list, iPhone_name, context="all"):
    if input("Would you like to save search results on a CSV file csv (s/n): "
             )[0].lower() == "s":
        with open(
                f"saved_queries/{iPhone_name.lower().replace('-', '_')}_{context}.csv",
                "w") as f:
            writer = csv.writer(f)
            writer.writerow(
                ("Price (€)", "Conditions", "Color", "Storage", "Link"))
            for i in iPhones_list:
                writer.writerow(i.values())


def validate_iPhone_model_name(model_name):
    return requests.get(
        f"{SWAPPIE_SCRAPING_URL}/iphone-{sanitize_iPhone_model_name(model_name)}"
    ).ok


def menu_handler(menu_options, commands_list):
    print(menu_options)
    while True:
        c = input("> ")
        try:
            command_function = next(
                d.get("function") if d.get("function") else c
                for d in commands_list if d["command"] == c)
        except:
            if c == str(len(commands_list) + 1):
                return -1
            elif c.lower() == "menu" or len(c) and c[0].lower() == "m":
                print(menu_options)
            elif c == "9":
                print("bye")
                sys.exit(0)
            else:
                if c:
                    print("Invalid comand!")
                continue
        else:
            if type(command_function) is str:
                return command_function
            elif command_function() == -1:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(menu_options)


def generic_input_handler(input_msg,
                          error_msg,
                          validator,
                          sanitizer=lambda v: v.lower()):
    v = sanitizer(input(f"{input_msg}: "))
    while not validator(v):
        print(error_msg)
        v = sanitizer(input(f"{input_msg}: "))
    return v


def print_search_results(results_list,
                         iPhone_name,
                         focus_key=None,
                         context="all"):
    if bool(results_list):
        secondary_keys = results_list[0].keys()
        if focus_key:
            secondary_keys = [
                k for k in results_list[0].keys() if k != focus_key
            ]
        for r in results_list:
            log = f"{'€' if focus_key == 'price' else ''}{r[focus_key]}" if focus_key else ""
            for k in secondary_keys:
                log = f"{log+' ' if log else ''}{'€' if k == 'price' else ''}{r[k]}"
            print(log)
        save_data_to_csv_file(results_list, iPhone_name, context)
    else:
        print("No iPhones found!")

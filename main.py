from features import find_cheapest_iPhone, find_better_iPhone, calc_cumulative_savings
from helpers import menu_handler

if __name__ == "__main__":
    menu_handler(
        "SWAPPIE SMART SCRAPER!\n\Main menu\n\n1 - Find cheapest iPhone\n2 - Find the best iPhone for you\n3 - Learn to save\n9 - Quit (ctrl + c)\n",
        (
            {"command": "1", "function": find_cheapest_iPhone},
            {"command": "2", "function": find_better_iPhone},
            {"command": "3", "function": calc_cumulative_savings}
        )
    )

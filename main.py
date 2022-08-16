from features import find_cheapest_iPhone, find_better_iPhone, calc_cumulative_savings
from helpers import menu_handler

if __name__ == "__main__":
    menu_handler(
        "SWAPPIE SMART SCRAPER!\n\nMenu Principale\n\n1 - Trova l'iPhone più economico\n2 - Trova l'iPhone più adatto a te\n3 - Scopri quanto risparmieresti comprando l'iPhone in modo intelligente\n9 - Esci\n\n*** Puoi visualizzare il menu in ogni momento con il comando 'm' ***\n*** Puoi uscire dal programma in qualsiasi momento con ctrl + c (non ti preoccupare se vedi un errore) ***\n",
        (
            {"command": "1", "function": find_cheapest_iPhone},
            {"command": "2", "function": find_better_iPhone},
            {"command": "3", "function": calc_cumulative_savings}
        )
    )

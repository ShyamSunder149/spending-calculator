from bs4 import BeautifulSoup
from prettytable import PrettyTable

import copy
import argparse

from expense import Expense

import utils

def main():
    parser = argparse.ArgumentParser(description="Spending tracker for Google Pay", epilog="Hope that helps!!")
    parser.add_argument('-ecsv', help="Export contents as CSV", action="store_true")
    parser.add_argument('-avg', help="Show average per month spending", action="store_true")
    parser.add_argument('-f', help="Path for the HTML file associated with the operation", required=True)
    args = parser.parse_args()

    money_divs, transaction_divs = parse_html_file(args.f)
    monthly_spendings = process_transactions(money_divs, transaction_divs)
    print(utils.construct_table(monthly_spendings))

    if args.avg:
        utils.calculate_average_spending(monthly_spendings)

    if args.ecsv:
        utils.export_to_csv(monthly_spendings, 'test.csv')

def parse_html_file(file_path: str) -> tuple[list, list]:
    with open(file_path, "r") as file:
        parsed_html = BeautifulSoup(file, features="lxml")
    divs = parsed_html.body.find_all("div", attrs={'class': 'content-cell'})
    money_divs = [divs[i] for i in range(len(divs)) if i % 3 == 0]
    transaction_divs = [divs[i + 2] for i in range(len(divs)) if i % 3 == 0]
    return money_divs, transaction_divs

def process_transactions(money_divs: list, transaction_divs: list) -> dict:
    categories = {
        "travel": ["IRCTC"],
        "entertainment": ["BOOKMYSHOW", "LA CINEMA"],
        "stocks": ["Zerodha"],
        "online_purchase": ["Flipkart", "Amazon"]
    }

    months = "Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec".split(",")
    monthly_spendings = {month: Expense() for month in months}

    for money_div, transaction_div in zip(money_divs, transaction_divs):
        if "Completed" not in transaction_div.text:
            continue

        split_comps = money_div.text.split(" ")
        amount = split_comps[1].split(".")[0]
        amount = int(amount[1:].replace(",", ""))
        month = split_comps[-5][-3:]

        if "2024" not in split_comps[-3] or amount >= 5000:
            continue

        if "Received" in money_div.text:
            monthly_spendings[month].total_credit += amount
        else:
            monthly_spendings[month].total_debit += amount

        for category, options in categories.items():
            monthly_spendings[month].add_expense_to_category(options, money_div.text, category, amount)

    return monthly_spendings



if __name__ == "__main__":
    main()

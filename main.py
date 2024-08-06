from bs4 import BeautifulSoup
import argparse
import copy
from prettytable import PrettyTable

class Expense:
    def __init__(self):
        self.total_debit = 0
        self.total_credit = 0
        self.category_spendings = {}

def check_category(category: str, expense: Expense) -> int:
    return expense.category_spendings.get(category, 0)

def add_expense_to_category(options: list[str], text: str, expense: Expense, category: str, amount: int):
    if any(option in text for option in options):
        expense.category_spendings[category] = expense.category_spendings.get(category, 0) + amount

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
            add_expense_to_category(options, money_div.text, monthly_spendings[month], category, amount)

    return monthly_spendings

def print_table(monthly_spendings: dict):
    table = PrettyTable()
    table.field_names = ["Month", "Debit", "Credit", "Net", "Travel", "Entertainment", "Online Purchase", "Stocks"]

    for month, expense in monthly_spendings.items():
        table.add_row([
            month,
            expense.total_debit,
            expense.total_credit,
            expense.total_debit - expense.total_credit,
            check_category("travel", expense),
            check_category("entertainment", expense),
            check_category("online_purchase", expense),
            check_category("stocks", expense)
        ])

    print(table)

def calculate_average_spending(monthly_spendings: dict):
    total_spending = 0
    active_months = 0

    for expense in monthly_spendings.values():
        net_spending = expense.total_debit - expense.total_credit
        if net_spending != 0:
            total_spending += net_spending
            active_months += 1

    return total_spending / active_months if active_months else 0

def export_to_csv(table: PrettyTable, file_name: str):
    with open(file_name, 'w', newline='') as file:
        file.write(table.get_csv_string())

def main():
    parser = argparse.ArgumentParser(description="Spending tracker for Google Pay", epilog="Hope that helps!!")
    parser.add_argument('-ecsv', help="Export contents as CSV", action="store_true")
    parser.add_argument('-avg', help="Show average per month spending", action="store_true")
    args = parser.parse_args()

    money_divs, transaction_divs = parse_html_file("takeout.html")
    monthly_spendings = process_transactions(money_divs, transaction_divs)
    print_table(monthly_spendings)

    if args.avg:
        average_spending = "{:.2f}".format(calculate_average_spending(monthly_spendings))
        print(f'Average per month spending: {average_spending}')

    if args.ecsv:
        table = PrettyTable()
        table.field_names = ["Month", "Debit", "Credit", "Net", "Travel", "Entertainment", "Online Purchase", "Stocks"]
        for month, expense in monthly_spendings.items():
            table.add_row([
                month,
                expense.total_debit,
                expense.total_credit,
                expense.total_debit - expense.total_credit,
                check_category("travel", expense),
                check_category("entertainment", expense),
                check_category("online_purchase", expense),
                check_category("stocks", expense)
            ])
        export_to_csv(table, 'test.csv')

if __name__ == "__main__":
    main()

from expense import Expense 
from bs4 import BeautifulSoup 

def parse_html_file(file_path: str) -> tuple[list, list]:
    with open(file_path, "r") as file:
        parsed_html = BeautifulSoup(file, features="lxml")
    divs = parsed_html.body.find_all("div", attrs={'class': 'content-cell'})
    money_divs = [divs[i] for i in range(len(divs)) if i % 3 == 0]
    transaction_divs = [divs[i + 2] for i in range(len(divs)) if i % 3 == 0]
    return money_divs, transaction_divs


def update_monthly_spendings(money_div : str, monthly_spendings : dict, categories : dict) -> None: 
   split_comps = money_div.text.split(" ")
   amount = split_comps[1].split(".")[0]
   amount = int(amount[1:].replace(",", ""))
   month = split_comps[-5][-3:]

   if "2024" in split_comps[-3] and amount < 5000:
       if "Received" in money_div.text:
           monthly_spendings[month].total_credit += amount
       else:
           monthly_spendings[month].total_debit += amount
    
       for category, options in categories.items():
           monthly_spendings[month].add_expense_to_category(options, money_div.text, category, amount)


def process_transactions(filepath : str) -> dict:
    
    money_divs, transaction_divs = parse_html_file(filepath)

    categories = {
        "travel": ["IRCTC"],
        "entertainment": ["BOOKMYSHOW", "LA CINEMA"],
        "stocks": ["Zerodha"],
        "online_purchase": ["Flipkart", "Amazon"]
    }

    months = "Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec".split(",")
    monthly_spendings = {month: Expense() for month in months}

    for money_div, transaction_div in zip(money_divs, transaction_divs):
        if "Completed" in transaction_div.text:
            update_monthly_spendings(money_div, monthly_spendings, categories)
    
    return monthly_spendings


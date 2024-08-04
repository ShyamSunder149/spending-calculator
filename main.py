from bs4 import BeautifulSoup
import argparse
import copy
from prettytable import PrettyTable 

class Expense:
    
    def __init__(self):
        self.total_debit = 0
        self.total_credit = 0
        self.category_spendings = {}

def check_category(category : str, expense : Expense) -> int : 
    if category in expense.category_spendings.keys() :
        return expense.category_spendings[category]
    return 0

def check_add(options : list[str], text : str, expense : Expense, category : str, amount : int) :
    for i in options :
        if i in text :
            if category in expense.category_spendings.keys() :
                expense.category_spendings[category] += amount
            else :
                expense.category_spendings[category] = amount

def main() :

    parser = argparse.ArgumentParser(description="spending tracker for google pay",
                                     epilog="Hope that helps!!")
    parser.add_argument('-ecsv',
                        help= "export contents as csv",
                        action="store_true")
    args = parser.parse_args()

    f = open("takeout.html", "r").read()
    parsed_html = BeautifulSoup(f, features="lxml")
    divs = parsed_html.body.find_all("div", attrs={'class' : 'content-cell'})
    money_divs = [divs[i] for i in range(len(divs)) if i%3 == 0]
    transaction_divs = [divs[i+2] for i in range(len(divs)) if i%3 == 0]

    travel = ["IRCTC"]
    entertainment = ["BOOKMYSHOW", "LA CINEMA"]
    stocks = ["Zerodha"]
    online_purchase = ["Flipkart", "Amazon"]
    
    expense = Expense()

    # monthly spending
    monthly_spendings = {}
    rs = {"debit" : 0, "credit" : 0}
    months = "Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec".split(",")
    for i in months :
        monthly_spendings[i] = copy.deepcopy(expense)
    
    for i in range(len(money_divs)) :
        if "Completed" in transaction_divs[i].text :
            split_comps = money_divs[i].text.split(" ")
            amount = split_comps[1].split(".")[0]
            amount = int(amount[1:].replace(",",""))
            month = split_comps[-5][len(split_comps[-5]) - 3:]
            if "2024" in split_comps[-3] and amount < 5000:    
                if "Received" in money_divs[i].text :
                    monthly_spendings[month].total_credit += amount 
                else :
                    monthly_spendings[month].total_debit += amount

                check_add(travel, money_divs[i].text, monthly_spendings[month], "travel", amount)
                check_add(entertainment, money_divs[i].text, monthly_spendings[month], "entertainment", amount)
                check_add(stocks, money_divs[i].text, monthly_spendings[month], "stocks", amount)
                check_add(online_purchase, money_divs[i].text, monthly_spendings[month], "online_purchase", amount)

    table = PrettyTable()
    table.field_names = ["Month", "Debit", "Credit", "Net", "Travel", "Entertainment", "Online Purchase", "Stocks"]
    for i in months: 
        table.add_row([i,
                      monthly_spendings[i].total_debit, 
                      monthly_spendings[i].total_credit, 
                      monthly_spendings[i].total_debit-monthly_spendings[i].total_credit, 
                      check_category("travel", monthly_spendings[i]), 
                      check_category("entertainment", monthly_spendings[i]), 
                      check_category("online_purchase", monthly_spendings[i]),
                      check_category("stocks", monthly_spendings[i])])
    print(table)

    if args.ecsv :
        with open('test.csv', 'w', newline='') as f_output:
            f_output.write(table.get_csv_string())

if __name__ == "__main__" :
    main()

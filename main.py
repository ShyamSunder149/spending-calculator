from bs4 import BeautifulSoup
import copy

class Expense:
    
    def __init__(self):
        self.total_debit = 0
        self.total_credit = 0
        self.category_spendings = {
            "travel" : 0,
            "entertainment" : 0,
            "stocks" : 0,
            "online_purchase" : 0
        }

def main() :
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
        monthly_spendings[i] = copy.copy(expense)
    
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
                for i in split_comps:
                    if i in travel :
                        monthly_spendings[month].category_spendings["travel"] += amount 
                    elif i in entertainment :
                        monthly_spendings[month].category_spendings["entertainment"] += amount 
                    if i in stocks : 
                        monthly_spendings[month].category_spendings["stocks"] += amount 
                    elif i in online_purchase :
                        monthly_spendings[month].category_spendings["online_purchase"] += amount 
    
    for i in months:
        print(f'Net Expense : {monthly_spendings[i].total_debit - monthly_spendings[i].total_credit}')
        print(f'Total credit : {monthly_spendings[i].total_credit}')
        print(f'Total Debit : {monthly_spendings[i].total_debit}')
        print(f'Category Spendings : {monthly_spendings[i].category_spendings}')
if __name__ == "__main__" :
    main()

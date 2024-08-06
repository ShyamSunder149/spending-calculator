from prettytable import PrettyTable

def calculate_average_spending(monthly_spendings: dict) -> int:
    total_spending = 0
    active_months = len([expense.total_debit - expense.total_credit for expense in monthly_spendings.values() if expense.total_debit - expense.total_credit != 0])

    for expense in monthly_spendings.values():
        net_spending = expense.total_debit - expense.total_credit
        total_spending += net_spending if net_spending else 0

    return total_spending / active_months if active_months else 0

def construct_table(monthly_spendings: dict) -> PrettyTable:
    table = PrettyTable()
    table.field_names = ["Month", "Debit", "Credit", "Net", "Travel", "Entertainment", "Online Purchase", "Stocks"]

    for month, expense in monthly_spendings.items():
        table.add_row([
            month,
            expense.total_debit,
            expense.total_credit,
            expense.total_debit - expense.total_credit,
            expense.get_category_spendings("travel"),
            expense.get_category_spendings("entertainment"),
            expense.get_category_spendings("online_purchase"),
            expense.get_category_spendings("stocks")
        ])
    
    return table

def export_to_csv(monthly_spendings: dict, file_name: str) -> None:
    try : 
        with open(file_name, 'w', newline='') as file:
            file.write(table.get_csv_string())
        print("file Exported Successfully")
    except : 
        print("Some Error Occured")


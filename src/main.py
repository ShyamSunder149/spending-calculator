import argparse

from expense import Expense

import parser as p  
import utils

def main():
    parser = argparse.ArgumentParser(description="Spending tracker for Google Pay", epilog="Hope that helps!!")
    parser.add_argument('-ecsv', help="Export contents as CSV", action="store_true")
    parser.add_argument('-avg', help="Show average per month spending", action="store_true")
    parser.add_argument('-f', metavar="filename", help="Path for the HTML file associated with the operation", required=True)
    parser.add_argument('-y', metavar="year", type=int, help="Year for which you want the records", required=True)
    args = parser.parse_args()

    monthly_spendings = p.process_transactions(args.f, args.y)
    print(utils.construct_table(monthly_spendings))

    if args.avg:
        utils.calculate_average_spending(monthly_spendings)

    if args.ecsv:
        utils.export_to_csv(monthly_spendings, args.ecsv)

if __name__ == "__main__":
    main()

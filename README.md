# spending-calculator

This is basically one of my needs to do a finance manager and I don't want to make an entry daily on what I spend and do. And I find myself lazy to code an app which can scrape the messages which comes to the phone and shows you stuff. So instead I used google takeout to export my activities in google pay as html file and updated it as input to my program so I can check the spendings every month end. Please feel free to check out and let me know your suggestions. TIA

Steps to take Google pay backup : 
- Go to google takeout, select google pay and export my activity and initiate a one time download at your convenience to either drive or as download link to mail
- then put the path for -f flag with the main.py program 

Try hitting
```bash
python3 main.py -h 
```

```
usage: main.py [-h] [-ecsv] [-avg] -f filename -y year

Spending tracker for Google Pay

options:
  -h, --help   show this help message and exit
  -ecsv        Export contents as CSV
  -avg         Show average per month spending
  -f filename  Path for the HTML file associated with the operation
  -y year      Year for which you want the records

Hope that helps!!
```

### Features : 
- Export to Csv 
- Table view of expenses month wise
- Average per month net expense 
- year wise expense 

#### To-do :
- [x] fix category expenses  
- [x] Pretty print output
- [x] Table display
- [x] Export to csv option
- [x] flags implementation
- [x] generalise year implementation 
- [x] Average per month spending calculation 
- [ ] Calculate big expenses separately
- [ ] Categorise big expenses 
- [x] add separate implementation to add categories 
- [x] Refactor the code 


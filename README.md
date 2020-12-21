
# Visualisation tool
Work in progress: This version designed to only plot choropleth maps

Requires whoisxmlapi.com APIKEY (write your apikey inside data/meta/APIKEY.txt)
Requires python-basemap to be installed

Workflow: Map from list of IP
1. List IPs in a text file
2. Run vistool.py with txt file as input and with flag -l
3. 1 Run vistool.py with newly created file as input and flag -pic
3. 2 Or run vistool.py with the folder of all files created, and with flag -pac

Workflow: Map from a cowrie logs
1. Clean the log using vistool.py command -c
2. Form a list of IPs using vistool.py command -ip
3. Follow the steps in the first workflow

# TO DO
Create config reader (for easy settings)
Store cowrie logs in sql db (process logs using sql)
Use offline geo ip list (get rif of whoisxml dependency)
More visualisation options
Fix most of the solutions for neater ones, reduce redundant code
Clean and optimize
Add error handling
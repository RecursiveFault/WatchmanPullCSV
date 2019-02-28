#By Matthew Moellman, GSD for Encore Technologies
import sys
import requests
import pandas

if __name__ == '__main__':
    apikey = "lJhZd0JtUp1zIfSnS76g14Yozx06iL1gzhua9Q"
    itr = 1  # iterator
    UID = input("Press enter for all records, or enter the Group UID for a specific group: ")
    if UID != '':
        UID = '&group_id=' + UID # prepend for url insertion if specified

    response = requests.get("https://encoretech.monitoringclient.com/v2.5/computers?api_key={0}{1}&page={2}".format(apikey,UID,itr)).json()  # check response to ensure data was found
    
    if response != []:
        df = pandas.read_json("https://encoretech.monitoringclient.com/v2.5/computers?api_key={0}{1}&page={2}".format(apikey,UID,itr), orient='records') #converts json to generic key-value object
        with open('WatchmanPull.csv', 'w') as f: #Overwrites any previously existing file with first set of computers
            df.to_csv(f) #converts object to csv and writes to created file
        print("Downloading: ", end=''),
    else:
        print("No result for entered value found, exiting...")
        sys.exit()
        
    while response != []:  # loop until final page of computers returns no results
        print("|", end=''),
        itr = itr + 1  # iterate page index
        urlpage = "https://encoretech.monitoringclient.com/v2.5/computers?api_key={0}{1}&page={2}".format(apikey,UID,itr) #iterate api call page to download next set
        response = requests.get(urlpage).json() #ensure next page exists for loop

        df = pandas.read_json(urlpage,orient='records')
        with open('WatchmanPull.csv', 'a') as f: #appends CSV formatted set of values to previously created CSV file
            df.to_csv(f, header=False)
    print("\nComplete!")
    sys.exit()

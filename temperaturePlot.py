from matplotlib import pyplot as plt 

ave_temp = []
year_month = []
count = 0
with open('jythonMusic/imagesAndData/temperature.csv', 'r') as inputFile:
    next(inputFile)
    for line in inputFile:
        
        line = line.replace('"','')
        row = line.split(",")
        year_month.append(row[6])
        ave_temp.append(row[7])
        count+=1
        #Displaying only first 48 records on the plot
        if count == 48:
            break
        
x = range(1, len(ave_temp)+1)
plt.suptitle("Month Year vs Temperature Plot")
plt.title("Displaying records of only first 4 years(1921-24)")
plt.xlabel("Months each year(yyyy-mm)") 
plt.ylabel("Average temperature in degree celsius") 
plt.xticks(x, year_month, rotation='vertical')
plt.plot(x,ave_temp)
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
plt.show()

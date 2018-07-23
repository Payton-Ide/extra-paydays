#!/usr/bin/env python

#Calendar program to determine which months have 5 of a given weekday for a given year
#Author: Payton Ide

import numpy as np 

#####################################################################
#Initial declarations and definitions
#####################################################################

#Define days in month as dictionary 
daysinmonth = {"January": 31, "February": 28, "March": 31, "April": 30, "May": 31, "June": 30, "July": 31, "August": 31,"September": 30, "October": 31, "November": 30, "December": 31} 

leapdaysinmonth = {"January": 31, "February": 29, "March": 31, "April": 30, "May": 31, "June": 30, "July": 31, "August": 31,"September": 30, "October": 31, "November": 30, "December": 31} 

#Dictionary to go from month name to month number
monthmapper = {"January": 0, "February": 1, "March": 2, "April": 3, "May": 4, "June": 5, "July": 6, "August": 7,"September": 8, "October": 9, "November": 10, "December": 11}

#Dictionary to go from day of week to day number
daymapper = {"Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6}


######################################################################
#Read input
#####################################################################

#Get year, to determine firstday
year = int(input("Enter year: "))

#Ask which day to count
dayofinterest = input("Enter day of interest (eg. Sunday): ")


#####################################################################
#Calculate starton for each month
#####################################################################

#Is it a leap year? boolean 
if (year % 4) == 0 and (((year % 100) != 0) or ((year % 400) == 0)):
	leap = True
	print("Leap year")
else:
	leap = False

#Base Truth: January 1st of 1900 was a Monday
firstday = 1 

#Advance day number of January first
daystoadd = 0
for i in range(1900, year):
	if (i % 4) == 0 and (((i % 100) != 0) or ((i % 400) == 0)):
		daystoadd += 2
	else:
		daystoadd += 1

firstday = (firstday + daystoadd) % 7

#Declare array
startholder = np.zeros((12, 3))

#Setup first column as month numbers
for i in range(len(startholder)):
	startholder[i][0] = i + 1

#Setup second column as days in month minus 28. Will be used to add to previous starton
if leap == False:
	startholder[:,1] = [3, 0, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3]
elif leap == True:
	startholder[:,1] = [3, 1, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3]
else:
	print("Error on leap year value")

#Start with January before loop starts
startholder[0][2] = firstday

#Loop using second column to calculate month start date based on info from previous months
for i in range(1,12):
	#Previous starton + addition mod 7
	startholder[i][2] = (startholder[i-1][2] + startholder[i-1][1]) % 7


######################################################################
#Create Calendar for each month
#####################################################################

#Use daymapper to convert from day name to column number
daycolumn = daymapper[dayofinterest]

#Initialize list of months
fivedaymonths = []

#Create each month calendar entry, then calculate number of instances of day of interest
for monthname in monthmapper.keys():
	#Set month name
	month = monthname

	#Set starton: 0-6 for Sunday-Saturday 
	#Convert month to number to get start date from startholder array
	monthnum = monthmapper[month]

	#Use startholder array to set starton
	starton = startholder[monthnum][2]

	#initialize first week 
	y = np.zeros((1, 7))
	for i in range(y.shape[1]): 
		if i < starton: 
			y[0][i] = 0 
		elif i == starton: 
			y[0][i] = 1 
		elif i > starton: 
			y[0][i] = y[0][i-1] + 1 

	#Use y as first week, already manipulated below as x 
	x = y 

	#Set "parameters" for loop 
	if leap == True:
		numberofdays = leapdaysinmonth[month]
	else:
		numberofdays = daysinmonth[month] 

	countermax = numberofdays 

	#Set loop helper variables 
	counter = 0 
	killer = 0 

	#Loop to add rows until a number too large is reached 
	while counter < countermax and killer == 0: 
		#Create new row by adding 1 to each element
		rowtostack = np.zeros((1, 7)) 
		for i in range(rowtostack.shape[1]): 
			rowtostack[0][i] = x[-1][6] + i + 1 

		#Add new row to array
		x = np.row_stack((x, rowtostack)) 

		#Replace values that are too large with 0, kill once this is done 
		for k in range(len(x)): 
			for m in range(x.shape[1]): 
				if x[k][m] > numberofdays: 
					x[k][m] = 0 
					killer = 1 

		#Increment counter 
		counter += 7 

	#Remove entire row if it is all zeros (can only happen to last or first row)
	if x[-1][0] == 0: 
		x = np.delete(x, -1, 0) 
	elif x[0][6] == 0:
		x = np.delete(x, 0, 0)

	#Calculate days of interest
	intdaycount = 0
	for i in range(len(x)):
		if x[i][daycolumn] != 0:
			intdaycount += 1

	if intdaycount == 5:
		fivedaymonths.append(month)

	#print(x)

#Display results
print("List of 5", dayofinterest, "months in", year, ":")
for i in fivedaymonths:
	print(" -", i)
import numpy as np
import csv
import os



# The output file generated contains the calculated probabilities of the precursor and product ions in the Analyte_list.txt files
# The effects of mass filtering is taken into account with the outputted values
# The 
#---------------------------------------------
# Name of Output File with calculated selectivities
out_file = open("output_selectivities.csv", "w")

# Location and Name of the Analyte_list file
#g = open("Analyte_list.txt", "r")

Analyte_list = "Analyte_list.csv"

# Location of the full MS data
FullMS_file = "fullMS.csv"

# Location of the MS2 data
MS2_file = "allMS2.csv"

# What is the mass accuracy of your instrument?
ppm = 3

# What is the isolation window width(m/z)?
Isolation_window = 12

# AIF ?
AIF = "N"

#---------------------------------------------------
































Window_range = Isolation_window/2


ppm = float(ppm)
Ion_mz_delta = ppm/1000000

# Bringing in the precursor and product ions of the analytes being assessed


g = open(Analyte_list, 'r')
a = g.readlines()
g.close()



# Number of analytes
Analyte_num = len(a) - 1
#print(Analyte_num)




#Initializing the output file
Analyte = 0
out_file.write("Name,Abbreviation,Pr(m/z),P(Pr),F1(m/z),P(F1),F2(m/z),P(F2),F3(m/z),P(F3),F4(m/z),P(F4),F5(m/z),P(F5),F6(m/z),P(F6),F7(m/z),P(F7)\n")


#------------------------------------------
# Reading in the complete Full MS data and pasting the mz signals as an array in a temporary file
#------------------------------------------
Full = open("fullMS.csv","r")
fullms = Full.readlines()
Full.close()
Full_len = len(fullms)
data0 = csv.reader(open(FullMS_file, 'r'), delimiter=",", quotechar='|')
next(data0, None)
column1, column2, column3, column4, column5 = [], [], [], [], []
for row in data0:
	column1.extend([row[0]])
column1 = str(column1)
column1 = column1.replace(",","\n")
column1 = column1.replace("'","")	

#Writting out only the m/z signals found in the fullMS.csv file
Temp0 = open('temp0.txt', 'w')
Temp0.write(column1)
Temp0.close()

#Reading in that complete file as an array
Temp0 = open('temp0.txt', 'r')
temp0 = Temp0.readlines()
Temp0.close()
os.remove('temp0.txt')


# Total number of signals detected in all scans
Total_Full_MS_Signals = len(temp0)
# Accounting for blank lines at beginning and end of array
temp0 = temp0[1:Total_Full_MS_Signals-1]

# initializing the full MS array that will be searched
x0 = np.array(temp0)
y0 = x0.astype(np.float)


#------------------------------------------
# Reading in the complete MS2 data
#------------------------------------------
	
data1 = csv.reader(open(MS2_file, 'r'), delimiter=",", quotechar='|')
next(data1, None)
column1, column2, column3, column4, column5 = [], [], [], [], []
for row in data1:
	column1.extend([row[0]])
	
column1 = str(column1)
column1 = column1.replace(",","\n")
column1 = column1.replace("'","")
	
Temp = open('temp1.txt', 'w')
Temp.write(column1)
Temp.close()


Temp1 = open('temp1.txt', 'r')
temp1 = Temp1.readlines()
Temp1.close()
os.remove('temp1.txt')


# Total number of signals detected in all MS2 scans
Total_MS2_Signals = len(temp1)
# Accounting for blank lines at beginning and end of array
temp1 = temp1[1:Total_MS2_Signals-1]

# initializing the full MS2 array that will be searched
x1 = np.array(temp1)
y1 = x1.astype(np.float)

#--------------------------------------------------------------------------
# reading in the analyte compound characteristics

data_analyte = csv.reader(open(Analyte_list, 'r'), delimiter=",", quotechar='|')
next(data_analyte, None)
Col_Name, Col_Abbreviation, Col_Retention_time, Col_Precursor, Col_Number_of_products, Fragment1, Fragment2, Fragment3, Fragment4, Fragment5, Fragment6, Fragment7, Fragment8, Fragment9, Fragment10, Fragment11 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
for row in data_analyte:
	Col_Name.extend([row[0]])
	Col_Abbreviation.extend([row[1]])
	Col_Retention_time.extend([row[2]])
	Col_Precursor.extend([row[3]])
	Col_Number_of_products.extend([row[4]])
	Fragment1.extend([row[5]])
	Fragment2.extend([row[6]])
	Fragment3.extend([row[7]])
	Fragment4.extend([row[8]])
	Fragment5.extend([row[9]])
	Fragment6.extend([row[10]])
	Fragment7.extend([row[11]])
	Fragment8.extend([row[12]])
	Fragment9.extend([row[13]])
	Fragment10.extend([row[14]])
	Fragment11.extend([row[15]])


while Analyte < Analyte_num:

	out_line_pd = str("\n")
	Name = Col_Name[Analyte]
	Name = Name.replace("-"," ")
	Abrev = Col_Abbreviation[Analyte]
	Precursor = Col_Precursor[Analyte]
	precursor = float(Precursor)
	print("\n")
	print(Name)
#---------------------------------------------------
# Defining the m/z range where signals would be counted

	precursor_mz = precursor

	ion_mz_delta = Ion_mz_delta * precursor_mz
	Ion_mz_low = precursor_mz - ion_mz_delta
	Ion_mz_high = precursor_mz + ion_mz_delta

#-----------------------------------------------------------		
# Counting the number of spectra in which the precursor ion was detected at the given mass accuracy	
#-----------------------------------------------------------	
		
	Precursor_selectivity_count = ((Ion_mz_low < y0) & (y0 < Ion_mz_high)).sum()

# If the ion was not found in any full MS scans, a 0.1 value is appllied in place of 0.0)
	if Precursor_selectivity_count == 0:
		Precursor_selectivity_count = 0.10
	else:
		Precursor_selectivity_count = float(Precursor_selectivity_count)

# Probability value determined by the number of detections over total number of signals in files					
	Precursor_selectivity= Precursor_selectivity_count/Total_Full_MS_Signals
	print_out = str(precursor)
	print_out1 = str(Precursor_selectivity)
	print_out1 = str(print_out+" - "+print_out1)

	print(print_out1)

#-----------------------------------------------------------	
# Determining probabability of detecting product ion using a certain isolation window
#-----------------------------------------------------------	
	
		
# Accounting for isolation window size			
	if AIF == "Y":
		Isolation_selectivity = 1.0	

	else:
		Isolation_selectivity_count = (((precursor - Window_range) < y0) & (y0 < (precursor + Window_range))).sum()
		Isolation_selectivity_count = float(Isolation_selectivity_count)
		total_Full_MS_Signals = float(Total_Full_MS_Signals)
		Isolation_selectivity = Isolation_selectivity_count/total_Full_MS_Signals

	print("Quad Selectivity enhancement:")

	
	print(Isolation_selectivity)
		
		
#-----------------------------------------------------------	
# Determining probability of product ions
#-----------------------------------------------------------
# Counting the number of product ions in the analyte list

	
	Ion_num = Col_Number_of_products[Analyte]

	Ion_num = int(Ion_num)
	Ion_Count = 0

	while Ion_Count < Ion_num:
#		print(ion)

		if Ion_Count == 0:	
			Ion_mz = Fragment1[Analyte]
			print("Product Ions:")
		if Ion_Count == 1:	
			Ion_mz = Fragment2[Analyte]
		if Ion_Count == 2:	
			Ion_mz = Fragment3[Analyte]
		if Ion_Count == 3:	
			Ion_mz = Fragment4[Analyte]
		if Ion_Count == 4:	
			Ion_mz = Fragment5[Analyte]
		if Ion_Count == 5:	
			Ion_mz = Fragment6[Analyte]
		if Ion_Count == 6:	
			Ion_mz = Fragment7[Analyte]
		if Ion_Count == 7:	
			Ion_mz = Fragment8[Analyte]
		if Ion_Count == 8:	
			Ion_mz = Fragment9[Analyte]
		if Ion_Count == 9:	
			Ion_mz = Fragment10[Analyte]
		if Ion_Count == 10:	
			Ion_mz = Fragment11[Analyte]			

		Ion_mz = float(Ion_mz)
		ion_mz_delta = Ion_mz_delta * Ion_mz
		Ion_mz_low = Ion_mz - ion_mz_delta
		Ion_mz_high = Ion_mz + ion_mz_delta

# Count the number of instances in the target isolation window						
		Product_Selectivity_Count = ((Ion_mz_low < y1) & (y1 < Ion_mz_high)).sum()
		Product_Selectivity_Count = float(Product_Selectivity_Count)
#		print(Product_Selectivity_Count)
		if Product_Selectivity_Count == 0.0:
			Product_Selectivity_Count = 0.01	
			
		
		total_MS2_Signals = float(Total_MS2_Signals)
		Product_Selectivity = Product_Selectivity_Count/total_MS2_Signals
		
# Factoring in selectivity gained by isolation window size
		
		Product_Selectivity = Product_Selectivity*Isolation_selectivity		
				
# Writing out the file results			
		line_out = str(Ion_mz)
		line_out = str(line_out+" - "+str(Product_Selectivity))		
		print(line_out)
		
		out_line_pd = str(out_line_pd + line_out + ",")
		


		Ion_Count = Ion_Count + 1
#		print(Ion_Count)				
#-----------------------------------------------------------------
		
	out_line1 = str(Name)
	
	out_line2 = str(precursor_mz)
	out_line3 = str(Precursor_selectivity)
	out_line4 = str(out_line_pd)
	
	
	out_line = str(out_line1+","+Abrev+","+out_line2+","+out_line3+","+out_line4)
	out_line = out_line.replace("\n","")
	out_line = out_line.replace(" - ",",")
	out_line = out_line.replace(", ",",")
	out_line = out_line.replace(" ,",",")
	out_file.write(out_line)
	out_file.write("\n")
	
	
	Analyte = Analyte + 1
	
out_file.close()

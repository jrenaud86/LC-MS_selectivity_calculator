## This script tabulates all the m/z signals in Full MS and MS/MS spectra into 1 file.
## A file name "File_list.txt" must contain a list and location of all the mzML files (converted by ProteoWizard into txt format)
## ... to be used



#Collect Full MS Data? (Y/N)
Full_MS = "Y"

#Colletct MS2 Data? (Y/N)
MS_2 = "Y"


#After what time (min) start considering mz signals?
RT_start = 0.3












































#------------------------------------------------------------------------------------------

File_list = open("File_list.txt", "r")
file_list = File_list.readlines()
File_list.close()
n_files = len(file_list)


MS2_File_Name = "allMS2.csv"


if Full_MS == "Y":
#initializing full ms array

	Full_MS_hist = []

	J = 0
	J_max = 3000

	while J < J_max:
		Full_MS_hist.append(0)
		J = J + 1
	

	f = open("fullMS.csv","w")
	f.close()
		
	f = open("fullMS.csv","a")

	J = 0
	while J < n_files:
		

		File = file_list[J]
		File = File.replace("\n","")
		File = File.replace(" ","")

		g = open(File, "r")
		a = g.readlines()
		g.close()

		MS1_scan_num = a.count("        cvParam: ms level, 1\n")



		i = 0
		Scan = 0
		while Scan < MS1_scan_num:
			
	
#Recording the retention time of each scan
			Scan_position = a.index("        cvParam: ms level, 1\n",i)
			RT_position = a.index("          scan:\n",i)
			RT = a[RT_position+1]
			RT = RT.replace("cvParam: scan start time,","")
			RT = RT.replace("minute","")
			RT = RT.replace(" ","")
			RT = RT.replace("\n","")
			RT = RT.replace(",","")
			
			rt = float(RT)

# Extracting the mz data of each scan
			mz_array = a.index("          cvParam: m/z array, m/z\n",i)+1
			mz_array = a[mz_array]
			mz_array = mz_array.replace("          binary: ","")
			mz_array = mz_array.replace(" ","\n")
			mz_start = mz_array.index("]")
			mz_array = mz_array[mz_start+1:]
			mz_array_len = len(mz_array)
			mz_array = mz_array[1:mz_array_len-1]
			
			
			mz_array = str(mz_array)
			
			line = str(","+RT+"\n")
			mz_array = mz_array.replace("\n",line)
			
			if rt > RT_start:
				
				
				f.write(mz_array)
				
			i = Scan_position + 1
			Scan = Scan + 1
		
		J = J + 1
	
	f.close()
else:
	print("no Full MS requested")

	
	
if MS_2 == "Y":
		
	k = open(MS2_File_Name, "w")


	J = 0
	while J < n_files:


		File = file_list[J]
		File = File.replace("\n","")
		File = File.replace(" ","")

		g = open(File, "r")
		a = g.readlines()
		g.close()

		MS2_scan_num = a.count("              selectedIon:\n")


		i = 0
		Scan = 0
		while Scan < MS2_scan_num:
		
			RT_position = a.index("          scan:\n",i)
			RT = a[RT_position+1]
			RT = RT.replace("cvParam: scan start time,","")
			RT = RT.replace("minute","")
			RT = RT.replace(" ","")
			RT = RT.replace("\n","")
			RT = RT.replace(",","")
			rt = float(RT)
			if rt < RT_start:
				Scan = Scan + 1
				Scan_position = a.index("              selectedIon:\n",i)
			else:	
				Scan_position = a.index("              selectedIon:\n",i)
		

				MZ_position = a.index("          cvParam: m/z array, m/z\n",i)
				mz_array = a[MZ_position+1]
				mz_array = mz_array.replace("          binary: ","")
				mz_array = mz_array.replace(" ","\n")
				mz_array = mz_array.replace("\n\n","")
				mz_start = mz_array.index("]")
				mz_array = mz_array[mz_start+1:]
				mz_array_len = len(mz_array)
				mz_array = mz_array[1:mz_array_len-1]
				mz_array = str(mz_array + "\n")
				mz_array = mz_array.replace(" ","\n")
				
				line = str(","+RT+"\n")
				mz_array = mz_array.replace("\n",line)

			
				k.write(mz_array)
				Scan = Scan + 1
			
			i = Scan_position + 1

		
		J = J + 1
		
else:
	print("no MS2 requested")
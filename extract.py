import os.path
from os import path
import csv
import pandas as pd
import re
import pkg_resources
import requests
import re
from symspellpy.symspellpy import SymSpell, Verbosity  # its a spell check library
print(re)
max_edit_distance_dictionary = 2
prefix_length = 7
# create object
sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
# load dictionary
dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
bigram_path = pkg_resources.resource_filename("symspellpy", "frequency_bigramdictionary_en_243_342.txt")
# term_index is the column of the term and count_index is the
# column of the term frequency
if not sym_spell.load_dictionary(dictionary_path, term_index=0,count_index=1):
        print("Dictionary file not found")
if not sym_spell.load_bigram_dictionary(bigram_path, term_index=0,count_index=2):
        print("Bigram dictionary file not found")

table1_exists=None
table2_exists=None
table3_exists=None
table4_exists=None
table5_exists=None
table1_lines=None
table2_lines=None
table3_lines=None
table4_lines=None
table5_lines=None
df_table1=None
df_table2=None

"""
From the file: rawText.txt
text_file_lines:has a list of lines
list_of_words: has a list of all the words
"""
text_file=open("rawText.txt","r")
text_file_lines=text_file.readlines()
text_file.seek(0)
text_file_total_txt=text_file.read()
text_file.seek(0)
list_of_words=[]
for i in range(0,len(text_file_lines)):
	text_file_lines[i]=text_file_lines[i].strip("\n")
	words_on_line=text_file_lines[i].split(" ")
	for j in range(0,len(words_on_line)):
		list_of_words.append(words_on_line[j])
	words_on_line=[]
"""
from the file: keyValues.csv
keys: has a list of all the keys
values: has a list of all the values
"""
csv_file=open("keyValues.csv","r")
csv_rows=csv_file.readlines()
csv_file.seek(0)
values=[]
keys=[]
for i in csv_rows:
	i.strip("\n")
	pair=i.split(",")
	keys.append(pair[0])
	values.append(pair[1])
	#print(pair[0],":",pair[1])

for i in range(0,len(keys)):
	if(keys[i].startswith("\"")):
			keys[i]=keys[i][1:len(keys[i])-2]	
			
"""from file: table-1.csv"""
table1_exists=False
table2_exists=False
if(path.exists("table-1.csv")):
	df_table1=pd.read_csv('table-1.csv')
	table1_exists=True
	table1=open("table-1.csv")
	table1_lines=table1.readlines()
	for i in range(0,len(table1_lines)):
		line=table1_lines[i].split("\",")
		new_line=[]
		for j in line:
			j=j[1:len(j)-1]
			new_line.append(j)
		table1_lines[i]=new_line
"""from file: table-2.csv"""
if(path.exists("table-2.csv")):
	df_table2=pd.read_csv('table-2.csv')
	table2_exists=True
	table2=open("table-2.csv")
	table2_lines=table2.readlines()
	#print(table2_lines)
	for i in range(0,len(table2_lines)):
		line=table2_lines[i].split("\",")
		new_line=[]
		for j in line:
			j=j[1:len(j)-1]
			new_line.append(j)
		table2_lines[i]=new_line		
"""from file: table-3.csv"""
if(path.exists("table-3.csv")):
	table3_exists=True
	df_table3=pd.read_csv('table-3.csv')
	table3=open("table-3.csv")
	table3_lines=table3.readlines()
	#print(table2_lines)
	for i in range(0,len(table3_lines)):
		line=table3_lines[i].split("\",")
		new_line=[]
		for j in line:
			j=j[1:len(j)-1]
			new_line.append(j)
		table3_lines[i]=new_line
	#print(table2_lines)	


"""from file: table-4.csv"""
if(path.exists("table-4.csv")):
	table4_exists=True
	table4=open("table-4.csv","r")
	table4_lines=table4.readlines()
	#print(table2_lines)
	df_table4=pd.read_csv('table-4.csv')
	for i in range(0,len(table4_lines)):
		line=table4_lines[i].split("\",")
		new_line=[]
		for j in line:
			j=j[1:len(j)-1]
			new_line.append(j)
		table4_lines[i]=new_line
		
"""from file: table-5.csv"""
if(path.exists("table-5.csv")):
	table5_exists=True
	table5=open("table-5.csv")
	table5_lines=table5.readlines()
	#print(table2_lines)
	df_table5=pd.read_csv('table-5.csv')
	for i in range(0,len(table5_lines)):
		line=table5_lines[i].split("\",")
		new_line=[]
		for j in line:
			j=j[1:len(j)-1]
			new_line.append(j)
		table5_lines[i]=new_line
df=pd.read_csv('keyValues.csv')
seller_info={"Seller State":"","Seller ID":"","Seller Name":"","Seller Address":"","Seller GSTIN Number":"","Country of Origin":"","Currency":"","Description":""}
def seller_state(df,seller_info):
    df=df.drop_duplicates()
    for i in df.index:
        if(isinstance(df['key'][i],str)):
                description=df['key'][i].lower()
                if(description.find("place of supply")!=-1):
                    if(df['value'][i]==""):
                            print("Seller state:",df['value'][i])
                            seller_info.update({"Seller State":df['value'][i]})
                            break
                    else:
                            i+=1
                            description=df['key'][i].lower()
                            if(description.find("state")!=-1):
                                    print("Seller state:",df['value'][i])
                                    seller_info.update({"Seller State":df['value'][i]})
                                    break
                elif(isinstance(df['value'][i],str)):
                    description=df['value'][i].lower()
                    if(description.find("place of supply")!=-1):
                        seller_info.update({"Seller State":description.split("place of supply",1)[1]})
                        break
def seller_id(text_file_lines,seller_info):
    for i in text_file_lines:
        i=i.lower()
        if('cin' in i):
            found=i.find(":")
            if(found!=-1):
                print("Seller ID:",i.split(":")[1].replace("\n",'').strip(' ').strip("-"))
                seller_info.update({"Seller ID":i.split(":")[1].replace("\n",'').strip(' ').strip("-")})
            else:
                found=i.find(".")
                if(found!=-1):
                    print("Seller ID:",i.split(":")[1].replace("\n",'').strip(' ').strip("-"))
                    seller_info.update({"Seller ID":i.split(".")[1].replace("\n",'').strip(' ').strip("-")})
            break
def seller_gst(text_file_lines,seller_info):
    nxt_line=0
    for i in text_file_lines:
        i=i.lower()
        if(nxt_line):
            Gst_no=i.strip("\n").strip(" ")
            if(Gst_no.isalnum() and len(Gst_no)==15):
                print("Seller GSTIN Number:",Gst_no.replace("-",""))
                seller_info.update({"Seller GSTIN Number":Gst_no.replace("-","")})
            break
        if('gst' in i):
            found=i.find(":")
            if(found!=-1):
                Gst_no=i.split(":")[1].strip("\n").strip(" ")
                if(len(Gst_no)!=15):
                    Gst_no=Gst_no.split(" ")
                    for k in range(len(Gst_no)):
                        Gstin=Gst_no[k]
                        if(len(Gstin)==15):
                            Gst_no=Gstin
                            break
                if(Gst_no.isalnum() and len(Gst_no)==15):
                    print("Seller GSTIN Number:",Gst_no.replace("-",""))
                    seller_info.update({"Seller GSTIN Number":Gst_no.replace("-","")})
                break
            else:
                found=i.find(".")
                if(found!=-1):
                    Gst_no=i.split(".")[1].strip("\n").strip(" ")
                    if(Gst_no.isalnum() and len(Gst_no)==15):
                        print("Seller GSTIN Number:",Gst_no.replace("-",""))
                        seller_info.update({"Seller GSTIN Number":Gst_no.replace("-","")})
                    break
                else:
                    nxt_line=1
def currency(text_file_lines,seller_info):
    for i in text_file_lines:
        i=i.lower()
        if("currency" in i):
            found=i.find(":")
            if(found!=-1):
                print("Currency:",i.split(":")[1].strip(" ").strip("-").replace("\n",""))
                seller_info.update({"Currency":i.split(":")[1].strip(" ").strip("-").replace("\n","")})
                break
        if(("inr" in i) or ("rupees" in i) or("paise")):
            print("Currency: INR")
            seller_info.update({"Currency":"INR"})
            break
        if(("usd" in i) or ("dollars" in i)):
            print("Currency: USD")
            seller_info.update({"Currency":"USD"})
            break
def country_of_origin(text_file_lines,seller_info):
    f=1
    dict_of_currencies={'INR':'INDIA','USD':'USA'}
    for i in text_file_lines:
        i=i.lower()
        if("country of origin" in i):
            found=i.find(":")
            if(found!=-1):
                print("Country of Origin:",i.split(":")[1].strip(" ").strip("-").replace("\n","").replace("/",""))
                seller_info.update({"Country of Origin":i.split(":")[1].strip(" ").strip("-").replace("\n","").replace("/","")})
                f=0
                break
    try:
        if(f):
            print("Country of Origin:",dict_of_currencies[seller_info['Currency']])
            seller_info.update({"Country of Origin":dict_of_currencies[seller_info['Currency']]})
    except:
            print("")
def address(text_file_lines,seller_info):
    for i in text_file_lines:        
        if(i.count(",")>1):
            print("Seller Address:",i.strip("\n"))
            seller_info.update({"Seller Address":i.strip("\n")})
            break
seller_id(text_file_lines,seller_info)
seller_gst(text_file_lines,seller_info)
currency(text_file_lines,seller_info)
country_of_origin(text_file_lines,seller_info)
address(text_file_lines,seller_info)
seller_state(df,seller_info)
"""
Problem number 1: finding the invoice number
Case 1: When the invoice number is present in the keyValue pair file
	becomes very easy
	simply extract the value from the file
Case 2: When it is NOT in the keyValue file:

let all the candidates for invoice_number be stored in invoice_number_cand
Check #1: Must be a number
Check #2: Must not be a single digit number
Check #3: 
searh for line in wich the candidate appears
search for the line in which key word appears
find difference between the two lines
in case of multiple occurences, retain smaller distance
print the ones with the least distance

"""
invoice_number_cand=dict()
def invoice_number_txt(text_file_lines,list_of_words,invoice_number_cand):


	"""The following code picks out the most likely candidate for invoice number based on the information presented by the rawText.txt files"""
	for i in range(0,len(list_of_words)):
		if list_of_words[i].isnumeric():
			if len(list_of_words[i])>1:
				invoice_number_cand[list_of_words[i]]=i
				
	candidate_keys=list(invoice_number_cand.keys())
	count=0
	for i in range(0,len(text_file_lines)):
		if candidate_keys[count] in text_file_lines[i]:
			invoice_number_cand[candidate_keys[count]]=i
			count+=1
	
	
	check=0
	for i in range(0,len(text_file_lines)):
		check=0
		if 'Invoice No'.lower() in text_file_lines[i].lower():
			
			for count in range(0,len(candidate_keys)):
				if(check==0):
					invoice_number_cand[candidate_keys[count]]=abs(invoice_number_cand[candidate_keys[count]]-i)
					check=1
				if(check==1):
					if(invoice_number_cand[candidate_keys[count]]>abs(invoice_number_cand[candidate_keys[count]]-i)):
						invoice_number_cand[candidate_keys[count]]=abs(invoice_number_cand[candidate_keys[count]]-i)
					
	candidate_values=list(invoice_number_cand.values())
	#print(candidate_values)
	top3=candidate_values[:3]

	final=100000
	for i in candidate_keys:
		if(invoice_number_cand[i] in top3):
			if(int(invoice_number_cand[i])<int(final)):
				final=invoice_number_cand[i]
				final_candidate=i

	return final_candidate
		
def invoice_number_csv(keys,values):
	final_candidate=None
	for i in range(0,len(keys)):
		if 'Invoice No'.lower() in keys[i].lower() or 'Order No'.lower() in keys[i].lower():
			if(values[i].startswith("\"")):
				values[i]=values[i][1:len(values[i])-2]
			final_candidate=values[i].split(" ")[0]
	

	return final_candidate
	
invoice_number=invoice_number_csv(keys,values)
if(invoice_number==None):

	invoice_number=invoice_number_txt(text_file_lines,list_of_words,invoice_number_cand)
print("The invoice number is: ",invoice_number)
seller_info.update({"Invoice Number":invoice_number})

#####################################################
"""Invoice Date
Check in keyvalue pairs
"""
def invoice_date_csv(keys,values):
	for i in range(0,len(keys)):
		if 'Invoice Date'.lower() in keys[i].lower() or 'Order No /Date'.lower() in keys[i].lower() or 'Dated'.lower() in keys[i].lower():
			if 'due'.lower() in keys[i].lower():
				continue
			if(values[i].startswith("\"")):
				values[i]=values[i][1:len(values[i])-2]
			final_candidate=values[i].split(" ")[0]
			if "." in final_candidate or "/" in final_candidate:

				return final_candidate
			else:
				final_candidate=values[i].split(" ")[1]

				return final_candidate

	

invoice_date=invoice_date_csv(keys,values)
print("The invoice date is: ",invoice_date)
seller_info.update({"Invoice Date":invoice_date})
######################################################
"""Delivery Date
Check in keyvalue pairs
"""
def due_date_csv(keys,values):
	for i in range(0,len(keys)):
		if 'Delivery Date'.lower() in keys[i].lower() or 'Due Date'.lower() in keys[i].lower():
			
			if(values[i].startswith("\"")):
				values[i]=values[i][1:len(values[i])-2]
			final_candidate=values[i].split(" ")[0]
			if "." in final_candidate or "/" in final_candidate:

				return final_candidate
			else:
				final_candidate=values[i].split(" ")[1]

				return final_candidate

due_date=due_date_csv(keys,values)
if(due_date==None):
	due_date=invoice_date
print("The due date is: ",due_date)
seller_info.update({"Due Date":due_date})
#####################################################
"""
total amount entered by WH operator
step#1: in case it still does not give the right answer, find the row that has INR in it. - return whatever word in the string has a number
step#2: numbers having . or , in them
step #3:ignore all single/double length characters since this is likely serial nubers and page numbers
step #4: search for the numeric closest to the text 'total invoic'-> v. complicated
step #5: remove everything that does not have a decimal point
step #6: any number that starts with 0, obviously doesnt qualify
we have to search rawText since keyvalues and tables don't have it

"""

def wh_amount_txt(list_of_words,text_file_lines,text_file_total_txt,re):
	for i in text_file_lines:
		if 'INR' in i:
			
			line_with_INR=i.split(" ")
			for j in line_with_INR:
				for k in j:
					if(k.isnumeric()):
						
						return j
			
	else:
		
		wh_amount_cand=dict()
		"""for loop below is to find candidate keys that qualify steps 1 and 2"""
		for i in list_of_words:
			if (bool(re.search('[a-zA-Z]', i)) or len(i)<=2):
				continue
			else:
				wh_amount_cand[i]=0
		"""for loop below is to initialize the candidate keys in the dictionary to a list of their location(s) in the text file. THis is stored in wh_amount_cand"""
		
		candidate_keys=list(wh_amount_cand.keys())
		count=0
		for i in candidate_keys:
			wh_amount_cand[i]=[]
			for j in range(0,len(text_file_lines)):
				if i in text_file_lines[j]:
					wh_amount_cand[i].append(j)
					continue
				
		#print(wh_amount_cand)#now this dictionary has keys of candidate values and values are a list of their locations

		"""below code is used to calculate the distance between the key and the search word/ identifier"""
		
		"""The identifier can appear multiple times and can have mulitple possibilities. The below code segment is used to find the locations of all the identifiers and append them to a alist called identifier_loc"""
		
		#check=0
		case=0
		identifier_loc=[]
		if("total Invoic".lower() in text_file_total_txt.lower()):
			for i in range(0,len(text_file_lines)):
				if("total Invoic".lower() in text_file_lines[i].lower()):
					identifier_loc.append(i)
			case=1
		elif("total lnvoic".lower() in text_file_total_txt.lower()):
			for i in range(0,len(text_file_lines)):
				if("total lnvoic".lower() in text_file_lines[i].lower()):
					identifier_loc.append(i)
			case=2
		elif("total".lower() in text_file_total_txt.lower()):
			for i in range(0,len(text_file_lines)):
				if("total".lower() in text_file_lines[i].lower()):
					identifier_loc.append(i)
			case=3
			
		

		"""Below code is used to find which candidate key and identifier bears the least distance. All combinations are subtracted and the minimum ones are stored in a dictionary called wh_amount_cand_min for all 3 possible identifiers"""

		if(case==1):
			
			wh_amount_cand_min=dict()
			for i in wh_amount_cand:
				wh_amount_cand_min[i]=9999999
			
			change=0

			for i in identifier_loc:
				
				for j in wh_amount_cand:
					for k in range(0,len(wh_amount_cand[j])):
					
						if(abs(wh_amount_cand[j][k]-i)<wh_amount_cand_min[j]):
							wh_amount_cand_min[j]=abs(wh_amount_cand[j][k]-i)
							"""change=1
							#print(wh_amount_cand_min)
					if(change==1):
						wh_amount_cand_min[j]=min
						change=0"""
					

		if(case==2):
			
			wh_amount_cand_min=dict()
			for i in wh_amount_cand:
				wh_amount_cand_min[i]=9999999
			
			change=0

			for i in identifier_loc:
				
				for j in wh_amount_cand:
					for k in range(0,len(wh_amount_cand[j])):
					
						if(abs(wh_amount_cand[j][k]-i)<wh_amount_cand_min[j]):
							wh_amount_cand_min[j]=abs(wh_amount_cand[j][k]-i)
							"""change=1
							#print(wh_amount_cand_min)
					if(change==1):
						wh_amount_cand_min[j]=min
						change=0"""
				
							
					
		if(case==3):
			
			wh_amount_cand_min=dict()
			for i in wh_amount_cand:
				wh_amount_cand_min[i]=9999999
			
			change=0

			for i in identifier_loc:
				
				for j in wh_amount_cand:
					for k in range(0,len(wh_amount_cand[j])):
					
						if(abs(wh_amount_cand[j][k]-i)<wh_amount_cand_min[j]):
							wh_amount_cand_min[j]=abs(wh_amount_cand[j][k]-i)
							"""change=1
							#print(wh_amount_cand_min)
					if(change==1):
						wh_amount_cand_min[j]=min
						change=0"""
			
			
			
			
			
		
		sorted_wh_amount_cand=sorted(wh_amount_cand_min.items(),key=lambda x:x[1])
	
		for i in sorted_wh_amount_cand:
			if('.' not in i[0]):

				sorted_wh_amount_cand.remove(i)
		for i in sorted_wh_amount_cand:		
			if(i[0][0] == '0'):

				sorted_wh_amount_cand.remove(i)
		
		#print(sorted_wh_amount_cand)
		return(sorted_wh_amount_cand[0][0])

			

	
wh_amount=wh_amount_txt(list_of_words,text_file_lines,text_file_total_txt,re)
print("Total Invoice amount entered by WH operator",wh_amount)
seller_info.update({"Total Invoice amount entered by WH operator":wh_amount})
"""
Total invoice qty:
step 1: find all integers
step 2: find integers along the column of qty
alternative: 
step 1: find the row which has 'Total' in it
step 2: the numeric quantity that is smaller will be the qty
 
"""
def qty_txt(list_of_words,table1_lines,table2_lines,table1_exists,table2_exists):
	candidates=[]
	for i in list_of_words:
		if (i.isnumeric()):
			candidates.append(i)
	col_no=0
	for i in table1_lines:
		for j in range(0,len(i)):
			if ((i[j].lower()=='Oty'.lower()) or (i[j].lower()=='Qty'.lower())):

				col_no=j
				break
	candidates_qty=[]
	if(col_no!=0):
		for i in table1_lines:
			if(len(i)>=col_no and len(i[col_no])>=1):

				if i[col_no][0].isdigit():
					candidates_qty.append(int(float(i[col_no])))
		if(table2_exists):
			for i in table2_lines:
				if(len(i)>=col_no and len(i[col_no])>=1):
					if i[col_no][0].isnumeric():
						candidates_qty.append(int(float(i[col_no])))

	credible_row=[]
	if(candidates_qty==[]):
		for i in table1_lines:

			for j in i:
				if j.lower()=='Total'.lower():
					credible_row=i
		if(credible_row==[]):
			for i in table2_lines:

				for j in i:
					if j.lower()=='Total'.lower():
						credible_row=i
				
					

		for i in credible_row:
			if len(i)>=1:
				if i.split(" ")[0][0].isdigit():
					candidates_qty.append(i.split(" ")[0])
		return min(candidates_qty,key=len)
			
	return (max(candidates_qty))
	
	
wh_qty=qty_txt(list_of_words,table1_lines,table2_lines,table1_exists, table2_exists)
print("Quantity entered by WH operator:",wh_qty)
seller_info.update({"Quantity entered by WH operator:":wh_qty})

"""
total tcs collected
possibility #1:
have all the table files open
search row 1 of all these files for the word 'Tax'
if it is there, save the column number and select the element on the last row of the same column number
step #1: has numbers in it and no letters
step #2: -eliminate candidates that are not present in the same row as 'Total'
step #3:-the element with the largest value not equal to the length of the number of columns 
		-can't be a 0
"""
def tcs_txt(list_of_words,table1_lines,table2_lines, table3_lines, table4_lines, table5_lines,table1_exists, table2_exists, table3_exists, table4_exists, table5_exists):

	if(table1_exists):
		col_no=0
		for i in range(0,len(table1_lines[0])):
			if ("tax ".lower() in table1_lines[0][i].lower()):
				
				col_no=i
				return (table1_lines[len(table1_lines)-1][col_no])
	if(table2_exists):
		col_no=0
		for i in range(0,len(table2_lines[0])):
			if ("tax ".lower() in table2_lines[0][i].lower()):
				
				col_no=i
				return (table2_lines[len(table2_lines)-1][col_no])
	if(table3_exists):
		col_no=0
		for i in range(0,len(table3_lines[0])):
			if ("tax ".lower() in table3_lines[0][i].lower()):
				
				col_no=i
				return (table3_lines[len(table3_lines)-1][col_no])
	if(table4_exists):
		col_no=0
		for i in range(0,len(table4_lines[0])):
			if ("tax ".lower() in table4_lines[0][i].lower()):
				
				col_no=i
				return (table4_lines[len(table4_lines)-1][col_no])
			
					
	if(table5_exists):
		col_no=0
		for i in range(0,len(table5_lines[0])):
			if ("tax ".lower() in table5_lines[0][i].lower()):
				
				col_no=i
				return (table5_lines[len(table5_lines)-1][col_no])




	
	candidates=[]
	for i in list_of_words:
		if(len(i)>=1):
			if (i[0].isnumeric() and not(bool(re.search('[a-zA-Z]', i)))):
				candidates.append(i)
	length_of_a_row=0
	#print(table1_lines)
	final_candidates=dict()
	if(table1_exists):
		
		last_row=table1_lines[len(table1_lines)-1]
		check=0
		for i in (last_row):
			if('Total'.lower() in i.lower() or 'Totud'.lower() in i.lower()):
				length_of_a_row=len(table1_lines[0])
				#print("HEY")
				check=1
				
		if(check==1):
			for i in candidates:
				if(i in last_row):
					if i not in final_candidates:
						for j in range(0,len(last_row)):
							if(last_row[j]==i):
								final_candidates[i]=j
								break
	
	#print(table2_lines)
	#print(candidates)
	
	#print(final_candidates)
	if(table2_exists):
		if(check==0):
			last_row=table2_lines[len(table2_lines)-1]
		check=0
		for i in (last_row):
			if('Total'.lower() in i.lower() or 'Totud'.lower() in i.lower()):
				length_of_a_row=len(table1_lines[0])
				check=1
				#print(check)
		if(check==1):
			for i in candidates:
				if(i in last_row):

					if i not in final_candidates:
						
						for j in range(0,len(last_row)):
							if(last_row[j]==i):
								final_candidates[i]=j
								break
	
	#print(last_row)
	#print(final_candidates)
	max=0
	final_candidate=None
	#print(length_of_a_row)
	for i in final_candidates:
		if(final_candidates[i]==length_of_a_row-2):
			continue
		else:
			if(max<final_candidates[i]):
				if(i[0]!='0'):
					max=final_candidates[i]
					final_candidate=i
					
	if(final_candidate==None):
		candidates=dict()
		"""for loop below is to find candidate keys that are numbers"""
		for i in list_of_words:
			if (bool(re.search('[a-zA-Z]', i)) or len(i)<=2):
				continue
			else:
				candidates[i]=0
		"""for loop below is to initialize the candidate keys in the dictionary to a list of their location(s) in the text file. THis is stored in candidates"""
		
		candidate_keys=list(candidates.keys())
		count=0
		for i in candidate_keys:
			candidates[i]=[]
			for j in range(0,len(text_file_lines)):
				if i in text_file_lines[j]:
					candidates[i].append(j)
					continue
				
		#print(candidates)
		"""below code is used to calculate the distance between the key and the search word/ identifier"""
		
		"""The identifier can appear multiple timesThe below code segment is used to find the locations of all the identifiers and append them to a alist called identifier_loc"""
		
		
		identifier_loc=[]
		if("tax ".lower() in text_file_total_txt.lower()):
			for i in range(0,len(text_file_lines)):
				if("tax ".lower() in text_file_lines[i].lower()):
					identifier_loc.append(i)
			
		#print(identifier_loc)
		tcs_min=dict()
		for i in candidates:
			tcs_min[i]=9999999
			
		change=0

		for i in identifier_loc:
			
			for j in candidates:
				for k in range(0,len(candidates[j])):
				
					if(abs(candidates[j][k]-i)<tcs_min[j]):
						tcs_min[j]=abs(candidates[j][k]-i)
						
						
		sorted_candidates=sorted(tcs_min.items(),key=lambda x:x[1])
	
		for i in sorted_candidates:
			if('.' not in i[0]):

				sorted_candidates.remove(i)
		for i in sorted_candidates:		
			if(i[0][0] == '0'):

				sorted_candidates.remove(i)	
				
		final_candidate=sorted_candidates[0][0]
	return final_candidate
	
	
	

wh_tcs=tcs_txt(list_of_words,table1_lines,table2_lines,table3_lines, table4_lines, table5_lines,table1_exists, table2_exists, table3_exists, table4_exists, table5_exists)
print("Total TCS collected by WH operator",wh_tcs)
seller_info.update({"Total TCS collected by WH operator":wh_tcs})
#################################################
"""Numbers after the decimal point n the wh_amount"""
def round_off(wh_amount):
	decimal=''
	for i in wh_amount[::-1]:
		decimal=i+decimal
		if i=='.':
			break
	return decimal
decimal=round_off(wh_amount)
print("Round off charges:",decimal)
seller_info.update({"Round off charges":decimal})
################################################
"""return the word that has 'PO' in it
remove any part of the sring that is not a number or alphabet"""
def po_number_txt(list_of_words):
	candidates=[]
	candidate=''
	for i in list_of_words:
		if('PO' in i):
			for j in i:
				if(j.isdigit() or j.isalpha()):
					candidate+=j
				
				else:
					break
			candidates.append(candidate)
			candidate=''
	return candidates[0]
po_number=po_number_txt(list_of_words)
print("PO Number: ",po_number)
seller_info.update({"PO Number":po_number})
################################################
"""invoice amt without decimal"""
def invoice_amt_txt(wh_amount):
	invoice_amt=''
	encountered=0
	for i in wh_amount[::-1]:
		if(encountered==0):
			if(i=='.'):
			
				encountered=1
		else:
			invoice_amt=i+invoice_amt
	return invoice_amt
invoice_amt=invoice_amt_txt(wh_amount)
print("invoice amount:",invoice_amt)
seller_info.update({"invoice amount":invoice_amt})
###############################################
"""invoice total quantity
"""
def invoice_qty_txt(wh_qty):
	return wh_qty
invoice_qty=invoice_qty_txt(wh_qty)
print("invoice qty: ",invoice_qty)
seller_info.update({"invoice qty":invoice_qty})
###########################
"""print the value of gstin"""
def gstin_txt(keys,values):
	for i in range(0,len(keys)):
		if 'GSTIN' in keys[i] or 'GSITN' in keys[i] or 'GSTN' in keys[i]:
			gstin=(values[i][1:len(values[i])-2])
			return gstin
gstin=gstin_txt(keys,values)
print("gstin:",gstin)
seller_info.update({"gstin":gstin})
##################################
"""
Discount:
everything below the heading that has the words 'Disc'
everything with numbers gets appended
invoice 1 doesn't have this heading- it has '1%)'
so i added a constraint saying that even if '%' is in the heading i will print everything below it

"""
def discount(table1_lines):
	headings=table1_lines[0]
	col_no=None
	for i in range(0,len(headings)):
		#print(headings[i])
		if('Disc'.lower() in headings[i].lower() or '%' in headings[i]):
			#print(headings[i])
			col_no=i
			break
	discounts=[]
	if(col_no==None):
		return []
	for i in table1_lines[1:]:
		if(len(i[col_no])>1):
			if(i[col_no][0].isnumeric()):
				discounts.append(i[col_no])
	#print(table1_lines)
	return discounts[:len(discounts)-1]
discounts=discount(table1_lines)
print("discounts:",discounts)
"""
SGST %
Invoice 4- 
	check the column which has 'SGST Rate'
	REALLY BAD QUALITY.
	Sgst got read as '333T Bats'
	the scanned copy is of vv poor quality :(
INvoice 3-
	hasn't got ANY SGST :(
INvoice 2-
	hasn't got ANY SGST :(
INvoice 1-
	has both sgst and cgst but it is not recognized in the table.
	so i'll find 'sgst' in the .txt file
	find which 'rate' it is closer to
	mark the rate by a number (1st/2nd/3rd)
	find that occurence in that headings column
	add all the values below it to a list of SGST values	
"""
def sgst_csv(list_of_words, text_file_lines, table1_lines, table2_exists, table2_lines):
	rate_candidates=dict()
	count=1
	"""for loop below is to find the word rate and rank them in order of their occurence"""
	for i in list_of_words:
		if ('rate'.lower() in i.lower()):
			rate_candidates[count]=0
			count+=1
	
	count=1		
	for i in range(0,len(text_file_lines)):
		if ('rate'.lower() in text_file_lines[i].lower()):
			#print(text_file_lines[i])
			rate_candidates[count]=i
			count+=1
	
	#rint(rate_candidates)
	if(len(rate_candidates)==0):
		return []
	sgst_pos=None
	for i in range(0,len(text_file_lines)):
		if('sgst'.lower() in text_file_lines[i].lower()):
			sgst_pos=i
			break
	if(sgst_pos==None):
		return []
	for i in rate_candidates:
		rate_candidates[i]=abs(rate_candidates[i]-sgst_pos)
	
	
	sorted_rate_cand=sorted(rate_candidates.items(),key=lambda x:x[1])
	rate_occ=sorted_rate_cand[0][0]-1
	count=0
	col_no=None
	for j in range(0,len(table1_lines[0])):
		if ('rate'.lower() in table1_lines[0][j].lower()):
			if(count==rate_occ):
				col_no=j
				break
			else:
				count+=1
	if(col_no)==None:
		return []
	#print(col_no)
	sgst_rates=[]
	for i in table1_lines[1:]:
		if(len(i[col_no])>=1 and i[col_no][0].isnumeric()):
				sgst_rates.append(i[col_no])	
	if(table2_exists):
		for i in table2_lines[1:]:
			if(len(i[col_no])>=1 and i[col_no][0].isnumeric()):
				sgst_rates.append(i[col_no])
	return (sgst_rates)
	
	

sgst_rates=sgst_csv(list_of_words,text_file_lines,table1_lines,table2_exists, table2_lines)
print("SGST %: ",sgst_rates)
"""
CGST %
Invoice 4- 
	check the column which has 'SGST Rate'
	REALLY BAD QUALITY.
	Sgst got read as '333T Bats'
	the scanned copy is of vv poor quality :(
INvoice 3-
	hasn't got ANY SGST :(
INvoice 2-
	hasn't got ANY SGST :(
INvoice 1-
	has both sgst and cgst but it is not recognized in the table.
	so i'll find 'sgst' in the .txt file
	find which 'rate' it is closer to
	mark the rate by a number (1st/2nd/3rd)
	find that occurence in that headings column
	add all the values below it to a list of SGST values	
"""
def cgst_csv(list_of_words,text_file_lines, table1_lines, table2_exists, table2_lines):
	rate_candidates=dict()
	count=1
	"""for loop below is to find the word rate and rank them in order of their occurence"""
	for i in list_of_words:
		if ('rate'.lower() in i.lower() or 'rato'.lower() in i.lower()):
			rate_candidates[count]=0
			count+=1
	
	count=1		
	for i in range(0,len(text_file_lines)):
		if ('rate'.lower() in text_file_lines[i].lower() or 'rato'.lower() in text_file_lines[i].lower()):
			#print(text_file_lines[i])
			rate_candidates[count]=i
			count+=1
	
	#rint(rate_candidates)
	if(len(rate_candidates)==0):
		return []
	sgst_pos=None
	for i in range(0,len(text_file_lines)):
		if('cgst'.lower() in text_file_lines[i].lower() or 'cost'.lower() in text_file_lines[i].lower()):
			sgst_pos=i
			break
	if(sgst_pos==None):
		return []
	for i in rate_candidates:
		rate_candidates[i]=abs(rate_candidates[i]-sgst_pos)
	
	
	sorted_rate_cand=sorted(rate_candidates.items(),key=lambda x:x[1])
	rate_occ=sorted_rate_cand[0][0]-1
	count=0
	col_no=None
	for j in range(0,len(table1_lines[0])):
		if ('rate'.lower() in table1_lines[0][j].lower()):
			if(count==rate_occ):
				col_no=j
				break
			else:
				count+=1
	if(col_no)==None:
		return []
	#print(col_no)
	sgst_rates=[]
	for i in table1_lines[1:]:
		if(len(i[col_no])>=1 and i[col_no][0].isnumeric()):
				sgst_rates.append(i[col_no])	
	if(table2_exists):
		for i in table2_lines[1:]:
			if(len(i[col_no])>=1 and i[col_no][0].isnumeric()):
				sgst_rates.append(i[col_no])
	return (sgst_rates)
	
	

cgst_rates=cgst_csv(list_of_words,text_file_lines,table1_lines,table2_exists, table2_lines)
print("CGST %: ",cgst_rates)
"""
"""
def igst_txt(table1_lines):
	col_no=None
	for j in range(0,len(table1_lines[0])):
		
		if 'igst'.lower() in table1_lines[0][j].lower():
			col_no=j
	#print(col_no)
	if(col_no==None):
		return []
	igst_rates=[]
	if(len(table1_lines[1][col_no])>5 or len(table1_lines[1][col_no])<1):
			col_no-=1
	for i in table1_lines[1:]:
		if(len(i[col_no])>=1):
			igst_rates.append(i[col_no])
	return igst_rates
igst_rates=igst_txt(table1_lines)
print("IGST %:", igst_rates)
"""
"""
def total_txt(table1_lines, table2_exists, table2_lines):
	for i in range(0,len(table1_lines[0])):
		if(len(table1_lines[0][i])==0 and len(table1_lines[1][i])==0):
			break
		last_row=i
		
		#print(len(i))
		#print(i[len(i)-1])
	total=[]
	for i in table1_lines:
		if(len(i[last_row])>=1):
			if(i[last_row][0].isnumeric()):
				total.append(i[last_row])
	if(table2_exists):
		if(len(table2_lines)>last_row):
			for i in table2_lines:
				if(len(i[last_row])>=1):
					if(i[last_row][0].isnumeric()):
						total.append(i[last_row])
	return total
total=total_txt(table1_lines, table2_exists, table2_lines)
print("Total :",total)
def get_headers(text_file_lines,table1_exists,df_table1,table2_exists,df_table2):
        if(table1_exists):
                l=[(i.strip("\n")).lower() for i in text_file_lines]
                index=-1
                if("si" in l):
                    index=l.index("si")
                elif("sl.no" in l):
                    index=l.index("sl.no")
                elif("sl no" in l):
                    index=l.index("sl no")
                elif("sl" in l):
                    index=l.index("sl no")
                if(index!=-1):
                    i=index+1
                    numindex=-1
                    numcheck=1
                    while(i<len(l) and numcheck):
                        numindex=i
                        if(l[i].isdigit()):
                            numcheck=0
                        i+=1
                    if(numindex!=-1):
                        no_of_columns=numindex-index-2
                        try:
                            last_column=df_table1.columns[len(df_table1.columns)-2]
                            first_column=df_table1.columns[0]
                            li=l.index(last_column.lower().strip())
                            if(li<numindex):
                                cols=t[li-no_of_columns+1:li+1]
                                cols.append("")
                                df_table1.columns=cols
                                if(table2_exists):
                                        if(len(df_table1)==len(df_table2)):
                                            df_tablebleable2.columns=df_table1.columns
                        except:
                                print("")
get_headers(text_file_lines,table1_exists,df_table1,table2_exists,df_table2)
def table_content(df_table1,table2_exists,df_table2,sym_spell,pd):
    l=[i.lower().strip(' ') for i in df_table1.columns]
    cols_name=dict()
    # max edit distance per lookup (per single word, not per whole input string)
    max_edit_distance_lookup = 2
    cols=['Product code','HSN','Title','Quantity','Unit Price']
    for i in l:
        input_term = i
        suggestions = sym_spell.lookup_compound(input_term,max_edit_distance_lookup)
        for suggestion in suggestions:
            j=suggestion.term
        if(('material' in i) or ('product code') in i):
            cols_name.update({df_table1.columns[l.index(i)]:cols[0]})
        elif(('hsn' in i) or ('code'==i)):
            cols_name.update({df_table1.columns[l.index(i)]:cols[1]})
        elif(('description' in i) or('description' in j) or('daecripiior' in i) or('dascettion' in i)):
            cols_name.update({df_table1.columns[l.index(i)]:cols[2]})
        elif(('quantity' in i) or ((('qty' in i)or ('oty' in i)))):
            cols_name.update({df_table1.columns[l.index(i)]:cols[3]})
        elif(('Unit price' in i) or ('rate'==i) or("per unit" in i)):
            cols_name.update({df_table1.columns[l.index(i)]:cols[4]})
    df_table1=df_table1.rename(columns=cols_name)
    if(len(df_table1.columns)==len(df_table2.columns)):
        df_table2.columns=df_table1.columns
        df_table1=pd.concat([df_table1,df_table2])
    df_table1.drop(df_table1.columns.difference(cols),axis=1,inplace=True)
    if(len(df_table1.columns)!=len(cols)):
            for i in cols:
                    if(i not in df_table1.columns):
                            df_table1[i]=[pd.NA for k in range(len(df_table1))]
    return df_table1
df_table1=table_content(df_table1,table2_exists,df_table2,sym_spell,pd)
no_of_rows=len(df_table1)
total.extend(['' for i in range(no_of_rows-len(total))])
discounts.extend(['' for i in range(no_of_rows-len(discounts))])
cgst_rates.extend(['' for i in range(no_of_rows-len(cgst_rates))])
igst_rates.extend(['' for i in range(no_of_rows-len(igst_rates))])
sgst_rates.extend(['' for i in range(no_of_rows-len(sgst_rates))])
df=pd.DataFrame({"Total":total,"Discount":discounts,"CGST Rates":cgst_rates,"IGST Rates":igst_rates,"SGST Rates":sgst_rates})
df_table1=df_table1.join(df)
if('SL.no' not in df_table1.columns):
        df_table1.insert(0,'S.no',df.index+1)
print(df_table1)
with open('Invoice_output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Seller ID",seller_info['Seller ID'],"Invoice Date",seller_info['Invoice Date']])
    writer.writerow(["Seller Name",seller_info['Seller Name'],"Due Date",seller_info['Due Date']])
    writer.writerow(["Seller Address",seller_info['Seller Address'],"Total Invoice amount entered by WH operator", seller_info['Total Invoice amount entered by WH operator']])
    writer.writerow(["Seller GSTIN Number",seller_info['Seller GSTIN Number'],"Total TCS collected by WH operator", seller_info['Total TCS collected by WH operator']])
    writer.writerow(["Country of Origin",seller_info['Country of Origin'],"Round off charges", seller_info['Round off charges']]) 
    writer.writerow(["Currency",seller_info['Currency'],"PO Number", seller_info['PO Number']]) 
    writer.writerow(["Description",seller_info['Description'],"Invoice Items Total Amount", seller_info['invoice amount']]) 
    writer.writerow(["","","Invoice Items total quantity", seller_info['invoice qty']]) 
    writer.writerow(["","","Buyer GSTIN Number", seller_info['gstin']+'\n'])
    writer.writerow(df_table1)
    for index,row in df_table1.iterrows():
            writer.writerow(row)

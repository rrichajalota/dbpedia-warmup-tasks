#Chatbot that translates arabic numbers to roman number

from collections import OrderedDict

def int_to_roman(arabic_num):
    romanDict = OrderedDict()
    romanDict[1000] = "M"
    romanDict[900] = "CM"
    romanDict[500] = "D"
    romanDict[400] = "CD"
    romanDict[100] = "C"
    romanDict[90] = "XC"
    romanDict[50] = "L"
    romanDict[40] = "XL"
    romanDict[10] = "X"
    romanDict[9] = "IX"
    romanDict[5] = "V"
    romanDict[4] = "IV"
    romanDict[1] = "I"

    #iterate over all numbers in the list
    result = []

    for num in arabic_num:
        
        roman_str = ""
    	if num <= 0:
    		return "Invalid number"

    	while (num !=0):
    		for base in romanDict.keys():
    			if base <= num:
    				quot = num / base
    				num = num % base
    				roman_str += romanDict[base]*quot
    	
        result.append(roman_str)

    return result	

def extract_numbers(query): #extracts numbers from the query
    numbers = [int(q) for q in query.split() if q.isdigit()]
    return numbers


def welcome():
	print "Hi! This is a simple chatbot which translates arabic numbers to roman numbers."


if __name__ == "__main__":

    welcome()

    while(1):
        query = raw_input("Enter your query (press 0 to exit): ") 

        if query == '0':
            break

        arabic_num = extract_numbers(query)

        if len(arabic_num) == 0:
            print "Invalid query"
            continue 

        roman_num = int_to_roman(arabic_num)

        for num in roman_num:
            print num ,

        print 
        

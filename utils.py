import datetime as dt

def bubble_sort(values : list, sort_two_dimensions=False, index_of_element_in_subarray_to_compare=1, remove_non_numerical_values=True):
    """
    -A sorting algorithm for ordering numeric values in a list by swapping adjacent values. When a pass is completed without any swaps then the list is in the correct order.
    -It has a Big O notation of n^2 so isn't the most efficient but is suitable for small amounts of values; it is mainly used in the function detect_connected_components_sorted
        in the intelligence.py file where the largest number of items to sort through is only a few hundred which isn't too severe.
    -The algorithm is adapted so that it can deal with 2D-arrays if needed; the primary reason for this is in the intelligence module where key-value-pairs of a dictionary
        need sorting based on their values which can be done by zipping the dictionary and then applying a bubble sort on the 2D list created from the zipping, comparing values
        specified in the subarrays - if the subarrays contain a key at index 0 and a value at index 1 then the index of the element in the subarray to compare will be 1.
        The default settings if only a list is input for this function is to sort it as if it is 1-dimensional.
    :params: 
        =values - a list of numerical values to order
        =sort_two_dimensions - an optional argument which defaults to False; it allows the user to specify if the array being sorted is 1 dimensional or 2 dimensional. If it
            is 2 dimensional then you need to pick what value in the subarrays is being compared with each subsequent comparison - it is defaulted to the item at index 1 due to
            the primary focus of this function being to sort a zipped dictionary by its values.
        =index_of_element_in_subarray_to_compare - specifies which element in each of the subarrays is being used to make the comparisons for swaps if the array is 2 dimensional
        =remove_non_numerical_values - in the medianvalue function, a bubblesort is used to order the elements and then locate the median. If the list contains non-numerical values
            then we want to find the median of just the numbers present and not attempt to find the median of non-numerical values, hence a new list is created with non-floats / non-ints
            removed. By default, it is set to True so for cases where it isn't needed due to a list definitely being numerical, one should make sure it is False as it saves some time on 
            unnecessary comparisons.
    :return: the same list of values but in the correct numerical order
    """
    swaps_performed = 0
    pass_required = True
    if remove_non_numerical_values:
        new_values = []
        for each in values:
            try:
                each = float(each)
                new_values.append(each)
            except:
                a = 1   #filler code - if a value isn't a number, it just simply doesn't get added to the new list
        values = new_values
    while pass_required == True:
        swaps_performed = 0
        for i in range(0, len(values)-1):
            if sort_two_dimensions:
                condition = values[i][index_of_element_in_subarray_to_compare] > values[i+1][index_of_element_in_subarray_to_compare]   #defaults index to 1
            else:
                condition = values[i] > values[i+1]
            if condition:
                swaps_performed += 1
                temp = values[i]
                values[i] = values[i+1]
                values[i+1] = temp
        if swaps_performed > 0:
            pass_required = True
        else:
            pass_required = False
    return values

def validate_date(date : str):
    """"
    -Uses the datetime library to attempt converting a user-inputted date (YYYY-MM-DD) into a date-time object in order to verify if it is a real date or not
    :params: a user-inputted date as a string
    :return: if it isn't in the csv files or a real date then false is returned, else the date string is converted to a datetime object and returned
    """
    try:
        return dt.date(year = int(date[0:4]), month = int(date[5:7]), day = int(date[8:]))
    except:
        return False 

def sumvalues(values : list):
    """Takes in a list of numerical values and returns the sum of the values; if non-numerical values are present then the return will still have the sum of the numerical values but will also contain a count for how many invalid values were present
    :params: values - a list of values
    :return: the sum of the values, or a list of format [sum_of_numerical_values_present, number_of_invalid_values_present]
    """ 
    sum = 0   
    invalidList = False
    invalidValueCount = 0
    for each in values:
        try:
            sum += float(each)
        except:
            invalidList = True  #a non numerical value has been detected - the list will still be summed but there will be an extra return value which counts how many non-numerical values were supplied to the function
            invalidValueCount += 1
    if(invalidList):
        return [sum, invalidValueCount]
    else:
        return sum

def maxvalue(values):
    """Takes in a list and returns the index of the highest numerical value; if there are non-numerical values present then it raises an exception and returns the highest value it could find,
        as well as the string 'contains invalid data' as a list
    :params: values - the list of values of which to find the highest value's index
    :return: the index of the highest number in the list, unless the list contains non-numerical values in which case a two-value list is returned:
         - the first value is the index of the highest numerical value in the list, the second is the number of invalid data found in the list
    """
    invalidDataFound = 0
    index_of_maxvalue = 0
    largest_value_found = 0
    for i in range(0, len(values), 1):
        try:
            value = float(values[i])
            if(value > largest_value_found):
                index_of_maxvalue = i
                largest_value_found = value
        except:
             #list contains non-numerical values
            invalidDataFound = True
    if(invalidDataFound):
        index_of_maxvalue = [index_of_maxvalue, 'contains invalid data']
    return index_of_maxvalue


def minvalue(values):
    """Takes in a list and returns the index of the lowest numerical value; if there are non-numerical values present then it raises an exception and returns None
    :params: values - the list of values of which to find the lowest value's index
    :return: the index of the lowest number in the list, unless the list contains non-numerical values in which case None is returned
    """    
    invalidList = False
    index_of_minvalue = 0
    for i in range(0, len(values)):
        if(i != len(values)-1):
            try:
                if(values[i] > values[i+1]):
                    index_of_minvalue = i + 1
            except:
                print("No comparison of adjacent values could be performed - list must contain non-numerical values")
                invalidList = True
    if(invalidList):
        index_of_minvalue = None
    return index_of_minvalue

def medianvalue(values):
    """Finds the median of a set of numerical values; if the set contains non-numbers, then they are removed and a median is found from the numerical values that were in the list
    :params: values - list of numbers (ints or floats)
    :return: the median value of the list values
    """
    if len(values) == 1:
        median = values[0]
    else:
        try:
            values = bubble_sort(values, False, 0, False)   #runs a bubble sort assuming all values are numbers as in theory it should be quicker
        except:
            values = bubble_sort(values, False, 0, True) #the bubble_sort algorithm has thrown an error so evidently it contains non-numbers, hence they need removing from the list and a new bubble_sort to be performed
        n = len(values)-1
        if len(values) % 2 == 0:
            #median is inbetween the middle two values --> directly inbetween values[n/2] and values[n/2  + 1] where n = len(values)-1
            median = (values[int(n/2)] + values[int((n/2) + 1)]) / 2 #the median of a list where the total number of values is even is the midpoint of the two middle values
        else:
            #median is the middle number; i.e. if n is the size of the array, then median = values[ (n+1) / 2 ]
            median = values[int((n+1) / 2)]
    return median

def meannvalue(values : list):
    """Finds the mean average of a set of data in the form of numbers. If the values supplied contain non-numerical pieces of data then the sumvalues function used will return a list of size 2.
     The first item is the sum of the numerical data present; the second item refers to the number of non-numerical pieces of data present in values. This results in the meannvalue function only
     finding the mean average of the numerical data, taking into account the presence of invalid data in the array and subtracting this from the size when doing the calculation.
     EXAMPLE: in a list [1, 2, 3, 'a'], the sumvalues would return [6, 1] whereby six is the sum of the valid data and 1 is the number of false data. meannvalue would then perform the calculation
     sum[0] / len(values) - sum[1] to account for the invalid data, i.e. it would do 6 / (4-1) as there are only 3 numbers to take an average of --> 6 / 3 = 2
        :params: values - a list of numbers (ints or floats) to sum and find the mean of
        :return: the mean average, i.e. sum(values) / total number of pieces of data in values
    """
    sum = sumvalues(values)
    if isinstance(sum, float):
        #the sumvalues part did not have any issues with non-numerical values being present in the list it was supplied with
        return float(sum) / len(values)
    else:
        #if the sumvalues function returns anything other than an integer (the only other possibility of something being returned is a list according to the defintion of sumvalues), then the list of values supplied contains non-numerical data so this needs to be taken into account
        try:
            return float(sum[0]) / (len(values) - sum[1])   #sum[1] refers to the total number of non-numerical data in values; to take an average of what numerical data is present, you need to sum that data and then omit the non-numeric data
        except:
            #if the try part can't run then it is because of a 0/0 error, meaning no numerical data is in the list at all, thus no average can be taken and so the return value is None
            return None




def countvalue(values,xw):
    """A function that receives a list/array "values" and a value "xw" and returns
the number of occurrences of the value "xw" in the list/array "value". If the value isn't present then the function returns 0.
    :params: values - the list of values to search through; xw - the value to check for instances of.
    :return: the number of times the specified value "xw" appears in the list "values" """
    count = 0
    for each in values:
        if(each == xw):
            count += 1
    return count

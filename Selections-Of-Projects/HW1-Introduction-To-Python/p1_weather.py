#!/usr/bin/env python
# coding: utf-8

# In[16]:


def manhattan_distance(datapoint1, datapoint2):
    # Get the values from each dict
    value_list1 = datapoint1.values()
    value_list2 = datapoint2.values()

    # Get the values of the key "TMAX"
    xPoint1 = datapoint1.get("TMAX") 
    xPoint2 = datapoint2.get("TMAX")
    
    # Get the values of the key "PRCP"
    yPoint1 = datapoint1.get("PRCP")
    yPoint2 = datapoint2.get("PRCP")

    # Get the values of the key "TMIN"
    zPoint1 = datapoint1.get("TMIN")
    zPoint2 = datapoint2.get("TMIN")
    
    # Calculate the Manhattan distance.
    d = abs(xPoint1 - xPoint2) + abs(yPoint1 - yPoint2) + abs(zPoint1 - zPoint2)
    
    return d


# In[17]:


def read_dataset(filename):
    # Define necessary variables
    file = open(filename, 'r')
    dataList = []
    
    # Read lines from the file 
    while True:
        lines = file.readline()
        # Check if the line is empty
        if not lines: 
            break      
        # Split the line based on space
        lines = lines.split(' ')
        # Define the dict by using the values read from the file
        dict_element = {'DATE': lines[0], 'TMAX': float(lines[2]), 'PRCP': float(lines[1]), 'TMIN': float(lines[3]), 'RAIN':  lines[4].strip('\n')}
        # Append the dict to the list
        dataList.append(dict_element)
      # Stop reading the file  
    file.close()

        
    return dataList


# In[18]:


def majority_vote(nearest_neighbors):
    # Define needed variables
    rain = 0
    not_rain = 0
    result = 'FALSE'
    
    # Get the value of the key "RAIN" and calculate the numbers of "TRUE" and "FALSE"
    for dict in nearest_neighbors:
        # Get the value of the key "RAIN"
        if_rain = dict.get("RAIN")
        # Calculate the numbers of "TRUE" and "FALSE"
        if if_rain == 'TRUE':
            rain += 1
        else:
            not_rain += 1
     
    # Compare the numbers of "TRUW" and "FALSE" to get the result
    if rain < not_rain:
        result = 'FALSE'
    else:
        result = 'TRUE'
        
    return result


# In[48]:


def k_nearest_neighbors(filename, test_point, k, year_interval):
    # Deine needed variables
    element_list = read_dataset(filename)
    test_year = test_point.get("DATE")
    test_year = test_year[0:4]
    num_of_correct_year = 0
    correct_year_list = []
    result = 'FALSE'
    final_list = []
    number = 0
    
    # Find the valid years
    for element in element_list:
        year = element.get("DATE")
        year = float(year[0:4])
        
        # If the date is the same as the test_point, continues the loop
        if test_point.get("DATE") == element.get("DATE"):
            continue
            
        #If the year is valid, append it to the list.
        if (year > float(test_year) - float(year_interval)) and (year < float(test_year) + float(year_interval)):
            correct_year_list.append(element)
 
            
    # Calculate the Manhattan distance of the valid year and take K years
    while number < k:
        # Calcualte a temporary Manhanttan distance to compare it to that of the next one.
        cur_index = 0
        if len(correct_year_list) == 0:
            break
        cur_dist = manhattan_distance(correct_year_list[0], test_point)
        

        # Calcualte the next year's Manhattan distance and compare it to that of the next one
        for i in range(len(correct_year_list) - 1):
            if manhattan_distance(correct_year_list[i+1], test_point) < cur_dist:
                cur_index = i+1
                cur_dist = manhattan_distance(correct_year_list[i+1], test_point)
            
        # Append it to the final_list and delete it from correct_year_list
        final_list.append(correct_year_list[cur_index])
#        print(correct_year_list[cur_index])
#        print(len(final_list))
        correct_year_list.remove(correct_year_list[cur_index])
        number += 1
     
    result = majority_vote(final_list)
    return result


# In[50]:





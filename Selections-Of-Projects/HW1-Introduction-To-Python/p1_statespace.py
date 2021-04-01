#!/usr/bin/env python
# coding: utf-8

# In[4]:


def fill(state, max, which):
    # Make a copy of the state
    copy = [state[0], state[1]]
    
    # Fill the value based one the which
    if which == 0:
        copy[0] = max[0]
    elif which == 1:
        copy[1] = max[1]
        
    return copy


# In[5]:


def empty(state, max, which):
    # Make a copy of the state
    copy = [state[0], state[1]]
    
    # Empty the value based on the which
    if which == 0:
        copy[0] = 0
    elif which == 1:
        copy[1] = 0
        
    return copy
    


# In[6]:


def xfer(state, max, source, dest):
    # Make a copy of the state
    copy = [state[0], state[1]]
    
    # Check the source and the dest
    if source == 0 and dest == 1:
        # Pour the contents of the jug at the index source into the jug 
        # at index dest until the source is empty or the dest is full
        while copy[1] < max[1] and copy[0] > 0:
            copy[1] += 1
            copy[0] -= 1
    elif source == 1 and dest == 0:
        while copy[0] < max[0] and copy[1] > 0:
            copy[0] += 1
            copy[1] -= 1
    
    return copy


# In[32]:


def succ(state, max):
    # Define the needed variables
    copy = [state[0], state[1]]
    
    # Call the fill()
    output1 = fill(copy,max,0)
    list = [output1]
    if_exist = 0
    output2 = fill(copy,max,1)
    # Check if there is a smae result in the list; if not, append the result 
    # to the list 
    for i in list:
        if i[0] == output2[0] and i[1] == output2[1]:
            if_exist = 1
            break
    if if_exist != 1:
        list.append(output2)
    if_exist = 0    
    
    # Call the empty()
    output3 = empty(copy,max,0)
    # Check if there is a smae result in the list; if not, append the result 
    # to the list 
    for i in list:
        if i[0] == output3[0] and i[1] == output3[1]:
            if_exist = 1
            break
    if if_exist != 1:
        list.append(output3)
    if_exist = 0  
    # Call the empty()
    output4 = empty(copy,max,1)
    # Check if there is a smae result in the list; if not, append the result 
    # to the list 
    for i in list:
        if i[0] == output4[0] and i[1] == output4[1]:
            if_exist = 1
            break
    if if_exist != 1:
        list.append(output4)
    if_exist = 0  
    # Call the xfer()
    output5 = xfer(copy,max,0,1)
    # Check if there is a smae result in the list; if not, append the result 
    # to the list 
    for i in list:
        if i[0] == output5[0] and i[1] == output5[1]:
            if_exist = 1
            break
    if if_exist != 1:
            list.append(output5)
    if_exist = 0  
    # Call the xfer()
    output6 = xfer(copy,max,1,0)
    # Check if there is a smae result in the list; if not, append the result 
    # to the list 
    for i in list:
        if i[0] == output6[0] and i[1] == output6[1]:
            if_exist = 1
            break   
    if if_exist != 1:
            list.append(output6)
    if_exist = 0  
        

    
    print(list)


# In[ ]:





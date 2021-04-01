#!/usr/bin/env python
# coding: utf-8

# In[26]:


# given a state of the board, return a list of all valid successor states
def succ(state, static_x, static_y):
    returned_list = []
    n = len(state)
    
    # check if there is no queen on the static point
    if not(state[static_x] == static_y):
        returned_list = []
    else:
        for i in range(0,n):
            if i == static_x:
                continue
            else:

                if state[i] == n-1:
                    child1 = move_down(state,i)
                    returned_list.append(child1)
                elif state[i] == 0:
                    child1 = move_up(state, i)
                    returned_list.append(child1)
                else:
                    child1 = move_up(state, i)
                    child2 = move_down(state, i)
                    returned_list.append(child1)
                    returned_list.append(child2)
                    
#    print(sorted(returned_list))
    returned_list = sorted(returned_list)
    return returned_list
                    
def move_up(state,i):
    child_state = []
    child_state = state.copy()
    child_state[i] +=  1
    return child_state

def move_down(state,i):
    child_state = []
    child_state = state.copy()
    child_state[i] -=  1
    return child_state  

def f(state):
    f = 0
#    print(state)
    n = len(state)
    chessboard = state.copy()
    
    for i in range(0,n):
#        print(i)
        if check_pos_row(state,i, n) or check_neg_row(state, i) or check_up_diagonal(state, i, n) or check_down_diagonal(state, i): 
            f = f + 1
#            print("f=",f)
#    print(f)
    return f

def check_pos_row(state, i, n):
    if_attacted = False
    j = i
#    print(i)
    while j+1 < n:
        if state[i] == state[j+1]:
            if_attacted = True
#            print(state[j],state[j+1])
#            print("pos_row")
            break
        j += 1

    return if_attacted

def check_neg_row(state, i):
    if_attacted = False
    j = i
    while j - 1 >= 0:
        if state[i] == state[j-1]:
#            print(state[j-1],state[i])
            if_attacted = True
#            print("neg_row")
            break
        j -= 1
    return if_attacted

def check_up_diagonal(state, i, n):
    if_attacted = False
    j = i
    while j < n:
        if abs(state[i] - state[j]) == abs(i-j) and i !=j:
#            print(state[i],state[j])
            if_attacted = True
#            print("up_dia")
            break
        j += 1
    return if_attacted

def check_down_diagonal(state, i):
    if_attacted = False
    j = i
    while j >=0:
        if abs(state[i] - state[j]) == abs(i-j) and i !=j:
            if_attacted = True
#            print("down_dia")
            break
        j -= 1
    return if_attacted

# given the current state, use succ() to generate the successors and return the selected next state
def choose_next(curr, static_x, static_y):
    state_list = succ(curr, static_x, static_y)
    f_state_list = []
    returned_state = None
    
#    print(state_list)
#    print(len(state_list))

    # check if the state list is an empty list
    if len(state_list) == 0:
        returned_state = None
    else: 
        state_list.append(curr)
        f_n = 0
        for i in range(0,len(state_list)):
            f_n = f(state_list[i])
            f_state_list.append((f_n, state_list[i]))
        
        f_state_list = sorted(f_state_list)
        returned_state = f_state_list[0][1]
#    print(f_state_list)
#    print(returned_state)
    return returned_state        
    
# run the hill-climbing algorithm from a given initial state, return the convergence state
def n_queens(initial_state, static_x, static_y, print_path=True):
    succ_list = []
    succ_list.append((f(initial_state), initial_state))
    f_prev_state = f(initial_state)
    returned_state = []
    
    cur_state = choose_next(initial_state,static_x, static_y)
    if not(cur_state == None):
        f_cur_state = f(cur_state)
        succ_list.append((f_cur_state, cur_state))
    
        while f_cur_state != f_prev_state and f_cur_state != 0:
#        print(cur_state)
            f_prev_state = f_cur_state
            cur_state = choose_next(cur_state,static_x, static_y)
            f_cur_state = f(cur_state)
            succ_list.append((f_cur_state, cur_state))
#        print(cur_state)
        
        succ_list = sorted(succ_list, reverse=True)
        
        if print_path == True:
            for i in succ_list:
                print(i[1], 'f=%d' %i[0])
                
        returned_state = succ_list[len(succ_list)-1][1]

        
    
    
#    for i in succ_list:
#        print(i[1], "f=", i[0])
#    print(returned_state)
    return returned_state
        
    
import random

def n_queens_restart(n, k, static_x, static_y):
    random.seed(1)
    initial_state = []
    returned_state = []
    returned_f = 0
    
    # generate an initial state by using Python's random module
    for i in range(0,n):
        if i == static_x:
            initial_state.append(static_y)
        else:
            m = random.randint(0, n-1)
            initial_state.append(m)
    cur_state = initial_state
    
    # start the for-loop for k times
    for j in range(0,k):
#        print(cur_state)
        cur_state = n_queens(cur_state, static_x, static_y, print_path=False)
        f_cur = f(cur_state)
        
        returned_f = f_cur
        returned_state = cur_state
        
        # check if the problem is solved with an f() value of 0; if so, break the loop
        if f_cur != 0:
#            print("a new initial state")
            temp_state = []
#            print(n)
            for i in range(0,n):
#                print(i)
                if i == static_x:
                    temp_state.append(static_y)
                else:
                    m = random.randint(0, n-1)
                    temp_state.append(m)
#            print(temp_state)
            cur_state = temp_state

        else:
            break
            
            
    print(returned_state, 'f=%d' %returned_f)
    
    
    
    
            
        


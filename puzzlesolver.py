from jugs import jugs_get_successor_state
from jugs import jugs_check_goal
import copy
import sys

class configstruct:
    N = 0
    capacity = []

def dfs(ans,config,check_goal):
    TH = config.N * 10 #threshold for checking current state possible investigation
    lvl = 1 #level of track back on graph path
    counter = 1 #counter for checking with TH
    early_state = copy.deepcopy(ans[0]) #the early state to check if after TH iterations has changed or not
    stack = []
    stack.append(ans)
    while(len(stack)>0):
        ans = copy.deepcopy(stack.pop()) #get the next graph ndoe to search
        stack.append(copy.deepcopy(ans))#take it back to stack so we can reach for other possible investigation
        state = ans[len(ans)-1]
        if(check_goal(state,config)): #check if the goal has been reached
            return ans #here is the answer, toss it back
        else: #get next possible move 
            #retrive last state of ans
            state = get_successor_state(ans[len(ans)-1],config) #next possible move
            #check if there is previous state like this or not
            sim = [i for (i, x) in enumerate(ans) if list(x)==list(state)]
            #if there is no such state, go on and continue
            if(len(sim)==0):
                ans.append(state)
                #check if this path answer is not already in the stack
                sim = [i for (i, x) in enumerate(stack) if (x)==(ans)]
                if(len(sim)==0):
                    stack.append(copy.deepcopy(ans))
                    #update early state in order to make sure you are chasing the right node
                    early_state = copy.deepcopy(ans)
                else: #if it is in the stack, then remove it
                    stack.pop()
        if(counter==TH):#check the counter
            counter = 0 #reset the counter
            if(lvl>=len(stack)): #if we probably may delete all stack, just to make sure, lower lvl by one
                lvl = len(stack)-1
            if(early_state==ans): #if we were searching for nothing new, delete parent
                for i in range(lvl): #get back to the top of the graph when no more move is possible
                    stack.pop()
                lvl +=1 #add one level for pruning
            else: #if there are some update, keep going
                early_state = copy.deepcopy(stack[len(stack)-1]) #reset early state
                lvl =0 #reset level
        counter +=1 #add one to the counter

#run by input
if (len(sys.argv)>1):
    config = configstruct() #inital config variable
    config_file = open(sys.argv[1]) #get the name of configuration file
    if(config_file.readline(4)=="jugs"):
        get_successor_state = jugs_get_successor_state
        check_goal = jugs_check_goal    
    config_file.readline() #skip newline "\n"
    #reading capacity line
    oldstr = config_file.readline() #read next line
    newstr = oldstr[1:len(oldstr)-2]
    cap = newstr.split(',') #capacity str
    #config_file.readline() #skip newline "\n"
    #reading initial line
    oldstr = config_file.readline() #read next line
    newstr = oldstr[1:len(oldstr)-2]
    init = newstr.split(',') #capacity str
    #config_file.readline() #skip newline "\n"
    #reading goal line
    oldstr = config_file.readline() #read next line
    newstr = oldstr[1:len(oldstr)-1] #since it is the last line we capture len(oldstr)-1 instead of -2
    goal = newstr.split(',') #capacity str
    #set config file
    config.N = len(cap) #number of jugs
    config.capacity#initiating config.capacity
    initial_state = []#initaite array
    config.goal = []
    #converting string to data
    for i in range(len(cap)):
        config.capacity.append(int(cap[i]))
        initial_state.append(int(init[i]))
        config.goal.append(int(goal[i]))     
    if(sys.argv[2]=="dfs"):
        method = dfs
else: #run without input
    ############ initiation test
    initial_state = [0,0]
    get_successor_state = jugs_get_successor_state
    check_goal = jugs_check_goal
    config = configstruct()
    config.N = 2
    config.capacity = [4,3]
    config.goal = [2,0]
    method = dfs

#start part
ans = []
ans.append(initial_state) #to make sure there is a matrix
ans = method(ans,config,check_goal)
print(ans)

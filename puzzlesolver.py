from jugs import jugs_get_successor_state
from jugs import jugs_check_goal
from jugs import cities_check_goal
from jugs import cities_get_successor_state
import copy
import sys
import math

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
    name_str = config_file.readline()
    #print(name_str[0:4])
    if(name_str[0:4]=="jugs"):
        get_successor_state = jugs_get_successor_state
        check_goal = jugs_check_goal    
        #config_file.readline() #skip newline "\n"
        #---------------------------------------noted
        #I bring all previous code under the jugs since for example we don't have capacity for other probelm
        #---------------------------------------noted
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
    elif(name_str[0:6]=="cities"):
        get_successor_state = cities_get_successor_state
        check_goal = cities_check_goal
        #config_file.readline() #skip newline "\n"
        #reading city location information
        oldstr = config_file.readline() #read next line
        newstr = oldstr[1:len(oldstr)-2]
        #store each citiy and location
        city_info = newstr.split('),') #extract each (city,x,y) in one seperate triple
        #when we start seperating all line will be like "(city,x,y" becuase of split
        #last line however is like  "(city,x,y)" so with line below we remove ")" for last string
        city_info[len(city_info)-1] = city_info[len(city_info)-1][0:len(city_info[len(city_info)-1])-1]
        cities = []
        location = []
        for x in city_info:
            temp = x.split(',')
            cities.append(temp[0][2:len(temp[0])-1]) #remove (' + '
            location.append((int(temp[1]),int(temp[2])))
        #config_file.readline() #skip newline "\n"
        #reading initial line
        oldstr = config_file.readline() #read next line
        initial_state = []
        initial_state.append(copy.deepcopy(oldstr[0:len(oldstr)-1])) #name of initial state
        initial_state.append('0') #cost of initial state
        #reading goal line
        oldstr = config_file.readline() #read next line
        config.goal = copy.deepcopy(oldstr[0:len(oldstr)-1])
        #reading path
        oldstr = config_file.readline() #read next line
        #parameters for config
        config.source = []
        config.destination = []
        config.cost = []
        #read each line and process it
        while(len(oldstr)>0):
            #remove paranthesis and []s
            newstr = oldstr[2:len(oldstr)-3]
            oldstr = newstr.split(',') #extract each part using split and ','
            config.source.append(copy.deepcopy(oldstr[0][1:len(oldstr[0])-1])) #store source
            config.destination.append(copy.deepcopy(oldstr[1][1:len(oldstr[1])-1])) #store destination
            #compute distance of these cities and multiply it by cost per unit
            source_ind = [i for (i, x) in enumerate(cities) if x==config.source[len(config.source)-1]]
            destination_ind = [i for (i, x) in enumerate(cities) if x==config.destination[len(config.source)-1]]
            #since source_ind and destination_ind are both list then in the dist computation below we use 
            #source_ind[0] to make it a integer not a list, however we know source_ind has only one value because 
            #there is only one unique city in cities list

            #compute dist based on location of two cities
            dist = math.sqrt(math.pow(location[source_ind[0]][0]-location[destination_ind[0]][0],2)+
                    math.pow(location[source_ind[0]][1]-location[destination_ind[0]][1],2))
            config.cost.append(float(oldstr[2])*dist) #store the cost
            oldstr = config_file.readline() #read next line
            config.N = len(cities)
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

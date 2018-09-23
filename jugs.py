import random
import copy


def jugs_get_successor_state(ST,config):
    N = config.N #number of jugs
     #every single assignment is a pointer so any changes will affect both sides. 
     # i decided to copy the variable to make sure changes only applies to local variable
    state = copy.deepcopy(ST)
    #check if all jugs are empty or not
    if sum(state)==0 : #if all jugs are empty fill one randomly
        i = random.randint(0,N-1)
        state[i] = config.capacity[i]
        return state
    #if there are filled jugs, we go to fill jugs with eachother or empy one of them randomly
    #we also may randomly fill one empty jug
    while(1): #use while to make sure one state has beed added
        ra = random.random()
        if(ra<0.33) : #refill jugs
            #non_empty_jugs = list(x for x in state if x>0)
            non_empty_jugs = [i for (i, x) in enumerate(state) if x>0]
            non_full_jugs = []
            #find those jugs which are not full
            for i in range(N):
                if(state[i]<config.capacity[i]):
                    non_full_jugs.append(i)
            #if there is no empty_jugs or full_jugs then can't continue
            if ( (len(non_empty_jugs)==0) | (len(non_full_jugs)==0) | (set(non_empty_jugs)==set(non_full_jugs)) ):
                continue
            #if(len(non_empty_jugs) == 0 | len(non_full_jugs)==0 ) :
                #continue 
            else:
                #choose one random non_empty jugs
                ind1 = non_empty_jugs[random.randint(0,len(non_empty_jugs)-1)]
                #choose one random non_full jugs
                ind2 = non_full_jugs[random.randint(0,len(non_full_jugs)-1)]
                #refill ind2 by ind1
                #find the empty capacity of current jug by min between ind1,ind2 jugs or possible capacity
                if(ind1!=ind2): 
                    if (state[ind1]+state[ind2]<=config.capacity[ind2]): #if there is enough space for whole jug
                        X = state[ind1]
                    else:
                        X = min([state[ind1],config.capacity[ind2]-state[ind2]]) #if there is not only pour as much as it has spcace or stat[ind1] has water
                    state[ind2] = state[ind2]+X #add water to destination
                    state[ind1] = state[ind1] - X #remove water from source
                    #print("this one!")
                    return state
        elif(ra<0.66): #pour one jugs (empty)
            #non_empty_jugs = list((x for x in state if x>0)) #make generator as list(generator is for searching and finding in arrays)
            non_empty_jugs = [i for (i, x) in enumerate(state) if x>0] #make generator as list(generator is for searching and finding in arrays)
            
            if(non_empty_jugs):
                state[non_empty_jugs[random.randint(0,len(non_empty_jugs)-1)]] = 0
                return state
        else: #fill one empty jugs
           #empty_jugs = list(x for x in state if x==0) 
           empty_jugs = [i for (i, x) in enumerate(state) if x==0]
           if(len(empty_jugs)>0):
               ra = random.randint(0,len(empty_jugs)-1)
               state[empty_jugs[ra]] = config.capacity[empty_jugs[ra]]
               return state

def jugs_check_goal(state,config):
    if(list(state)==list(config.goal)):
        return True
    else:
        return False


#-------------------------------------Cities-------------------------------------------------
def cities_get_successor_state(ST,config):
    state = copy.deepcopy(ST) #copy arument
    #we have cities connection like this config.source = "start if a path" , config.destination = "end of a path"
    #config.cost = cost of that path*distance 
    source_ind = [i for (i, x) in enumerate(config.source) if x==state[0]]
    if(len(source_ind)==1): #only one option
        ra = 0
    else: #more than one option
        ra = random.randint(0,len(source_ind)-1) #select a possible path randomly
    state[0] = config.destination[source_ind[ra]] #select a city as destination
    state[1] = config.cost[source_ind[ra]] #set the cost for the path
    return state

def cities_check_goal(state,config):
    if(state[0]==config.goal): #if the city of current state is equal to goal then we reach the point
        return True
    else:
        return False
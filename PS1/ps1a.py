###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    d={}
    y=[]
    f=open(filename)
    #line by line initliaze a list of cow, weight pairs
    for line in f:
        #make sure the list is empty before doing anything
        y.clear()
        #create a list of pairs to append to the dictionary, separated by commas
        y=line.split(',')
        d[y[0]]=int(y[1])
        
    f.close()
    return d

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    #put the best (by weight) cows first
    cowsCopy=sorted(cows,key=cows.get, reverse=True)
    #initialize a list to hold each inner list of trips
    total_trips=[]
    while cowsCopy:
        #each trip starts weight at 0
        totalweight=0
        #at start of each iteration through the while loop create a new list for the current trip
        current_trip=[]
        #keep track of which cows we have used
        remove=[]
        #greedy algorithm
        for i in range(len(cowsCopy)):
            #if we can add the cow to the current trip, add it
            if cows[cowsCopy[i]]+totalweight<=limit:
                current_trip.append(cowsCopy[i])
                totalweight+=cows[cowsCopy[i]]
                remove.append(cowsCopy[i])
        total_trips.append(current_trip)
        #remove each cow from the list that we have added
        for x in remove:
            cowsCopy.remove(x)
    return total_trips

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    #possible partitions
    possible_parts=sorted(get_partitions(cows))
    trips=[]

    for x in possible_parts:
        trip=[]
        for y in x:
            #create a new empty list for each partition called weights
            weights=[]
            for l in y:
                #add cows weight to weight
                weights.append(cows[l])
            #add the sum of each trip to the trip list
            trip.append(sum(weights))
        #if each entry in trip is less than the limit, than that is a valid trip and we add it to trips
        if all(trip<=limit for trip in trip):
            trips.append(x)
    remove_dupes=[]
    #remove duplicate trips
    for x in trips:
        if x not in remove_dupes:
            remove_dupes.append(x)
    trips_length=[]
    #add the length of each trip to a new list called trips_length
    for x in remove_dupes:
        trips_length.append(len(x))
    #return the trip which has the least length
    return trips_length.index(min(trips_length))



        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.


    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    start=time.time()
    print(len(greedy_cow_transport(load_cows('ps1_cow_data_2.txt'))))
    end=time.time()
    print('Time taken:' + end-start)
    start=time.time()
    print(len(brute_force_cow_transport(load_cows('ps1_cow_data_2.txt'))))
    end=time.time()
    print('Time taken:' end-start)

    pass
x='ps1_cow_data_2.txt'
print(load_cows(x))
print(greedy_cow_transport(load_cows(x)))
print(brute_force_cow_transport(load_cows(x)))
compare_cow_transport_algorithms()

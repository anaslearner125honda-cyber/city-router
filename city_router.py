
from pathlib import Path
import pickle
from collections import deque
import time 

def filepath() :
    home = Path.home()
    foldername = "Anas_graph"
    filename = "graph.txt"
    full_path = home/foldername/filename
    return home,foldername,filename,full_path

def makenew_graphfile() :
    home,foldername,filename,full_path = filepath()
    data = {}
    folder = home / foldername
    folder.mkdir(parents=True,exist_ok=True)
    with open(full_path,"wb") as file2 :
        pickle.dump(data,file2)
    with open(full_path,"rb") as file3 :
        graph = pickle.load(file3)
    return graph

def load_graph() :
    graph = None
    home,foldername,filename,full_path = filepath()
    if full_path.exists() :
        try :
            with open(full_path,"rb") as file1 :
                graph = pickle.load(file1)
        except Exception as e :
            print("#"*60)
            print("YOUR FILE IS CORRUPTED AND CANNOT BE USED.........")
            print("SO PROGRAME RENAME THIS OLD FILE AND MAKE A NEW EMPTY GRAPH FILE...")
            print("#"*60)
            time_str = str(time.time())
            name_ready = "graph_corrupt" + "_" + time_str + ".txt"
            full_path.rename(home / foldername / name_ready)
            graph = makenew_graphfile()
    else :
        graph = makenew_graphfile()
    return graph

def save_graph(graph) :
    home,foldername,filename,full_path = filepath()
    with open(full_path,"wb") as file :
        pickle.dump(graph,file)


def add_city(graph,cityname) :
    graph[cityname] = set()

def add_road(graph,source,destination) :
    graph[source].add(destination)
    graph[destination].add(source)


def shortest_path(graph, src, dst):
    queue = deque([src])
    visit_set = set()
    visit_set.add(src)
    parent_tracker = {src:None}
    while queue :
        itempop = queue.popleft()
        for i in graph[itempop] :
            if i == dst :
                parent_tracker[i] = itempop
                queue = None
                break
            if i in visit_set :
                continue
            queue.append(i)
            visit_set.add(i)
            parent_tracker[i] = itempop
    if dst not in parent_tracker :
        return []
    pathlist_ulti = []
    temp = dst
    while temp is not None :
        pathlist_ulti.append(temp)
        temp = parent_tracker[temp]
    pathlist_seedhi = []
    for i in range(len(pathlist_ulti)-1,-1,-1) :
        pathlist_seedhi.append(pathlist_ulti[i])
    return pathlist_seedhi


def change_graph_fordfs(usergraph) :
    newgraph = {}
    for i in usergraph :
        nlist = []
        for j in usergraph[i] :
            nlist.append(j)
        newgraph[i] = [nlist,0]
    return newgraph

def is_path_possible(usergraph,city1,city2) :
    graph = change_graph_fordfs(usergraph)
    stack = [city1]
    visit_set = set()
    set_stack = set()
    set_stack.add(city1)
    while stack :
        g = graph[stack[-1]]
        if g[1] == len(g[0]) :
            visit_set.add(stack[-1])
            set_stack.remove(stack.pop())
            continue
        nextcity = g[0][g[1]]
        if nextcity == city2 :
            return True
        if nextcity in set_stack or nextcity in visit_set :
            g[1] += 1
            continue
        g[1] += 1
        stack.append(nextcity)
        set_stack.add(nextcity)
    return False


def all_path_possible(usergraph,city1,city2,limit) :
    status = is_path_possible(usergraph,city1,city2)
    if status is False :
        return True,[]
    graph = change_graph_fordfs(usergraph)
    all_results = []   #
    count = 0
    stack = [city1]
    set_stack = set()
    set_stack.add(city1)
    while stack :
        g = graph[stack[-1]]
        if g[1] == len(g[0]) :
            g[1] = 0
            set_stack.remove(stack.pop())
            continue
        nextcity = g[0][g[1]]
        if nextcity == city2 :
            lst = []
            for j in stack :
                lst.append(j)
            lst.append(city2)
            all_results.append(lst)
            count += 1
            g[1] += 1
            if count > limit :
                break
            continue
        if nextcity in set_stack :
            g[1] += 1
            continue
        g[1] += 1
        stack.append(nextcity)
        set_stack.add(nextcity)

    if stack == [] :
        return True,all_results
    
    else :
        all_results.pop()
        return False,all_results



def input_s_d(graph) :
    user1 = input("ENTER SOURCE  CITY      :  ")
    user2 = input("ENTER DESTINATION  CITY :  ")
    city1 = user1.lower().strip()
    city2 = user2.lower().strip()
    empty_line = f"EMPTY SOURCE OR DESTINATION  NOT ALLOWED"
    not_exist1_line = f"THIS  '{city1}'  NOT EXIST IN GRAPH "
    not_exist2_line = f"THIS  '{city2}'  NOT EXIST IN GRAPH "
    same_line = f"SAME SOURCE AND DESTINATION ARE NOT ALLOWED"
    if city1 == "" or city2 == "" :
        return False,None,None,empty_line
    elif city1 == city2 :
        return False,city1,city2,same_line
    elif city1 not in graph :
        return False,city1,city2,not_exist1_line
    elif city2 not in graph :
        return False,city1,city2,not_exist2_line
    return True,city1,city2,None

def input_c(graph) :
    userinput = input("ENTER CITY NAME  :  ")
    clean_input = userinput.lower().strip()
    empty_line = f"THIS  '{clean_input}' DONT SAVE BECAUSE YOUR INPUT IN EMPTY"
    exist_line = f"THIS  '{clean_input}'  ALREADY EXIST SO THIS INPUT IS NOT SAVE"
    if clean_input == "" :
        return False,None,empty_line
    elif clean_input in graph :
        return False,None,exist_line
    return True,clean_input,None

def paths_print(pathslist) :
    print("*"*60)
    for i in pathslist :
        print(i)
    print("*"*60)

def main_func() :
    graph = load_graph()
    allpaths_limit = 200
    print("="*60)
    print("-------------- WELCOME TO CITY GRAPH FUNCTIONS ---------------")
    print("="*60)
    print("1.TO ADD A CITY IN GRAPH")
    print("2.ADD A ROAD BETWEEN TWO CITIES")
    print("3.TO SEE YOUR FULL GRAPH")
    print("4.FIND SHORTEST PATH BETWEEN TWO CITIES")
    print("5.TO CHECK CONNECTION EXIST BETWEEN TWO CITIES")
    print("6.TO SEE ALL PATHS BETWEEN TWO CITIES")
    print("7.TO EXIT PROGRAM")
    while True :
        userinput = input("CHOOSE YOUR OPTION (1,2,3,4,5,6,7)  :  ")
        user = userinput.strip()
        if user == "1" :
            status,cityname,error_line = input_c(graph)
            if status is True :
                add_city(graph,cityname)
                print(f"THIS  '{cityname}'  HAS BEEN SAVED SUCCESSFULLY ADDED IN GRAPH")
                save_graph(graph)
            else :
                print(error_line)

        elif user == "2" :
            status,city1,city2,error_line = input_s_d(graph)
            if status is True :
                if city2 in graph[city1] :
                    print(f"{city1} <<==>> {city2}  ALREADY EXIST THIS RELATION.SO ITS NOT SAVE")
                else :
                    add_road(graph,city1,city2)
                    print(f"ROAD BETWEEN  {city1}  <<===>>  {city2} HAS BEEN SUCCESSFULLY CREATED")
                    save_graph(graph)
            else :
                print(error_line)

        elif user == "3" :
            if graph == {} :
                print("NOW GRAPH IS EMPTY  : {} ")
            else :
                print("*"*60)
                for i,k in graph.items() :
                    print(f"{i}  ==>> {k}")
                print("*"*60)

        elif user == "4" :
            status,city1,city2,error_line = input_s_d(graph)
            if status is True :
                s_path = shortest_path(graph,city1,city2)
                if len(s_path) == 0 :
                    print(f"{city1} TO {city2}  , NOT POSSIBLE ANY PATH")
                else :
                    print(f"{city1} TO {city2}  , ===>>> {s_path}")
            else :
                print(error_line)

        elif user == "5" :
            status,city1,city2,error_line = input_s_d(graph)
            if status is True :
                result = is_path_possible(graph,city1,city2)
                if result is True :
                    print(f"'{city1}' TO '{city2}'  PATH IS POSSIBLE")
                else :
                    print(f"'{city1}' TO '{city2}'  PATH IS NOT POSSIBLE")
            else :
                print(error_line)

        elif user == "6" :
            status,city1,city2,error_line = input_s_d(graph)
            if status is True :
                status,allpaths = all_path_possible(graph,city1,city2,allpaths_limit)
                if status is True :
                    print(f"************* TOTAL PATHS COUNT : {len(allpaths)} *****************************")
                    if len(allpaths) != 0 :
                        paths_print(allpaths)
                else :
                    print(f"**************  LIMIT EXCEED ONLY '{allpaths_limit}' PATHS YOU CAN SEE ********************")
                    paths_print(allpaths)
            else :
                print(error_line)
             
        elif user == "7" :
            print("THANK YOU FOR USE.GOOD BYE")
            print("="*60)
            break

        else :
            print("YOU ONLY CHOOSE BETWEEN (1--7) OPTION")
        print("-"*60)

if __name__ == "__main__" :
    main_func()

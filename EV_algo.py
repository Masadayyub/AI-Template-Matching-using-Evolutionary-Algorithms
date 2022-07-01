from os import readlink
import random as ran
import numpy as np
from typing import Counter
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as image
import math
import matplotlib.patches as patches

small_img = image.imread('imo2.jpg')
small_dimensions = small_img.shape
small_row = small_dimensions[0]
small_col = small_dimensions[1]


big_img = image.imread('imo1.jpg')
big_dimensions = big_img.shape
big_row = big_dimensions[0]
big_col = big_dimensions[1]


def Sort_Tuple(tuple):
    tuple.sort(key = lambda x: x[2], reverse = True ) 
    return tuple

def binary_conversion(number,bits):
    a = bin(number).replace("0b", "")
    b = a[::-1]
    while len(b) < bits:
        b += '0'
    b = b[::-1]
    return(b)

def max_of_gen(tup_list):
    m_list = []
    for i in range(len(tup_list)):
        mem = tup_list[i]
        ele = mem[2]
        m_list.append(ele)
    maxo = max(m_list)
    return maxo

def avg_tuple(tuple):
    counter = 0
    for i in range(len(tuple)):
        mem = tuple[i]
        ele = mem[2]
        counter = counter + ele

    avg = counter/len(tuple)
    return avg



def pop_initialization(row,column,popsize):
    p_list = []
    for a in range (popsize):
        r = ran.randint(0,row)
        c = ran.randint(0,column)
        x = [r,c]
        p_list.append(x)
    return p_list

def correlation(image1,image2,a):
    x=[]
    y=[]
    fitness=[]
    for i,j in a:
        x.append(i)
        y.append(j)

    for i in range(len(x)):
        if x[i]+small_row<big_row and y[i]+small_col<big_col:
            newlist=image1[x[i]:x[i]+small_row,y[i]:y[i]+small_col]
            corelationvalues=np.corrcoef(image2.ravel(),newlist.ravel())
            fitness.append(corelationvalues[0,1])
        else:
            fitness.append(-1)
    return fitness
    


def fitness_Eval(vals,p_list):
    val = []
    for a in range(len(p_list)):
        member = p_list[a]
        row = member[0]
        col = member[1]
        c_value = vals[a]
        memb = (row,col,c_value)
        val.append(memb)
    return val


def rank_pop(list):
    
    Sort_Tuple(list)
    return list

def Crossover(rankedlist):
    listy = []
    no_1 = 0
    no_2 = 0

    for a in range(len(rankedlist)):
        if no_1 == 0:
            no_1 = rankedlist[a]
        else:
            no_2 = rankedlist [a]
        if no_1 != 0 and no_2 != 0 :
            #for number 1
            row_1 = no_1[0]
            column_1 = no_1[1]
            val_1 = no_1[2]
            row1_b = binary_conversion(row_1,9)
            col1_b = binary_conversion(column_1,10)
            row1_str = str(row1_b) #concatenate the numbers , 1st cnvrt in str then conctenate, then int
            col1_str = str(col1_b)
            new_num1 = row1_str+col1_str #concatenate the row and column for new gen
            rand = ran.randint(0,18) #random number to slice the  binary no each time
            new_num1_i = new_num1[:rand] #slice the concatenated string
            new_num1_ii = new_num1[rand:] #slice the concatenated string

            #for number 2
            row_2 = no_2[0]
            column_2 = no_2[1]
            val_2 = no_2[2]
            row2_b = binary_conversion(row_2,9)
            col2_b = binary_conversion(column_2,10)
            row2_str = str(row2_b) #concatenate the numbers , 1st cnvrt in str then conctenate, then int
            col2_str = str(col2_b)
            new_num2 = row2_str+col2_str #concatenate the row and column for new gen
            new_num2_i = new_num2[:rand]
            new_num2_ii = new_num2[rand:]
            new_num1 = new_num1_i + new_num2_ii
            new_num2 = new_num2_i + new_num1_ii
            new_child_1_i = new_num1[:9]
            new_child_1_ii = new_num1[9:]
            new_child_2_i = new_num2[:9]
            new_child_2_ii = new_num2[9:]
            child1_row = int(new_child_1_i,2) #convert in binary
            child1_col = int(new_child_1_ii,2)
            child_1 = (child1_row,child1_col,val_1)
            child2_row = int(new_child_2_i,2)
            child2_col = int(new_child_2_ii,2)
            child_2 = (child2_row, child2_col,val_2)
            listy.append(child_1)
            listy.append(child_2)
            no_1 = no_2 = 0
    return(listy)


def mutation(list):
    mutated_list = []
    for a in range(len(list)):
        member = list[a]
        row = member[0]
        column = member[1]
        val = member[2]
        row = binary_conversion(row,9)
        col = binary_conversion(column,10)
        row_str = str(row) #concatenate the numbers , 1st cnvrt in str then conctenate, then int
        col_str = str(col)
        rc_str = row_str+col_str

        if member[2] > 0.5:
            rando = ran.randint(10,18)
        else:
            rando = ran.randint(1,9)

        if rc_str[rando] == '0':
            rc_str = rc_str[:rando] + '1' + rc_str[rando+1:]
        else:
            rc_str = rc_str[:rando] + '0' + rc_str[rando+1:]
        
        row = rc_str[:9]
        col = rc_str[9:]
        row = int(row,2)
        col = int(col,2)
        rc_val = (row,col)
        mutated_list.append(rc_val)
    
    return mutated_list


def E_algo():
    gen = 0
    max_gen = 1000
    maxim_cordp = []
    geny  = []
    average = []
    max_pts = []
    pop = pop_initialization(big_row,big_col,100)
    while gen <max_gen:
        cor_values = (correlation(big_img,small_img,pop))
        avg = np.average(cor_values)
        average.append(avg)
        fitness = fitness_Eval(cor_values,pop)
     
        ranked = (rank_pop(fitness))
        
        
        maxi = ranked[0]
        maxo = maxi[2]
        max_pts.append(maxo)
        maxim_cordp.append(maxi)


        if maxo >= 0.82:
            break

        crossed = Crossover(ranked)
        pop = mutation(crossed)


        gen = gen +1
        geny.append(gen)

        

        

        
    # average = avg_tuple(mut_val_ranked)
    maxim_cordp= Sort_Tuple(maxim_cordp)
    
    return maxim_cordp,average,geny,max_pts



a = E_algo()
maxim = a[0]
average = a[1]
geny = a[2]
max_pts = a[3]

max_coordinate = maxim[0]
max_x = max_coordinate[0]
max_y = max_coordinate[1]
max_c = (max_x,max_y)

fig,ax = plt.subplots(1)
rect = patches.Rectangle((max_y,max_x),small_col,small_row, linewidth =2, edgecolor = 'b',fill = False)
ax.imshow(big_img, cmap = "gray")
ax.add_patch(rect)
plt.show()




# plt.plot(max_pts, label = "Max_of_Gen")
# plt.plot(average, label = "Avg_of_Gen")
# plt.xlabel('Generations')
# plt.ylabel('Cor-Values')

# plt.title("EV_Algo Graph")
# plt.legend()
# plt.show()



# Mauro Dell'Amico 9/2023 

import sys
import random

import tsp_utils as tspu

def plot(n, points, dist,s_edges=[],  tit=[]):
    edges = [(i,j) for (i,j) in dist.keys() if i < j ]
    tspu.plot_selectedEdges2D(points, edges, selectededges=s_edges, title=tit, save_fig='Try.png')
    return

############################### MAIN ##################################################
def main():
    #generate and display 2D graphs
    TSPLIB = True # if true reads a TSPLIB instance (name in argv[1])    
           
    if TSPLIB:
        if len(sys.argv) < 2:
            print('\n ** Usage: ShoGraphs.py nameOfTsplibInstanceFile\n\n')
            sys.exit(1)  
        n, points, dist, optTour, optCost = tspu.readTSPLIB(sys.argv[1])
        select = [(optTour[i],optTour[i+1]) for i in range(n-1)] + [(optTour[n-1],optTour[0])]
        plot(n,points,dist,s_edges=select,tit=sys.argv[1])  
    else:
        #random instance 
        if len(sys.argv) < 2:
            print('\n ** Usage: ShowGraphs.py npoints\n\n')
            sys.exit(1)  
            
        n = int(sys.argv[1])        
        # Create a complete Euclidean Graph
        random.seed(91283)
        squareSide = 100
        points,dist  = tspu.randomEuclGraph(n,squareSide)
        # distance is a dictionary where the keys are the edges and the values the corresponding distances
        select = [ (i, (i +1) % n) for i in range(n)] # the tour 0,1,2,...,n-1,0
        plot(n,points,dist,s_edges=select,tit="Complete Euclidean")    
        
        # Create a random geometrical Graph        
        maxDist = 0.3
        #random.seed(9123)
        points,dist  = tspu.randomGraphGeo(n, maxDist)
        plot(n,points,dist,tit="Random Geometric Graph")          

        # Create a random geometrical Graph        
        prob = 0.5
        #random.seed(1243)
        points,dist  = tspu.randomGraph2D(n, prob)
        plot(n,points,dist,tit="Random Graph in 2D")  
        
if __name__ == '__main__':
	main()
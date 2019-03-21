This is my base case using classes for Students, Schools, and Routes.

What I think is nice about this code is that we can easily change the number of busses or capacity of schools by changing the routeInputData and schoolInputData files. 

Right now the code does have some bugs. The route optimization function randomly crashes. I have zipped up the output files from a successful run using only 300 swaps and the results were quite good. The route and their averages can be seen in the routeOutputData file. If we choose to work on this base case or build off of the code, we could run the optimization loops thousands of times and get even better results.

I know the code is not the cleanest or the greatest documentation but it is functioning quite well (minus the part where it crashes) and I like the idea of using classes to seperate out functionality.
# HMO project (won 3rd place)

- Students of FER have possibility to change group for the 
some course they are attending
- Our task was to create optimization procedure to maximize evaluation score

### OPTIMIZATION ALGORITHM DESCRIPTION
My optimization algorithm is made up of three sequential algorithms/procedures
1. greedy algorithm - simple algorithm that iterates over substitution requests
and approves each request if conditions and constraints are satisfied (greedily).
 It is repeated n times (cause some previous invalid requests are valid now after some
    substitutions are made)
2. Direct swaps - After greedy approach, we can't make any more requests.
But we can look if there are requests and examples between pair of students
where each of them wants to go to another's one group and grant both requests and thus
make two substitutions at once
3. Hybrid algorithm:
    - Combination of simulated annealing algorithm and tabu search algorithm
    - main idea: by removing some substitution(request) in current solution maybe we can free space for one 
  or more better substitutions. We ignore removed substitution when looking for new valid substitutions (tabu)
  If we get better solution, we accept it, otherwise we stochastically decide whether we will accept it or not.
  If we accept worse solution, now we remove another substitution(request) from done substitutions (we have a list of 
  removed solutions). By doing this we can succesfully avoid local optimums and find areas with better solutions. 
  The constant improvement of the solution over time is in favor of this thesis.

from ortools.linear_solver import pywraplp
  #        Atlanta Boston Chicago
#Jones       21     23     17
#Goldblum    15     17     13
#Schuldinger 20     17     18
sales = [
    [21, 23, 17],
    [15, 17, 13],
    [20, 17, 18]
]
 #         Atlanta   Boston Chicago
#Jones        65       50      20
#Goldblum     85       65      90
#Schuldinger 100       30      80
allo_cost = [[65, 50, 20],
             [85, 65, 90],
             [100, 30, 80]]
num_workers = len(sales)
num_tasks = len(sales[0])


# print(allo_cost[1][2])
def main():
    # Solver
    # Create the mip solver
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    # x[i, j] is an array of 0-1 variables, which will be 1
    # if worker i is assigned to task j.
    x = {}
    for i in range(num_workers):
        for j in range(num_tasks):
            x[i, j] = solver.IntVar(0, 1, '')
    # Constraints
    # Each worker is assigned to at most 1 task.
    for i in range(num_workers):
        solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) <= 1)

    # Each task is assigned to exactly one worker.
    for j in range(num_tasks):
        solver.Add(solver.Sum([x[i, j] for i in range(num_workers)]) == 1)
   
    # sum of allocation cost must be less than 200
    solver.Add(solver.Sum([allo_cost[i][j] * x[i, j] for i in range(num_workers) for j in range(num_tasks)]) <= 200)
    # Objective
    objective_terms = []
    for i in range(num_workers):
        for j in range(num_tasks):
            objective_terms.append(sales[i][j] * x[i, j])

    solver.Maximize(solver.Sum(objective_terms))
    # Solve
    status = solver.Solve()
    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Total yearly sales is = ', solver.Objective().Value(), '\n')
        for i in range(num_workers):
            for j in range(num_tasks):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if x[i, j].solution_value() > 0.99:
                    print('Worker %d assigned to task %d.  Cost = %d' %
                          (i, j, sales[i][j]))

if __name__ == '__main__':
    main()

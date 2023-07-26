#diogo oliveira

import cvxpy as cp
import numpy as np

eps = 1e-80

# Desativar mensagens de depuração do CVXPY
cp.CVXOPT = False

# Entrada da função objetivo
obj_expr = input("Insira a função objetivo: ")

# Entrada do número de restrições
num_constraints = int(input("Insira o número de restrições: "))

# Lista para armazenar as restrições
constraints = []
constraint_exprs = []  # Lista para armazenar as expressões das restrições

# Variáveis de otimização
x = cp.Variable()
y = cp.Variable()

# Entrada das restrições
for i in range(num_constraints):
    constraint_expr = input(f"Insira a restrição {i+1}: ")
    constraints.append(constraint_expr)
    constraint_exprs.append(eval(constraint_expr, {'x': x, 'y': y}))

# Função objetivo
objective = cp.Maximize(eval(obj_expr, {'x': x, 'y': y}))

# Restrições
all_constraints = [constraint for constraint in constraint_exprs]

# Problema de otimização
problem = cp.Problem(objective, all_constraints)

# Resolvendo o problema
problem.solve(solver=cp.ECOS, verbose=False)

# Extraindo os resultados para o valor máximo
max_value = np.around(problem.value, 6)  # Valor máximo com 6 casas decimais
x_solution_max = np.around(x.value, 6)  # Valor de x para a solução ótima com 6 casas decimais
y_solution_max = np.around(y.value, 6)  # Valor de y para a solução ótima com 6 casas decimais

# Invertendo a função objetivo para encontrar o valor mínimo
objective = cp.Minimize(eval(obj_expr, {'x': x, 'y': y}))

# Problema de otimização para o valor mínimo
problem = cp.Problem(objective, all_constraints)

# Resolvendo o problema para o valor mínimo
problem.solve(solver=cp.ECOS, verbose=False)

# Extraindo os resultados para o valor mínimo
min_value = np.around(problem.value, 6)  # Valor mínimo com 6 casas decimais
x_solution_min = np.around(x.value, 6)  # Valor de x para a solução ótima com 6 casas decimais
y_solution_min = np.around(y.value, 6)  # Valor de y para a solução ótima com 6 casas decimais

# Coordenadas das interseções das restrições
intersection_points = []
intersection_constraints = []

for i in range(num_constraints):
    for j in range(i + 1, num_constraints):
        constraint_i = constraint_exprs[i]
        constraint_j = constraint_exprs[j]
        problem = cp.Problem(cp.Minimize(0), [constraint_i, constraint_j])
        problem.solve(solver=cp.ECOS, verbose=False)
        if problem.status == 'optimal':
            intersection_x = np.around(x.value, 6)
            intersection_y = np.around(y.value, 6)
            intersection_points.append((intersection_x, intersection_y))
            intersection_constraints.append((i + 1, j + 1))

# Exibindo as coordenadas das interseções e suas respectivas restrições
print("Coordenadas das interseções das restrições:")
for i in range(len(intersection_points)):
    print("Restrições:", intersection_constraints[i])
    print("Coordenadas:")
    print("x =", intersection_points[i][0])
    print("y =", intersection_points[i][1])
    print("--------------------------------")

# Exibindo os resultados
print("Valor máximo:", max_value)
print("Solução ótima para o máximo:")
print("x =", x_solution_max)
print("y =", y_solution_max)
print("--------------------------------")
print("Valor mínimo:", min_value)
print("Solução ótima para o mínimo:")
print("x =", x_solution_min)
print("y =", y_solution_min)
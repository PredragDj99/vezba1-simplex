from ortools.linear_solver import pywraplp

def LinearProgrammingExample():
    # Instantiate a Glop solver, naming it LinearExample.
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return

    # Variables should have any non-negative value.
    otpad1 = solver.NumVar(570000, solver.infinity(), "otpad1")
    otpad2 = solver.NumVar(160000, solver.infinity(), "otpad2")
    otpad3 = solver.NumVar(650000, solver.infinity(), "otpad3")

    timeSeconds = 24*60*60

    print("\nNumber of variables(mixtures) =", solver.NumVariables())

    # Constraint 1-3: calorific value between 5 and 20 and target 16 MJ/kg
    kv1 = 2
    kv2 = 3
    kv3 = 1.5
    solver.Add(kv1*otpad1+kv2*otpad2+kv3*otpad3 - 20*(570000+160000+650000) <= 0)  # <=20
    solver.Add(kv1*otpad1+kv2*otpad2+kv3*otpad3 - 5*(570000+160000+650000) >= 0)  # >=5
    solver.Add(kv1*otpad1+kv2*otpad2+kv3*otpad3 - 16*(570000+160000+650000) == 0)  # Target 16

    # Constraint 4: H2O <= 50%
    h1 = 0.03
    h2 = 0.3
    h3 = 0.0375
    solver.Add(h1*otpad1+h2*otpad2+h3*otpad3 - 0.5*(570000+160000+650000) <= 0)

    # Constraint 5: Cl <= 30 000 mg/kg
    cl1 = 245
    cl2 = 376
    cl3 = 204
    solver.Add(cl1*otpad1+cl2*otpad2+cl3*otpad3 - 30000*(570000+160000+650000) <= 0)

    # Constraint 6: S <= 20 000 mg/kg
    s1 = 245
    s2 = 376
    s3 = 2000
    solver.Add(s1*otpad1+s2*otpad2+s3*otpad3 - 20000*(570000+160000+650000) <= 0)

    # Constraint 7: F <= 200 mg/kg
    f1 = 1.7
    f2 = 5
    f3 = 3.9
    solver.Add(f1*otpad1+f2*otpad2+f3*otpad3 - 200*(570000+160000+650000) <= 0)

    # Constraint 8: Hg <= 10 mg/kg
    hg1 = 0.05
    hg2 = 0.15
    hg3 = 0.003
    solver.Add(hg1*otpad1+hg2*otpad2+hg3*otpad3 - 10*(570000+160000+650000) <= 0)

    # Constraint 9: Cd+Tl <= 25 mg/kg
    cd1 = 1.7
    cd2 = 5
    cd3 = 3.9
    solver.Add(cd1*otpad1+cd2*otpad2+cd3*otpad3 - 25*(570000+160000+650000) <= 0)

    # Constraint 10: heavy metals(Cl, Hg, Cd+Tl) <= 2000 mg/kg
    solver.Add((cl1+hg1+cd1)*otpad1+(cl2+hg2+cd2)*otpad2+(cl3+hg3+cd3)*otpad3 - 2000*(570000+160000+650000) <= 0)

    # Constraint 11: ashes <= 40%
    a1 = 0.02
    a2 = 0
    a3 = 0.31
    solver.Add(a1*otpad1+a2*otpad2+a3*otpad3 - 0.4*(570000+160000+650000) <= 0)

    # Constraint 12, 13: Thermal energy
    thermalEnergy1 = 570000/timeSeconds * kv1
    thermalEnergy2 = 160000/timeSeconds * kv2
    thermalEnergy3 = 650000/timeSeconds * kv3
    solver.Add(thermalEnergy1+thermalEnergy2+thermalEnergy3 - 19.8 >= 0)
    solver.Add(thermalEnergy1+thermalEnergy2+thermalEnergy3 - 32.2 <= 0)

    print("Number of constraints =", solver.NumConstraints())

    # Objective function: max{x+y+z}
    solver.Maximize(otpad1+otpad2+otpad3)

    # Solve the system.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("\nSolution:")
        print("Objective value =", solver.Objective().Value())
        print("otpad1 =", otpad1.solution_value())
        print("otpad2 =", otpad2.solution_value())
        print("otpad3 =", otpad3.solution_value())

        print("\nthermalEnergy1 =", thermalEnergy1)
        print("thermalEnergy2 =", thermalEnergy2)
        print("thermalEnergy3 =", thermalEnergy3)

        print("Duration ih hours =", timeSeconds/60/60)
    else:
        print("The problem does not have an optimal solution.")

    print("\nAdvanced usage:")
    print("Problem solved in %f milliseconds" % solver.wall_time())
    print("Problem solved in %d iterations" % solver.iterations())


LinearProgrammingExample()

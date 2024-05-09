#!/usr/bin/env python3


import sys

import random
import time

import networkx as nx

import gurobipy as gp
from gurobipy import GRB

import tsp_utils as tspu


def pairwise(it):
    it = iter(it)
    prev = next(it)
    for cur in it:
        yield prev, cur
        prev = cur


gp.disposeDefaultEnv()

env_params = {
    GRB.Param.ComputeServer: "gurobi-compute-container:61000",
    GRB.Param.WLSTokenDuration: 1,
}

QUIET = False

RANDOM = True  # if True generates a random instance
TSPLIB = True  # if true reads a TSPLIB instance (name in argv[1])
CPP_IN = False # examples from https://github.com/victorX101/min-cost-arborescence/blob/master/code.cpp


def make_pred(n, arcs):
    pred = [None] * n
    for i, j in arcs:
        assert pred[j] is None
        pred[j] = i
    return pred


def find_cycle(n, arcs):
    pred = make_pred(n, arcs)

    for start in range(n):
        order = []
        seen = set()
        cur = start
        while cur is not None:
            if cur in seen:
                # cycle detected
                return order[order.index(cur) :]

            seen.add(cur)
            order.append(cur)
            cur = pred[cur]

    return None


def find_path(n, arcs, max_arcs_in_path):
    pred = make_pred(n, arcs)
    is_leaf = [True] * n
    for i, j in arcs:
        is_leaf[i] = False

    for start in range(n):
        cur = start
        p = []
        while cur is not None:
            p.append(cur)
            if len(p) - 1 > max_arcs_in_path:
                return p[::-1]
            cur = pred[cur]
    return None


def main():
    root = 0
    max_arcs_in_path = 20
    opt_cost = None

    if CPP_IN:
        with open(sys.argv[1]) as in_file, open(sys.argv[2]) as out_file:
            n, root = map(int, next(in_file).strip().split())
            root -= 1
            m = int(next(in_file))
            dist = {}
            for _ in range(m):
                i, j, w = map(int, next(in_file).strip().split())
                dist[i - 1, j - 1] = w
            opt_cost = next(map(int, next(out_file).strip().split()))
        print("Read", n, root, dist, opt_cost)
    elif TSPLIB:
        if len(sys.argv) < 3:
            print("Usage: tsp.py nameOfTsplibInstanceFile\n\n")
            sys.exit(1)
        n, points, dist = tspu.readTSPLIB(sys.argv[1])
    else:
        # random instance
        if len(sys.argv) < 2:
            print("Usage: tsp.py npoints\n\n")
            sys.exit(1)

        n = int(sys.argv[1])
        if RANDOM:
            random.seed(989)
            points, dist = tspu.randomEuclGraph(n, 100)

    g = nx.DiGraph()
    for (i, j), w in dist.items():
        g.add_edge(i, j, weight=w)
    # NOTE: I think this chooses _any_ root, not the one we want
    nx_result = nx.algorithms.tree.branchings.minimum_spanning_arborescence(g)

    if QUIET:
        gp.setParam("OutputFlag", 0)
    else:
        gp.setParam("OutputFlag", 1)

    with gp.Env(params=env_params) as env, gp.Model("arb", env=env) as m:
        arc = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name="arc")
        m.addConstrs(arc.sum("*", j) == 1 for j in range(n) if j != root)
        m.write("/models/arb.lp")

        m.Params.lazyConstraints = 1

        def callback(model, where):
            if where == GRB.Callback.MIPSOL:
                x = model.cbGetSolution(arc)
                selected_arcs = gp.tuplelist(
                    (i, j) for i, j in arc.keys() if x[i, j] > 0.5
                )

                if (c := find_cycle(n, selected_arcs)) is not None:
                    model.cbLazy(
                        gp.quicksum(arc[i, j] for i in c for j in c if (i, j) in arc)
                        <= len(c) - 1
                    )
                    if not QUIET:
                        print(f"\n>>> Cycle eliminated: {c}\n")
                elif (p := find_path(n, selected_arcs, max_arcs_in_path)) is not None:
                    model.cbLazy(
                        gp.quicksum(arc[i, j] for i, j in pairwise(p))
                        <= max_arcs_in_path
                    )
                    if not QUIET:
                        print(f"\n>>> Path eliminated: {p}\n")

        start = time.time()
        m.optimize(callback)
        end = time.time()

        vals = m.getAttr("x", arc)
        selected_arcs = gp.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)

        print("")
        print("Optimal cost", opt_cost)
        print("NetworkX cost", nx_result.size("weight"))
        print("Found solution cost:", m.objVal)
        print("Time", end - start)
        print("Selected:", selected_arcs)
        print("")


if __name__ == "__main__":
    main()

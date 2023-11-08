# utilities.py - AIPython useful utilities
# AIFCA Python code Version 0.9.9 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright 2017-2023 David L. Poole and Alan K. Mackworth
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import random
import math

def argmaxall(gen):
    """gen is a generator of (element,value) pairs, where value is a real.
    argmaxall returns a list of all of the elements with maximal value.
    """
    maxv = -math.inf       # negative infinity
    maxvals = []      # list of maximal elements
    for (e,v) in gen:
        if v>maxv:
            maxvals,maxv = [e], v
        elif v==maxv:
            maxvals.append(e)
    return maxvals

def argmaxe(gen):
    """gen is a generator of (element,value) pairs, where value is a real.
    argmaxe returns an element with maximal value.
    If there are multiple elements with the max value, one is returned at random.
    """
    return random.choice(argmaxall(gen))

def argmax(lst):
    """returns maximum index in a list"""
    return argmaxe(enumerate(lst))
# Try:
# argmax([1,6,3,77,3,55,23])

def argmaxd(dct):
   """returns the arg max of a dictionary dct"""
   return argmaxe(dct.items())
# Try:
# arxmaxd({2:5,5:9,7:7})
def flip(prob):
    """return true with probability prob"""
    return random.random() < prob

def pick_from_dist(item_prob_dist):
    """ returns a value from a distribution.
    item_prob_dist is an item:probability dictionary, where the
        probabilities sum to 1.
    returns an item chosen in proportion to its probability
    """
    ranreal = random.random()
    for (it,prob) in item_prob_dist.items():
        if ranreal < prob:
            return it
        else:
            ranreal -= prob
    raise RuntimeError(f"{item_prob_dist} is not a probability distribution")

def dict_union(d1,d2):
    """returns a dictionary that contains the keys of d1 and d2.
    The value for each key that is in d2 is the value from d2,
    otherwise it is the value from d1.
    This does not have side effects.
    """
    d = dict(d1)    # copy d1
    d.update(d2)
    return d

def test():
    """Test part of utilities"""
    assert argmax([1,6,55,3,55,23]) in [2,4]
    assert dict_union({1:4, 2:5, 3:4},{5:7, 2:9}) == {1:4, 2:9, 3:4, 5:7} 
    print("Passed unit test in utilities")

if __name__ == "__main__":
    test()

def test_aipython():
    # Agents: currently no tests
    # Search:
    print("***** testing Search *****")
    import searchGeneric, searchBranchAndBound, searchExample, searchTest
    searchGeneric.test(searchGeneric.AStarSearcher)
    searchBranchAndBound.test(searchBranchAndBound.DF_branch_and_bound)
    searchTest.run(searchExample.problem1,"Problem 1")
    # CSP
    print("\n***** testing CSP *****")
    import cspExamples, cspDFS, cspSearch, cspConsistency, cspSLS
    cspExamples.test_csp(cspDFS.dfs_solve1)
    cspExamples.test_csp(cspSearch.solver_from_searcher)
    cspExamples.test_csp(cspConsistency.ac_solver)
    cspExamples.test_csp(cspConsistency.ac_search_solver)
    cspExamples.test_csp(cspSLS.sls_solver) 
    cspExamples.test_csp(cspSLS.any_conflict_solver)
    # Propositions
    print("\n***** testing Propositional Logic *****")
    import logicBottomUp, logicTopDown, logicExplain, logicNegation
    logicBottomUp.test()
    logicTopDown.test()
    logicExplain.test()
    logicNegation.test()
    # Planning
    print("\n***** testing Planning *****")
    import stripsHeuristic
    stripsHeuristic.test_forward_heuristic()
    stripsHeuristic.test_regression_heuristic()
    # Learning
    print("\n***** testing Learning *****")
    import learnProblem, learnNoInputs, learnDT, learnLinear
    learnNoInputs.test_no_inputs(training_sizes=[4])
    data = learnProblem.Data_from_file('data/carbool.csv', target_index=-1, seed=123)
    learnDT.testDT(data, print_tree=False)
    learnLinear.test()
    # Deep Learning: currently no tests
    # Uncertainty
    print("\n***** testing Uncertainty *****")
    import probGraphicalModels, probRC, probVE, probStochSim
    probGraphicalModels.InferenceMethod.testIM(probRC.ProbSearch)
    probGraphicalModels.InferenceMethod.testIM(probRC.ProbRC)
    probGraphicalModels.InferenceMethod.testIM(probVE.VE)
    probGraphicalModels.InferenceMethod.testIM(probStochSim.RejectionSampling, threshold=0.1)
    probGraphicalModels.InferenceMethod.testIM(probStochSim.LikelihoodWeighting, threshold=0.1)
    probGraphicalModels.InferenceMethod.testIM(probStochSim.ParticleFiltering, threshold=0.1)
    probGraphicalModels.InferenceMethod.testIM(probStochSim.GibbsSampling, threshold=0.1)
    # Learning under uncertainty: currently no tests
    # Causality: currently no tests
    import decnNetworks
    decnNetworks.test(decnNetworks.fire_dn)
    # Reinforement Learning: currently no tests
    # Multiagent systems: currently no tests
    # Relational Learning: currently no tests
    

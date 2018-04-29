# -*- coding: utf-8 -*-
"""
Solve ABM

@author: Marzieh, 2014
@commented: Harrison Paul Cooper, 2017
@updated: Harrison Paul Cooper, 2018
@last_updated: Harrison Paul Cooper, 23/04/2018
"""
from senescent_cells import sc
from proliferating_cells import pc
from quiescent_cells import qc


def update_messages(env):
    """


    General procedure:
        Update messages for each agent
        Create new list containing only living agents
        Update agent counter
    :param env:
    :return:
    """
    for agent in env.quiescent_cells:
        agent.process_messages()
    env.quiescent_cells = ([a for a in env.quiescent_cells if not a.messages.dead])
    qc.num_qc = sum([isinstance(agent, qc) for agent in env.quiescent_cells])
    
    for agent in env.senescent_cells:
        agent.process_messages()
    env.senescent_cells = ([a for a in env.senescent_cells if not a.messages.dead])
    sc.num_sc = sum([isinstance(agent, sc) for agent in env.senescent_cells])
        
    for agent in env.proliferating_cells:
        agent.process_messages()
    env.proliferating_cells = ([a for a in env.proliferating_cells if not a.messages.dead])
    pc.num_pc = sum([isinstance(agent, pc) for agent in env.proliferating_cells])
        

def agent_solve(env):
    """
    Goes through each agent applying their rules each iteration.

    :param env: Contains the current agents on the simulation
    :return: The updated states for each agent
    """
    new_senescent_cells = []  # List of new senescent cells created for this iteration
    new_proliferating_cells = []  # List of new proliferating cells created for this iteration
    new_quiescent_cells = []  # List of new quiescent cells created this iteration

    for agent in env.senescent_cells:
        if agent.stage == agent.max_stage:
            agent.kill_cell()
        if not agent.messages.dead:
            agent.growth()

    for agent in env.proliferating_cells:
        senescence = agent.senescence()
        if senescence is not None:
            new_senescent_cells.append(senescence)
            continue
        if agent.iscluster is True:
            quiescence = agent.quiescence()
            if quiescence is not None:
                new_quiescent_cells.append(quiescence)
                continue
        agent.migrate(env)
        agent.apoptosis()
        if not agent.messages.dead:
            new = agent.growth()
            if new is not None:
                new_proliferating_cells.append(new)

    for agent in env.quiescent_cells:
        senescence = agent.senescence()
        if senescence is not None:
            new_senescent_cells.append(senescence)
            continue
        if agent.iscluster is False:
            proliferating = agent.proliferating()
            if proliferating is not None:
                new_proliferating_cells.append(proliferating)
        agent.migrate(env)

    # Add new agents to list
    env.senescent_cells.extend(new_senescent_cells)
    env.proliferating_cells.extend(new_proliferating_cells)
    env.quiescent_cells.extend(new_quiescent_cells)

    update_messages(env)

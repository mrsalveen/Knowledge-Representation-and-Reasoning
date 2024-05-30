import action_language as al

def print_execution(state, program):
    involved_agents = set()
    print("=====================Executing actions======================")
    print(f"Initial state: {state}")
    for action, agent in program:
        state = action.execute(state, agent)
        involved_agents.update(action.involved_agents)
        print(f"After {agent} performs {action.name}: {state}")
    print("============================================================")
    return involved_agents

def main():
    # Initial state
    initial_fluents = {
        'wall_demolished': False,
        'canon_loaded': False
    }
    state = al.State(initial_fluents)

    # Define actions
    shoot_canon = al.Action(
        name="shoot_canon",
        preconditions={'canon_loaded': True},
        effects={'wall_demolished': True, 'canon_loaded': False},
        agents=['agent1', 'agent2']
    )

    load_canon = al.Action(
        name="load_canon",
        preconditions={'canon_loaded': False},
        effects={'canon_loaded': True},
        # Only agent2 can load the canon
        agents=['agent2']
    )

    # Define program as a list of (action, agent) pairs
    program1 = [
        (shoot_canon, 'agent1'), # This will have no effect since canon is not loaded
        (load_canon, 'agent1'),  # This will not have any effect since agent1 can't load
        (load_canon, 'agent2'),
        (shoot_canon, 'agent1'),
        (load_canon, 'agent2'),
        (shoot_canon, 'agent1'),
    ]

    # Only agent2 is involved in the program
    program2 = [
        (shoot_canon, 'agent1'), # This will have no effect since canon is not loaded
        (load_canon, 'agent1'),  # This will not have any effect since agent1 can't load
        (load_canon, 'agent2'),
        (shoot_canon, 'agent2'),
    ]

    involved_agents = print_execution(state, program2)
    print(f"Agents involved in the program: {involved_agents}")


if __name__ == "__main__":
    main()
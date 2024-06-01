import action_language as al

# STREAMLIT
# Adding agents as a separate tab.
# Add the way goals are added 
# Description of each step when executing program
def print_execution(state, program, goal):
    involved_agents = set()
    print("=====================Executing actions======================")
    print(f"Initial state: {state}")
    last_fluents = state.get_fluents().copy()
    for action, agent in program:
        agent_had_effect = False
        action.execute(state, agent)
        new_fluents = state.get_fluents().copy()
        if last_fluents != new_fluents:
            agent_had_effect = True 
            changed_fluents = {key: (last_fluents[key], new_fluents[key]) for key in last_fluents if last_fluents[key] != new_fluents[key]}
        if agent_had_effect:
            involved_agents.add(agent)
            print(f"After {agent} performs {action.name} state changed to: {state}")
            print("Changed fluents: ", changed_fluents)
        else:
            print(f"After {agent} performs {action.name} state does NOT change: {state}")
    print("============================================================")

    # Check if the goal is reached
    goal_reached = all(state.get_fluent_value(fluent) == value for fluent, value in goal.items())

    if goal_reached:
        print(f"Goal {goal} was reached.")
    else:
        print(f"Goal {goal} was not reached.")
    print(f"Agents involved in the program: {involved_agents}")

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

    # Define the goal
    goal1 = {'wall_demolished': True, 'canon_loaded': False}
    goal2 = {'canon_loaded': True}

    print_execution(state, program2, goal1)


if __name__ == "__main__":
    main()
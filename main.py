import action_language as al

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
        agent='agent1'
    )

    load_canon = al.Action(
        name="load_canon",
        preconditions={'canon_loaded': False},
        effects={'canon_loaded': True},
        agent='agent1'
    )

    # Execute actions sequentially
    actions = [shoot_canon, load_canon, shoot_canon]
    for action in actions:
        state = action.execute(state)
        print(f"After {action.name}: {state}")

if __name__ == "__main__":
    main()
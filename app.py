import streamlit as st
from action_language import Action, State  # Replace 'your_module' with the name of the module where Action and State are defined
import pandas as pd
# Initialize session state
if 'fluent_dict' not in st.session_state:
    st.session_state['fluent_dict'] = {}
if 'goal_dict' not in st.session_state:
    st.session_state['goal_dict'] = {}
if 'action_dict' not in st.session_state:
    st.session_state['action_dict'] = {}
if 'program_dict' not in st.session_state:
    st.session_state['program_dict'] = {}



# Tabs
fluents, agents, actions, programs = st.tabs(['Fluents', 'Agents', 'Actions', 'Programs'])

with fluents:
    #Fluent
    st.header('Fluent')
    fluent_name = st.text_input('Enter a name for the Fluent', key='fluent_name')
    fluent_value = st.checkbox('True (else False)', key='fluent_value')

    if st.button('Add Fluent'):
        st.session_state['fluent_dict'][fluent_name] = fluent_value
        st.write(f'Fluent {fluent_name} added')


    # ...
with actions:
    # Action
    st.header('Action')
    action_name = st.text_input('Enter a name for the Action', key='action_name')

    # Create a list of fluents for the preconditions and effects
    fluent_options = list(st.session_state['fluent_dict'].keys())
    value_options = [True, False]

    # Create columns for the precondition fluent and value dropdowns
    precondition_columns = st.columns(2)
    action_preconditions_fluent = precondition_columns[0].selectbox('Select precondition fluent for the Action', fluent_options, key='action_preconditions_fluent')
    action_preconditions_value = precondition_columns[1].selectbox('Select precondition value for the Action', value_options, key='action_preconditions_value')

    if st.button('Add Precondition'):
        # Create a unique key for the action's preconditions
        preconditions_key = f'{action_name}_preconditions'
        # Get the preconditions for the current action, or create a new dictionary if it doesn't exist
        preconditions = st.session_state.setdefault(preconditions_key, {})
        # Add the precondition to the action's preconditions
        preconditions[action_preconditions_fluent] = action_preconditions_value
        st.write(f'Precondition {action_preconditions_fluent}={action_preconditions_value} added')

    # Create columns for the effect fluent and value dropdowns
    effect_columns = st.columns(2)
    action_effects_fluent = effect_columns[0].selectbox('Select effect fluent for the Action', fluent_options, key='action_effects_fluent')
    action_effects_value = effect_columns[1].selectbox('Select effect value for the Action', value_options, key='action_effects_value')

    if st.button('Add Effect'):
        # Create a unique key for the action's effects
        effects_key = f'{action_name}_effects'
        # Get the effects for the current action, or create a new dictionary if it doesn't exist
        effects = st.session_state.setdefault(effects_key, {})
        # Add the effect to the action's effects
        effects[action_effects_fluent] = action_effects_value
        st.write(f'Effect {action_effects_fluent}={action_effects_value} added')

    action_agents = st.text_input('Enter agents for the Action (comma-separated)', key='action_agents', placeholder='Example: agent1,agent2')
    action_dict = st.session_state['action_dict']

    if st.button('Add Action'):
        # Get the preconditions and effects for the current action
        preconditions = st.session_state.get(f'{action_name}_preconditions', {})
        effects = st.session_state.get(f'{action_name}_effects', {})
        agents = action_agents.split(',')
        action_dict[action_name] = Action(action_name, preconditions, effects, agents)
        st.session_state['action_dict'] = action_dict
        st.write(f'Action {action_name} added')

        # ...
    # ...

    # Display the list of actions
    st.header('List of Actions')
    for action_name, action in st.session_state['action_dict'].items():
        st.markdown(f'**Action Name:** {action_name}')
        st.markdown(f'**Preconditions:** {", ".join([f"{k}={v}" for k, v in action.preconditions.items()])}')
        st.markdown(f'**Effects:** {", ".join([f"{k}={v}" for k, v in action.effects.items()])}')
        st.markdown(f'**Agents:** {", ".join(action.agents)}')
        st.markdown("---")
with programs:
    #Program
    st.header('Program')
    program_name = st.text_input('Enter a name for the Program', key='program_name')

    # Get the list of actions and agents
    action_options = list(st.session_state['action_dict'].keys())
    # Create a set of all agents
    agent_set = set()
    for action in st.session_state['action_dict'].values():
        agent_set.update(action.agents)  # Assuming 'agents' is an attribute of 'Action'

    # Convert the set to a list to use it as options for the selectbox
    agent_options = list(agent_set)

    # Create selectboxes for the action and agent
    selected_action = st.selectbox('Select an action for the step', action_options, key='selected_action')
    selected_agent = st.selectbox('Select an agent for the step', agent_options, key='selected_agent')

    program_dict = st.session_state.get('program_dict', {})

    if st.button('Add Step to Program'):
        if program_name not in program_dict:
            program_dict[program_name] = []
        program_dict[program_name].append((st.session_state['action_dict'][selected_action], selected_agent))  # Add the (action, agent) pair to the program
        st.session_state['program_dict'] = program_dict
        st.write(f'Step {selected_action}={selected_agent} added to Program {program_name}')

    if st.button('Show Program'):
        # Display the list of programs
        for program_name, steps in st.session_state['program_dict'].items():
            st.header(f'Program Name: {program_name}')
            for step in steps:
                action, agent = step
                st.subheader(f'Step: {action.name} by Agent: {agent}')
                # Create a DataFrame for the action information
                action_info = pd.DataFrame({
                    'Preconditions': [", ".join([f"{k}={v}" for k, v in action.preconditions.items()])],
                    'Effects': [", ".join([f"{k}={v}" for k, v in action.effects.items()])]
                })
                st.table(action_info)
            st.markdown("---")

    # Goal State
    st.header('Goal State')

    goal_name = st.text_input('Enter a name for the Goal', key='goal_name')
    goal_value = st.checkbox('True (else False)', key='gaol_value')

    if st.button('Add Goal'):
        st.session_state['goal_dict'] = {goal_name: goal_value}
        st.write(f'Goal {fluent_name} added')

    # Execute the program and display the involved agents
    st.header('Program Execution')
    selected_program = st.selectbox('Select a program to execute', list(st.session_state['program_dict'].keys()), key='selected_program')
    if st.button('Execute Program'):
        state = State(st.session_state['fluent_dict']) # Assuming 'initial_state' is stored in the session state
        program = st.session_state['program_dict'][selected_program]
        involved_agents = set()
        for action, agent in program:
            had_effect = action.execute(state, agent)  # Assuming 'execute' is a method of 'Action'
            if had_effect:
                involved_agents.add(agent)
        st.write(f'Agents involved in the program: {involved_agents}')
        # Check if the goal state is achieved
        goal_achieved = all(state.get_fluent_value(fluent) == value for fluent, value in st.session_state['goal_dict'].items())
        st.write(f'Goal state achieved: {goal_achieved}')

# Display the current state of all fluents in the sidebar
st.sidebar.header('Current State')
for fluent, value in st.session_state['fluent_dict'].items():
    st.sidebar.write(f'{fluent}: {value}')
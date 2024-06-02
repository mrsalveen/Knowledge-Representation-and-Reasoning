import streamlit as st
from action_language import Action, State  # Replace 'your_module' with the name of the module where Action and State are defined
import pandas as pd

# Initialize session state
if 'fluent_dict' not in st.session_state:
    st.session_state['fluent_dict'] = {}
if 'fluent_count' not in st.session_state:
    st.session_state['fluent_count'] = 1
if 'agent_list' not in st.session_state:
    st.session_state['agent_list'] = []
if 'agent_count' not in st.session_state:
    st.session_state['agent_count'] = 1
if 'goal_dict' not in st.session_state:
    st.session_state['goal_dict'] = {}
if 'action_dict' not in st.session_state:
    st.session_state['action_dict'] = {}
if 'action_count' not in st.session_state:
    st.session_state['action_count'] = 1
if 'precondition_count_0' not in st.session_state:
    st.session_state['precondition_count_0'] = 1
if 'effect_count_0' not in st.session_state:
    st.session_state['effect_count_0'] = 1
if 'program_dict' not in st.session_state:
    st.session_state['program_dict'] = {}

# Tabs
fluents, agents, actions, programs = st.tabs(['Fluents', 'Agents', 'Actions', 'Programs'])

############################################################################################################
############################################################################################################


# Function to add a new fluent text field
def add_fluent():
    st.session_state['fluent_count'] += 1
    st.experimental_rerun()

def remove_fluent():
    st.session_state['fluent_count'] -= 1
    st.experimental_rerun()

# Function to save all fluents
def save_fluents():
    for i in range(st.session_state['fluent_count']):
        fluent_name = st.session_state[f'fluent_name_{i}']
        fluent_value = st.session_state[f'fluent_value_{i}']
        if fluent_name:  # Only save if name is not empty
            st.session_state['fluent_dict'][fluent_name] = fluent_value
    st.success("Fluents saved successfully!")


with fluents:
    st.header('Fluents')
    
    # Render the text inputs for each fluent
    for i in range(st.session_state['fluent_count']):
        col1, col2 = st.columns([3, 2])
        with col1:
            st.text_input('Fluent Name', key=f'fluent_name_{i}')
        with col2:
            st.toggle("False/True", key=f'fluent_value_{i}')
    
    # Button to add/remove new fluent fields
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button('Add a New Fluent'):
            add_fluent()
    with col2:
        if st.button('Remove a Fluent'):
            remove_fluent()
    
    # Save button
    if st.button('Save Fluents', type='primary'):
        save_fluents()
        st.write(st.session_state['fluent_dict'])

############################################################################################################
############################################################################################################


# Function to add a new agent
def add_agent():
    st.session_state['agent_count'] += 1
    st.experimental_rerun()

# Function to remove an agent
def remove_agent():
    st.session_state['agent_count'] -= 1
    st.experimental_rerun()

# Function to save all agents
def save_agents():
    st.session_state['agent_list'] = []
    for i in range(st.session_state['agent_count']):
        agent_name = st.session_state[f'agent_name_{i}']
        if agent_name: # Only save if name is not empty
            if agent_name not in st.session_state['agent_list']:   
                st.session_state['agent_list'].append(agent_name)
            elif agent_name in st.session_state['agent_list']:
                st.warning(f"Agent '{agent_name}' is already in the list. Skipping")
    st.success("Fluents saved successfully!")


with agents:
    st.header('Agents')
    
    for i in range(st.session_state['agent_count']):
        st.text_input('Agent Name', key=f'agent_name_{i}')

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button('Add a New Agent'):
            add_agent()
            st.experimental_rerun()
    with col2:
        if st.button('Remove Agent'):
            remove_agent()
            st.experimental_rerun()

    # Save button
    if st.button('Save Agents', type='primary'):
        save_agents()
        st.write(st.session_state['agent_list'])

############################################################################################################
############################################################################################################


def add_action():
    st.session_state['action_count'] += 1
    st.experimental_rerun()

def add_action():
    st.session_state['action_count'] -= 1
    st.experimental_rerun()

def save_actions():
    action_dict = {}
    for i in range(st.session_state['action_count']):
        action_name = st.session_state.get(f'action_name_{i}', '')
        preconditions = save_preconditions(i)
        effects = save_effect(i)
        agents = st.session_state.get('action_agents', [])
        if action_name:
            action_dict[action_name] = {
                'preconditions': preconditions,
                'effects': effects,
                'agents': agents
            }
    st.session_state['action_dict'] = action_dict

def add_precondition(action_index):
    if f'precondition_count_{action_index}' not in st.session_state:
        st.session_state[f'precondition_count_{action_index}'] = 1
        st.experimental_rerun()
    else:
        st.session_state[f'precondition_count_{action_index}'] += 1
        st.experimental_rerun()

def remove_precondition(action_index):
    if f'precondition_count_{action_index}' in st.session_state and st.session_state[f'precondition_count_{action_index}'] > 1:
        st.session_state[f'precondition_count_{action_index}'] -= 1
        st.experimental_rerun()

def save_preconditions(action_index):
    preconditions = {}
    for i in range(st.session_state[f'precondition_count_{action_index}']):
        fluent_key = f'action_preconditions_fluent_{action_index}_{i}'
        value_key = f'action_preconditions_value_{action_index}_{i}'
        if fluent_key in st.session_state and value_key in st.session_state:
            precondition_fluent = st.session_state[fluent_key]
            precondition_value = st.session_state[value_key]
            preconditions[precondition_fluent] = precondition_value
    return preconditions

def add_effect(action_index):
    if f'effect_count_{action_index}' not in st.session_state:
        st.session_state[f'effect_count_{action_index}'] = 1
        st.experimental_rerun()
    else:
        st.session_state[f'effect_count_{action_index}'] += 1
        st.experimental_rerun()

def remove_effect(action_index):
    if f'effect_count_{action_index}' in st.session_state and st.session_state[f'effect_count_{action_index}'] > 1:
        st.session_state[f'effect_count_{action_index}'] -= 1
        st.experimental_rerun()

def save_effect(action_index):
    effects = {}
    for i in range(st.session_state[f'effect_count_{action_index}']):
        fluent_key = f'action_effects_fluent_{action_index}_{i}'
        value_key = f'action_effects_value_{action_index}_{i}'
        if fluent_key in st.session_state and value_key in st.session_state:
            effect_fluent = st.session_state[fluent_key]
            effect_value = st.session_state[value_key]
            effects[effect_fluent] = effect_value
    return effects


with actions:
    st.header('Actions')

    for i in range(st.session_state['action_count']):
        precondition_count = 1
        effect_count = 1

        col1, col2 = st.columns([3, 2])
        action_name = st.text_input('Enter a name for the Action', key=f'action_name_{i}')

        # FLUENTS
        fluent_options = list(st.session_state['fluent_dict'].keys())
        value_options = [True, False]

        # PRECONDITIONS
        for j in range(st.session_state[f'precondition_count_{i}']):
            precondition_columns = st.columns(2)
            action_preconditions_fluent = precondition_columns[0].selectbox('Select precondition fluent', fluent_options, key=f'action_preconditions_fluent_{i}_{j}')
            action_preconditions_value = precondition_columns[1].selectbox('Select precondition value', value_options, key=f'action_preconditions_value_{i}_{j}')

        if precondition_columns[0].button('Add Precondition'):
            add_precondition(i)

        if precondition_columns[1].button('Remove Precondition'):
            remove_precondition(i)

        if st.button('Save Precondition'):
            save_preconditions(i)

        # EFFECTS
        for j in range(st.session_state[f'effect_count_{i}']):
            effect_columns = st.columns(2)
            action_effects_fluent = effect_columns[0].selectbox('Select effect fluent for the Action', fluent_options, key=f'action_effects_fluent_{i}_{j}')
            action_effects_value = effect_columns[1].selectbox('Select effect value for the Action', value_options, key=f'action_effects_value_{i}_{j}')

        if effect_columns[0].button('Add Effect'):
            add_effect(i)

        if effect_columns[1].button('Remove Effect'):
            remove_effect(i)

        if st.button('Save Effect'):
            save_effect(i)

        # AGENTS
        agents_options = st.session_state['agent_list']
        action_agents = st.multiselect('Select agents for this Action', agents_options, key='action_agents')
        # action_agents = st.text_input('Enter agents for the Action (comma-separated)', key='action_agents', placeholder='Example: agent1,agent2')
        
        action_dict = st.session_state['action_dict']

        if st.button('Add Action'):
            add_action()

        if st.button('Save Actions', type='primary'):
            save_actions()

    # Display the list of actions
    st.header('List of Actions')
    for action_name, action in st.session_state['action_dict'].items():
        st.markdown(f'**Action Name:** {action_name}')
        st.markdown(f'**Preconditions:** {", ".join([f"{k}={v}" for k, v in action.preconditions.items()])}')
        st.markdown(f'**Effects:** {", ".join([f"{k}={v}" for k, v in action.effects.items()])}')
        st.markdown(f'**Agents:** {", ".join(action.agents)}')
        st.markdown("---")

############################################################################################################
############################################################################################################


with programs:
    st.header('Programs')
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
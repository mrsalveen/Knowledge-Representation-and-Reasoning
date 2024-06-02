import streamlit as st
from action_language import Action, State  # Replace 'your_module' with the name of the module where Action and State are defined
import pandas as pd

# Initialize session state
# if 'fluent_dict' not in st.session_state:
#     st.session_state['fluent_dict'] = {'wall_demolished': False, 'canon_loaded': False}
# if 'fluent_count' not in st.session_state:
#     st.session_state['fluent_count'] = 1
# if 'agent_list' not in st.session_state:
#     st.session_state['agent_list'] = ['Alice', 'Bob', 'Charlie']
# if 'agent_count' not in st.session_state:
#     st.session_state['agent_count'] = 1
# if 'goal_dict' not in st.session_state:
#     st.session_state['goal_dict'] = {'wall_demolished': False}
# if 'action_dict' not in st.session_state:
#     st.session_state['action_dict'] = {}
# if 'action_count' not in st.session_state:
#     st.session_state['action_count'] = 1
# if 'program_dict' not in st.session_state:
#     st.session_state['program_dict'] = {}
# if 'program_count' not in st.session_state:
#     st.session_state['program_count'] = 1
# if 'goal_fluent_count' not in st.session_state:
#     st.session_state['goal_fluent_count'] = 1

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
if 'program_dict' not in st.session_state:
    st.session_state['program_dict'] = {}
if 'program_count' not in st.session_state:
    st.session_state['program_count'] = 1
if 'goal_fluent_count' not in st.session_state:
    st.session_state['goal_fluent_count'] = 1
# Tabs
fluents, agents, actions, programs, execution = st.tabs(['Fluents', 'Agents', 'Actions', 'Programs', 'Execution'])

############################################################################################################
############################################################################################################


# Function to add a new fluent text field
def add_fluent():
    st.session_state['fluent_count'] += 1
    st.rerun()

def remove_fluent():
    if st.session_state['fluent_count'] > 1:
        st.session_state['fluent_count'] -= 1
        st.rerun()

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
    st.rerun()

# Function to remove an agent
def remove_agent():
    if st.session_state['agent_count'] > 1:
        st.session_state['agent_count'] -= 1
        st.rerun()

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
    st.success("Agents saved successfully!")


with agents:
    st.header('Agents')
    
    for i in range(st.session_state['agent_count']):
        st.text_input('Agent Name', key=f'agent_name_{i}')

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button('Add a New Agent'):
            add_agent()
            st.rerun()
    with col2:
        if st.button('Remove Agent'):
            remove_agent()
            st.rerun()

    # Save button
    if st.button('Save', type='primary', key='save_agents'):
        save_agents()
        st.write(st.session_state['agent_list'])

############################################################################################################
############################################################################################################


def add_action():
    st.session_state['action_count'] += 1
    st.rerun()

def remove_action():
    if st.session_state['action_count'] > 1:
        st.session_state['action_count'] -= 1
        st.rerun()

def save_actions():
    action_dict = {}
    for i in range(st.session_state['action_count']):
        action_name = st.session_state.get(f'action_name_{i}', '')
        preconditions = save_preconditions(i)
        effects = save_effect(i)
        agents = st.session_state.get(f'action_agents_{i}', [])
        if action_name:
            action_dict[action_name] = Action(action_name, preconditions, effects, agents)
    st.success("Actions saved successfully!")
    st.session_state['action_dict'] = action_dict

def add_precondition(action_index):
    st.session_state[f'precondition_count_{action_index}'] += 1
    st.rerun()

def remove_precondition(action_index):
    if f'precondition_count_{action_index}' in st.session_state and st.session_state[f'precondition_count_{action_index}'] > 0:
        st.session_state[f'precondition_count_{action_index}'] -= 1
        st.rerun()

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
        st.rerun()
    else:
        st.session_state[f'effect_count_{action_index}'] += 1
        st.rerun()

def remove_effect(action_index):
    if f'effect_count_{action_index}' in st.session_state and st.session_state[f'effect_count_{action_index}'] > 1:
        st.session_state[f'effect_count_{action_index}'] -= 1
        st.rerun()

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


with actions: # TODO: TOCHECK. Check if effects are being added if there are > 1. 
    # In my prev observations only 1 effect is saved.
    st.header('Actions')

    for i in range(st.session_state['action_count']):
        st.write(f'**Action {i+1}**')
        precondition_count = 1
        effect_count = 1

        col1, col2 = st.columns([3, 2])
        action_name = st.text_input('Enter a name for the Action', key=f'action_name_{i}')

        # FLUENTS
        fluent_options = list(st.session_state['fluent_dict'].keys())
        value_options = [True, False]

        # PRECONDITIONS
        if f'precondition_count_{i}' not in st.session_state:
            st.session_state[f'precondition_count_{i}'] = 0
        precondition_columns = st.columns(2)
        for j in range(st.session_state[f'precondition_count_{i}']):
            action_preconditions_fluent = precondition_columns[0].selectbox('Select precondition fluent', fluent_options, key=f'action_preconditions_fluent_{i}_{j}')
            action_preconditions_value = precondition_columns[1].selectbox('Select precondition value', value_options, key=f'action_preconditions_value_{i}_{j}')

        if precondition_columns[0].button('Add Precondition', key=f'action_preconditions_fluent_{i}'):
            add_precondition(i)

        if precondition_columns[1].button('Remove Precondition', key=f'action_preconditions_value_{i}'):
            remove_precondition(i)

        # EFFECTS
        if f'effect_count_{i}' not in st.session_state:
            st.session_state[f'effect_count_{i}'] = 1
        for j in range(st.session_state[f'effect_count_{i}']):
            effect_columns = st.columns(2)
            action_effects_fluent = effect_columns[0].selectbox('Select effect fluent for the Action', fluent_options, key=f'action_effects_fluent_{i}_{j}')
            action_effects_value = effect_columns[1].selectbox('Select effect value for the Action', value_options, key=f'action_effects_value_{i}_{j}')

        if effect_columns[0].button('Add Effect', key=f'action_effects_fluent_{i}'):
            add_effect(i)

        if effect_columns[1].button('Remove Effect', key=f'action_effects_value_{i}'):
            remove_effect(i)

        # AGENTS
        agents_options = st.session_state['agent_list']
        action_agents = st.multiselect('Select agents for this Action', agents_options, key=f'action_agents_{i}')
        # action_agents = st.text_input('Enter agents for the Action (comma-separated)', key='action_agents', placeholder='Example: agent1,agent2')
        action_dict = st.session_state['action_dict']

    action_columns = st.columns(2)
    if action_columns[0].button('Add Action', key=f'add_action_{i}'):
        add_action()

    if action_columns[1].button('Remove Action', key=f'remove_action_{i}'):
        remove_action()

    if st.button('Save', type='primary', key=f'save_action_{i}'):
        save_actions()
        st.write(st.session_state['action_dict'])


    # Display the list of actions
    # st.header('List of Actions')
    # for action_name, action in st.session_state['action_dict'].items():
        # st.markdown(f'**Action Name:** {action_name}')
        # st.markdown(f'**Preconditions:** {action["preconditions"]}')
        # st.markdown(f'**Effects:** {action["effects"]}')
        # st.markdown(f'**Agents:** {action["action_agents"]}')

############################################################################################################
############################################################################################################

def add_program_step(program_index):
    st.session_state[f'program_step_count_{program_index}'] += 1
    st.rerun()

def remove_program_step(program_index):
    if st.session_state[f'program_step_count_{program_index}'] > 1:
        st.session_state[f'program_step_count_{program_index}'] -= 1
        st.rerun()

def add_program():
    st.session_state['program_count'] += 1
    st.rerun()

def remove_program():
    if st.session_state['program_count'] > 1:
        st.session_state['program_count'] -= 1
        st.rerun()

def save_program():
    program_dict = {}
    for i in range(st.session_state['program_count']):
        program_name = st.session_state.get(f'program_name_{i}', '')
        if program_name:
            program_steps = []
            for j in range(st.session_state[f'program_step_count_{i}']):
                selected_action_name = st.session_state.get(f'selected_action_{i}_{j}', '')
                selected_agent_name = st.session_state.get(f'selected_agent_{i}_{j}', '')
                if selected_action_name and selected_agent_name:
                    program_steps.append((st.session_state['action_dict'][selected_action_name], selected_agent_name))
                    
            program_dict[program_name] = program_steps
    st.session_state['program_dict'] = program_dict
    st.success("Programs saved successfully!")

with programs:
    st.header('Programs')

    for i in range(st.session_state['program_count']):
        st.write(f'**Program {i+1}**')

        program_name = st.text_input('Enter a name for the Program', key=f'program_name_{i}')

        # Get the list of actions and agents
        action_names = list(st.session_state['action_dict'].keys())
        action_data = list(st.session_state['action_dict'].values())
        agent_options = st.session_state['agent_list']

        if f'program_step_count_{i}' not in st.session_state:
            st.session_state[f'program_step_count_{i}'] = 1
        for j in range(st.session_state[f'program_step_count_{i}']):
            program_step_columns = st.columns(2)
            selected_action = program_step_columns[0].selectbox('Select an action for this step', action_names, key=f'selected_action_{i}_{j}')
            selected_agent = program_step_columns[1].selectbox('Select an agent for this step', agent_options, key=f'selected_agent_{i}_{j}')

        # program_dict = st.session_state.get('program_dict', {})

        if program_step_columns[0].button('Add Step to the program', key=f'add_program_step_{i}_{j}'):
            add_program_step(i)
        if program_step_columns[1].button('Remove Step', key=f'remove_program_step_{i}_{j}'):
            remove_program_step(i)

    if program_step_columns[0].button('Add New Program', key=f'add_program_{i}'):
        add_program()

    if program_step_columns[1].button('Remove Program', key=f'remove_program_{i}'):
        remove_program()

    if st.button('Save', type='primary', key=f'save_program_{i}'):
        save_program()
        st.write(st.session_state['program_dict'])


############################################################################################################
############################################################################################################


def add_goal_fluent():
    st.session_state['goal_fluent_count'] += 1
    st.rerun()

def remove_goal_fluent():
    if st.session_state['goal_fluent_count'] > 1:
        st.session_state['goal_fluent_count'] -= 1
        st.rerun()

with execution:
    st.header('Execution')
    # single select from program 
    program_options = list(st.session_state['program_dict'].keys())
    # program_data = list(st.session_state['program_dict'].values())
    selected_program = st.selectbox('Select a program to execute', program_options, key='selected_program')

    goal_options = list(st.session_state['fluent_dict'].keys())
    goal_value_options = [True, False]

    goals_dict = {}
    goal_columns = st.columns(2)
    for i in range(st.session_state['goal_fluent_count']):
        selected_goal = goal_columns[0].selectbox('Select a goal fluent', goal_options, key=f'selected_goal_{i}')
        selected_goal_value = goal_columns[1].selectbox('Select goal value', goal_value_options, key=f'selected_goal_value_{i}')
        if selected_goal is not None and selected_goal_value is not None:
            goals_dict[selected_goal] = selected_goal_value

    if goal_columns[0].button('Add Goal Fluent', key='add_goal_fluent'):
        add_goal_fluent()
    if goal_columns[1].button('Remove Goal Fluent', key='remove_goal_fluent'):
        remove_goal_fluent()

    if st.button('Execute Program', type='primary', key='execute_program'):
        state = State(st.session_state['fluent_dict']) 
        involved_agents = set()
        program_data = st.session_state['program_dict'][selected_program]
        last_fluents = state.get_fluents().copy()
        st.write("=====================Executing actions======================")
        st.write(f"Initial state: {state}")
        for action, agent in program_data:
            agent_had_effect = False
            action.execute(state, agent)
            new_fluents = state.get_fluents().copy()
            if last_fluents != new_fluents:
                agent_had_effect = True 
                changed_fluents = {}
                # TODO: Fix this commented code below. tracking does not work
                # for key in last_fluents.keys():
                #     if last_fluents.get(key) != new_fluents.get(key):
                #         changed_fluents[key] = (last_fluents.get(key), new_fluents.get(key))
            if agent_had_effect:
                involved_agents.add(agent)
                st.write(f"After {agent} performs {action.name} state changed to: {state}")
                # st.write("Changed fluents: ", changed_fluents)
            else:
                st.write(f"After {agent} performs {action.name} state does NOT change: {state}")
        st.write(f"Agents involved in the program: {involved_agents}")
        # Check if the goal state is achieved
        goal_achieved = all(state.get_fluent_value(fluent) == value for fluent, value in goals_dict.items())
        if goal_achieved:
            st.write(f"Goal {goal_achieved} was reached.")
        else:
            st.write(f"Goal {goal_achieved} was not reached.")

# Display the current state of all fluents in the sidebar
st.sidebar.header('Current State')
for fluent, value in st.session_state['fluent_dict'].items():
    st.sidebar.write(f'{fluent}: {value}')
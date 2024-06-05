import streamlit as st
from action_language import Action, State

# Initialize session state
if 'fluent_dict' not in st.session_state:
    st.session_state['fluent_dict'] = {}
if 'agent_list' not in st.session_state:
    st.session_state['agent_list'] = []
if 'action_dict' not in st.session_state:
    st.session_state['action_dict'] = {}
if 'program_dict' not in st.session_state:
    st.session_state['program_dict'] = {}
if 'goals_dict' not in st.session_state:
    st.session_state['goals_dict'] = {}

# Parse input functions
def parse_initially_statements(text):
    initial_fluents = {}
    for line in text.split('\n'):
        if line.startswith('initially'):
            parts = line.split(' ')
            fluent = parts[1]
            initial_fluents[fluent] = True  # Assuming initially statements mean the fluent is True
    return initial_fluents

def parse_causes_statements(text):
    actions = {}
    for line in text.split('\n'):
        if 'causes' in line:
            parts = line.split(' ')
            action_name = parts[0]
            fluent = parts[2]
            condition = parts[-1]
            if action_name not in actions:
                actions[action_name] = Action(action_name, {condition: True}, {fluent: True}, [])
            else:
                actions[action_name].effects[fluent] = True
    return actions

def parse_after_statements(text):
    program = []
    final_state = {}
    for line in text.split('\n'):
        if 'after' in line:
            parts = line.split('after ')[1]
            steps = parts.strip().strip('()').split('), (')
            for step in steps:
                action, agent = step.split(', ')
                program.append({'action': action, 'agent': agent})
        else:
            parts = line.split(' ')
            fluent = parts[0]
            value = parts[1] == 'True'
            final_state[fluent] = value
    return program, final_state

# Parse user inputs
st.header('Input Section')

initially_statements = st.text_area('Enter Initially Statements')
causes_statements = st.text_area('Enter Causes Statements')
after_statements = st.text_area('Enter After Statements')

if st.button('Parse Inputs'):
    st.session_state['fluent_dict'] = parse_initially_statements(initially_statements)
    st.session_state['action_dict'] = parse_causes_statements(causes_statements)
    st.session_state['program_dict']['executed_program'], st.session_state['goals_dict'] = parse_after_statements(after_statements)
    st.success('Statements parsed successfully!')

# Display fluents
st.header('Fluents')
st.write(st.session_state['fluent_dict'])

# Display actions
st.header('Actions')
for action_name, action in st.session_state['action_dict'].items():
    st.write(f'**Action Name:** {action_name}')
    st.write(f'**Preconditions:** {action.preconditions}')
    st.write(f'**Effects:** {action.effects}')

# Display program
st.header('Program')
st.write(st.session_state['program_dict']['executed_program'])

# Execute the program
if st.button('Execute Program'):
    state = State(st.session_state['fluent_dict'])
    involved_agents = set()
    program_data = st.session_state['program_dict']['executed_program']
    last_fluents = state.get_fluents().copy()
    st.write("=====================Executing actions======================")
    st.write(f"Initial state: {state}")
    for action_name, agent in program_data:
        agent_had_effect = False
        action = st.session_state['action_dict'][action_name]
        action.execute(state, agent)
        new_fluents = state.get_fluents().copy()
        if last_fluents != new_fluents:
            agent_had_effect = True
            changed_fluents = {key: new_fluents[key] for key in last_fluents if last_fluents[key] != new_fluents[key]}
        if agent_had_effect:
            involved_agents.add(agent)
            st.write(f"After {agent} performs {action.name} state changed to: {state}")
        else:
            st.write(f"After {agent} performs {action.name} state does NOT change: {state}")
    st.write(f"Agents involved in the program: {involved_agents}")
    # Check if the goal state is achieved
    goal_achieved = all(state.get_fluent_value(fluent) == value for fluent, value in st.session_state['goals_dict'].items())
    if goal_achieved:
        st.write(f"Goal {goal_achieved} was reached.")
    else:
        st.write(f"Goal {goal_achieved} was not reached.")

# Display the current state of all fluents in the sidebar
st.sidebar.header('Current State')
for fluent, value in st.session_state['fluent_dict'].items():
    st.sidebar.write(f'{fluent}: {value}')

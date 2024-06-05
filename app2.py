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

def parse_initially_statements(text):
    initial_state = {}
    for line in text.split('\n'):
        if 'initially' in line:
            parts = line.split('initially ')[1].split(' ')
            
            fluent = parts[len(parts)-1]
            value = not ('NOT' in parts)
            initial_state[fluent] = value
    return initial_state

def parse_causes_statements(text):
    actions = {}
    for line in text.split('\n'):
        if 'causes' in line:
            parts = line.split('causes ')
            action = parts[0].strip()
            effects = parts[1].split(' if ')[0].split(', ')
            
            if 'if' in line:
                preconditions = parts[1].split(' if ')[1].split(', ')
            else:
                preconditions = []
            actions[action] = {'effects': {effect.replace('NOT ', ''): not ('NOT' in effect) for effect in effects},
                               'preconditions': {precondition.replace('NOT ', ''): not ('NOT' in precondition) for precondition in preconditions}}
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
    st.json(action)

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
    for steps in program_data:
        agent_had_effect = False
        action = Action(steps['action'], st.session_state['action_dict'][steps['action']]['preconditions'], st.session_state['action_dict'][steps['action']]['effects'], steps['agent'])
        action.execute(state, steps['agent'])
        new_fluents = state.get_fluents().copy()
        if last_fluents != new_fluents:
            agent_had_effect = True
            changed_fluents = {key: new_fluents[key] for key in last_fluents if last_fluents[key] != new_fluents[key]}
        if agent_had_effect:
            involved_agents.add(steps['agent'])
            st.write(f"After {steps['agent']} performs {action.name} state changed to: {state}")
        else:
            st.write(f"After {steps['agent']} performs {action.name} state does NOT change: {state}")
    st.write(f"Agents involved in the program: {involved_agents}")


# Display the current state of all fluents in the sidebar
st.sidebar.header('Current State')
for fluent, value in st.session_state['fluent_dict'].items():
    st.sidebar.write(f'{fluent}: {value}')

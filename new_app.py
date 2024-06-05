import streamlit as st
from action_language import Action, State
import pandas as pd
import re, json

if 'fluent_dict' not in st.session_state:
    st.session_state['fluent_dict'] = {}
if 'fluent_count' not in st.session_state:
    st.session_state['fluent_count'] = 1
if 'agent_list' not in st.session_state:
    st.session_state['agent_list'] = []
if 'agent_count' not in st.session_state:
    st.session_state['agent_count'] = 1
if 'num_input_boxes' not in st.session_state:
    st.session_state['num_input_boxes'] = 1
if 'statement_count' not in st.session_state:
    st.session_state['statement_count'] = 1
if 'program' not in st.session_state:
    st.session_state.program = []

st.header('Action Language Editor')

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

# Function to add a new agent
def add_agent():
    if 'After Statement' in [statement_type for statement_type, _ in st.session_state.program]:
        st.warning('Only one After Statement is allowed.')
    else:
        st.session_state['statement_count'] += 1
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

def parse_and_execute(statement_type, statement, mode = 'display'):
    # Execute the appropriate action based on the type of statement
    if statement_type == 'causes':
        # Use regular expressions to parse the statement
        if ' if ' in statement:
            match = re.match(r'(.*?) causes (.*?) if (.*)', statement)
            if match:
                action = match.group(1).strip()
                effect = match.group(2).strip()
                precondition = match.group(3).strip()
            else:
                st.error('Invalid Causes Statement. Please check the syntax.')
        else:
            match = re.match(r'(.*?) causes (.*)', statement)
            if match:

                action = match.group(1).strip()
                effect = match.group(2).strip()
                precondition = None
            else:
                st.error('Invalid Causes Statement. Please check the syntax.')

        if mode == 'display':

            st.json({
                "Action": action,
                "Effect": effect,
                "Precondition": precondition if precondition else 'None'
            })

    elif statement_type == 'initially':
        # Use regular expressions to parse the statement
        match = re.match(r'initially (.*)', statement)
        if match:
            fluent = match.group(1).strip()
            if mode == 'display':
                st.json({
                    "Initially Fluent": fluent
                })

        else:
            st.error('Invalid Initially Statement. Please check the syntax.')

    elif statement_type == 'after':
        # Use regular expressions to parse the statement
        match = re.match(r'(.*) after \(\((.*)\)\)', statement)
        if match:
            fluent = match.group(1).strip()
            program_steps = match.group(2).split('), (')
            program = []
            for step in program_steps:
                step_parts = step.replace('(', '').replace(')', '').split(', ')
                program.append({
                    'agent': step_parts[0],
                    'action': step_parts[1]
                })
            if mode == 'display':
                st.json({
                    "After Fluent": fluent,
                    "Program": program
                })
        
        else:
            st.error('Invalid After Statement. Please check the syntax.')
def add_statement():
    st.session_state['statement_count'] += 1
    st.rerun()

for i in range(st.session_state['statement_count']):
    col1, col2 = st.columns([1, 2])
    with col1:
        statement_type = st.selectbox('Select Statement Type', ['Causes Statement', 'Initially Statement', 'After Statement'], key=f'statement_type_{i}')
    with col2:
        statement = st.text_input('Enter a statement', key=f'statement_{i}')
        if st.button('Submit Statement', key=f'submit_statement_{i}'):
            # Check if the statement type is 'After Statement' and if one already exists in the program
            if statement_type == 'After Statement' and 'After Statement' in [existing_statement_type for j, (existing_statement_type, _) in enumerate(st.session_state.program) if j != i]:
                st.warning('Only one After Statement is allowed.')
            else:
                parse_and_execute(statement_type.lower().split(' ')[0], statement)
                # Check if the index i is in the range of st.session_state.program
                if i < len(st.session_state.program):
                    # Replace the statement at the current index in st.session_state.program
                    st.session_state.program[i] = (statement_type, statement)
                else:
                    # Append the new statement to the end of st.session_state.program
                    st.session_state.program.append((statement_type, statement))

if st.button('Add a New Statement'):
    add_statement()

if st.button('Show Program'):
    st.json(st.session_state.program)

if st.button('Execute Program'):
    pass
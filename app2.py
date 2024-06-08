import streamlit as st
from action_language import Action, State
import itertools
import re

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
if 'current_tab' not in st.session_state:
    st.session_state['current_tab'] = 'Q1'

def parse_initially_statements(text):
    initial_state = {}
    for line in text.split('\n'):
        if 'initially' in line:
            parts = line.split('initially ')[1].split(' ')
            
            fluent = parts[len(parts)-1]
            value = not ('not' in parts)

            # Check if the fluent has already been defined with a different value
            if fluent in initial_state and initial_state[fluent] != value:
                raise ValueError(f"Contradictory statements for fluent '{fluent}': cannot be both true and false")

            initial_state[fluent] = value
    return initial_state

def parse_causes_statements(text):
    actions = {}
    for line in text.split('\n'):
        if 'causes' in line:
            parts = line.split('causes ')
            action_parts = parts[0].strip().split(' by ')
            action = action_parts[0]
            agents = action_parts[1].split(', ') if len(action_parts) > 1 else []
            effects = parts[1].split(' if ')[0].split(', ')
            
            if 'if' in line:
                preconditions = parts[1].split(' if ')[1].split(', ')
            else:
                preconditions = []


            for agent in agents:
                action_key = f"{action} by {agent}"
                actions[action_key] = {'effects': {effect.replace('not ', ''): not ('not' in effect) for effect in effects},
                               'preconditions': {precondition.replace('not ', ''): not ('not' in precondition) for precondition in preconditions},
                               'agents': agent}

            
    return actions

def parse_after_statements(text):
    program = []
    final_state = {}
    for line in text.split('\n'):
        if 'after' in line:
            parts = line.split('holds after ')[1]
            pattern = re.compile(r'\(\s*([A-Z]+),\s*([A-Za-z]+)\s*\)')
            steps = pattern.findall(parts)
            if steps[0]:  # Check if steps are not empty
                for step in steps:
                    action, agent = step[0], step[1]
                    program.append({'action': action, 'agent': agent})
            else:
                program = []
         
            parts = line.split(' ')
            
            if 'not' in parts:
                fluent = parts[1]
                value = False
            else:
                fluent = parts[0]
                value = True
            final_state[fluent] = value
    return program, final_state

def parse_q2_statements(text):
    program = []
    for line in text.split('\n'):
        if 'involved in' in line:
            parts = line.split('holds after ')[1]
            pattern = re.compile(r'\(\s*([A-Z]+),\s*([A-Za-z]+)\s*\)')
            steps = pattern.findall(parts)
            for step in steps:
                action, agent = step[0], step[1]
                program.append({'action': action, 'agent': agent})
         
            main_agent = line.split(' involved ')[0]
        else:
            st.error('Invalid Q2 statement')
    return program, main_agent

def compare_final_state_with_goal(final_state, goal):
    final_state = final_state.get_fluents()
    for key, value in goal.items():
        if key not in final_state or final_state[key] != value:
            return 'No'
    return 'Yes'

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
    st.header('After statement')
    st.write(st.session_state['program_dict']['executed_program'])
    st.write("Goal state:") 
    st.json(st.session_state['goals_dict'])


Q1, Q2 = st.tabs(['Q1', 'Q2'])

with Q1:
    st.write("**Run program to get answer for Q1: Does condition hold after executing program?**")

    q1_statements = st.text_area('Enter Q1 program')

        # Execute the program
    if st.button('Execute Program Q1'):

        st.session_state['current_tab'] = 'Q1'

        

        st.session_state['program_dict']['q1_program'], goal_state = parse_after_statements(q1_statements)

        all_fluents = set(st.session_state['fluent_dict'].keys())
        for action in list(st.session_state['action_dict'].keys()):
            all_fluents = all_fluents.union(set(st.session_state['action_dict'][action]['effects'].keys()))
            all_fluents = all_fluents.union(set(st.session_state['action_dict'][action]['preconditions'].keys()))
        values = [[True, False] for _ in all_fluents]
        combinations = set(itertools.product(*values))
        combinations_as_dicts = [dict(zip(all_fluents, combination)) for combination in combinations]
        print(combinations_as_dicts)
        possible_combs = []
        final_combs = []
        st.write("===========================================================")
        st.write(f"Possible initiall combinations for after statement program : \
                 {st.session_state['goals_dict']} after {st.session_state['program_dict']['executed_program']}:")
        
        for comb in combinations_as_dicts:
            state = State(comb)
            program_data = st.session_state['program_dict']['executed_program']
            last_fluents = state.copy()
            for steps in program_data:
                action_key = f"{steps['action']} by {steps['agent']}"
                if action_key not in st.session_state['action_dict']:
                    raise ValueError(f"Action '{action_key}' does not exist")
                action = Action(action_key, st.session_state['action_dict'][action_key]['preconditions'], st.session_state['action_dict'][action_key]['effects'], steps['agent'])
                action.execute(state, steps['agent'])
                new_fluents = state.copy()
            if compare_final_state_with_goal(new_fluents, st.session_state['goals_dict']) == 'Yes':
                st.write(f"Possible comb: {last_fluents} ")
                possible_combs.append(last_fluents)

        st.write("===========================================================")
        st.write(f"Possible result combinations for after statement program : \
                        {goal_state} after {st.session_state['program_dict']['q1_program']}:")
        for comb in possible_combs:
            state = State(comb.get_fluents())
            program_data = st.session_state['program_dict']['q1_program']
            last_fluents = state.copy()
            for steps in program_data:
                action_key = f"{steps['action']} by {steps['agent']}"
                if action_key not in st.session_state['action_dict']:
                    raise ValueError(f"Action '{action_key}' does not exist")
                action = Action(action_key, st.session_state['action_dict'][action_key]['preconditions'], st.session_state['action_dict'][action_key]['effects'], steps['agent'])
                action.execute(state, steps['agent'])
                new_fluents = state.copy()
            if compare_final_state_with_goal(new_fluents, goal_state) == 'Yes':
                st.write(f"Final comb: {new_fluents} ")
                final_combs.append(new_fluents)
        if len(final_combs) == len(possible_combs):
            st.write("=====================Query answer:=====================")
            st.write(f"**YES**")
        elif len(final_combs) == 0:
            st.write("=====================Query answer:=====================")
            st.write(f"**NO**")
        else:
            st.write("=====================Query answer:=====================")
            st.write(f"**Condition holds after executing the program for some possible combinations**")

with Q2:
    st.write("**Run program to get answer for Q2: Was an agent involved in the program?**")

    q2_statements = st.text_area('Enter Q2 program')

    # Execute the program
    if st.button('Execute Program Q2'):
        st.session_state['current_tab'] = 'Q2'

        

        st.session_state['program_dict']['q2_program'], main_agent = parse_q2_statements(q2_statements)


        
        state = State(st.session_state['fluent_dict'])
        involved_agents = set()
        program_data = st.session_state['program_dict']['q2_program']
        last_fluents = state.get_fluents().copy()
        st.write("=====================Executing actions======================")
        st.write(f"Initial state: {state}")
        for steps in program_data:
            action_key = f"{steps['action']} by {steps['agent']}"

            if action_key not in list(st.session_state['action_dict'].keys()):
                raise ValueError(f"Action '{action_key}' does not exist")
            action = Action(action_key, st.session_state['action_dict'][action_key]['preconditions'], st.session_state['action_dict'][action_key]['effects'], steps['agent'])
            action.execute(state, steps['agent'])
            new_fluents = state.get_fluents().copy()
            agent_had_effect = False
            if last_fluents != new_fluents:
                agent_had_effect = True
                changed_fluents = {key: new_fluents[key] for key in last_fluents if last_fluents[key] != new_fluents[key]}
            if agent_had_effect:
                involved_agents.add(steps['agent'])
                st.write(f"After {steps['agent']} performs {action.name} state changed to: {state}")
            else:
                st.write(f"After {steps['agent']} performs {action.name} state does NOT change: {state}")
        st.write("=====================Query answer:=====================")

        if str(main_agent) in list(involved_agents):
            st.write(f"**YES**")
        else:
            st.write(f"**NO**")
        #st.write("=====================End of actions======================")



# Display the current state of all fluents in the sidebar
st.sidebar.header('Current State')
for fluent, value in st.session_state['fluent_dict'].items():
    st.sidebar.write(f'{fluent}: {value}')

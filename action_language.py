class Fluent:
    def __init__(self, name, value=True):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"{self.name}: {self.value}"


class State:
    def __init__(self, fluents=None):
        self.fluents = fluents if fluents is not None else {}

    def get_fluent_value(self, name):
        return self.fluents.get(name, None)

    def update_fluent(self, name, value):
        self.fluents[name] = value

    def __repr__(self):
        return str(self.fluents)


class Action:
    def __init__(self, name, preconditions, effects, agents):
        self.name = name
        # Preconditions and effects are dictionaries of the form {fluent: value}
        self.preconditions = preconditions
        self.effects = effects
        # Agents that can execute this action
        self.agents = agents
        # Involved Agents in the execution of this action
        self.involved_agents = set()

    def is_executable(self, state, agent):
        if agent not in self.agents:
            return False
        for fluent, value in self.preconditions.items():
            if state.get_fluent_value(fluent) != value:
                return False
        self.involved_agents.add(agent)
        return True

    def execute(self, state, agent):
        if self.is_executable(state, agent):
            for fluent, value in self.effects.items():
                state.update_fluent(fluent, value)
        return state

    def __repr__(self):
        return f"Action({self.name}, Pre: {self.preconditions}, Eff: {self.effects}, Agents: {self.agents})"
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
    def __init__(self, name, preconditions, effects, agent):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects
        self.agent = agent

    def is_executable(self, state):
        for fluent, value in self.preconditions.items():
            if state.get_fluent_value(fluent) != value:
                return False
        return True

    def execute(self, state):
        if self.is_executable(state):
            for fluent, value in self.effects.items():
                state.update_fluent(fluent, value)
        return state

    def __repr__(self):
        return f"Action({self.name}, Pre: {self.preconditions}, Eff: {self.effects}, Agent: {self.agent})"
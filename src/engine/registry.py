WORKFLOWS: dict[str, "WorkFlowDef"] = {}


class Marker:
    """ """

    def __repr__(self):
        return


class Sleep(Marker):
    def __init__(self, seconds: int):
        self.seconds = seconds


def sleep(seconds: int) -> Sleep:
    return Sleep(seconds)


class WorkFlowDef:
    def __init__(self, name: str, steps: list, retry=None):
        self.name = name
        self.steps = steps
        self.retry = retry

    def step_at(self, i):
        return self.steps[i]

    def is_last(self, i):
        return i == len(self.steps) - 1


def workflow(name: str, retry=None):
    def register(cls):
        WORKFLOWS[name] = WorkFlowDef(name=name, steps=cls.steps, retry=retry)
        return cls

    return register


def get_workflow(name: str) -> WorkFlowDef:
    return WORKFLOWS[name]


def _validate(steps: list):
    assert steps, "workflow has no steps"
    for step in steps:
        assert callable(step) or isinstance(step, Marker), f"Not a valid step: {step!r}"

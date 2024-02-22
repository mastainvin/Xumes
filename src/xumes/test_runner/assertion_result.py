

class AssertionResult:

    def __init__(self, passed: bool, fail_message: str, actual, expected):
        self.passed = passed
        self.fail_message = fail_message
        self.actual = actual
        self.expected = expected


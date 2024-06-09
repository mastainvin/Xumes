
class Driver:
    """
    A class that translates a function call into a JSON object containing the function name and parameters,
    and stores these calls in a dictionary under the key 'methods'.

    Attributes:
        _calls (list): A list to store the details of function calls.

    Methods:
        __getattr__(name: str) -> Callable:
            Returns a callable that captures the function name and parameters.
        __call__() -> list:
            Returns a list of stored function calls and clears the calls list.
    """

    def __init__(self):
        self._calls = []

    def __call__(self):
        """
        Returns a list containing the stored function calls and clears the calls list.

        Returns:
            list: A list containing the stored function calls.
        """
        call_details_list = self._calls
        self._calls = []
        return call_details_list

    def __getattr__(self, name: str):
        """
        Returns a callable that captures the function name and parameters.

        Args:
            name (str): The name of the function being called.

        Returns:
            Callable: A function that takes parameters and stores the call details.
        """

        def wrapper(*args, **kwargs):
            call_details = {
                "function_name": name,
                "parameters": {
                    "args": list(args),
                    "kwargs": kwargs
                }
            }
            self._calls.append(call_details)

        return wrapper

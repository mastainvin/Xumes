import unittest

from xumes.test_runner.driver import Driver


class DriverTest(unittest.TestCase):

    def test_driver_empty(self):
        driver = Driver()
        self.assertEqual(driver(), [])

    def test_driver_one_func(self):
        driver = Driver()
        driver.foo(10, 20, param1="test", param2=[1, 2, 3])
        self.assertEqual(driver(), [{
            "function_name": "foo",
            "parameters": {
                "args": [
                    10,
                    20
                ],
                "kwargs": {
                    "param1": "test",
                    "param2": [
                        1,
                        2,
                        3
                    ]
                }
            }
        }])

        self.assertEqual(driver(), [])

    def test_driver_multiple_funcs(self):
        driver = Driver()
        driver.foo(10, 20, param1="test", param2=[1, 2, 3])
        driver.bar(30, 40, param3="test2", param4=[4, 5, 6])

        self.assertEqual(driver(), [{
            "function_name": "foo",
            "parameters": {
                "args": [
                    10,
                    20
                ],
                "kwargs": {
                    "param1": "test",
                    "param2": [
                        1,
                        2,
                        3
                    ]
                }
            }
        }, {
            "function_name": "bar",
            "parameters": {
                "args": [
                    30,
                    40
                ],
                "kwargs": {
                    "param3": "test2",
                    "param4": [
                        4,
                        5,
                        6
                    ]
                }
            }
        }])

        self.assertEqual(driver(), [])

    def test_driver_multiple_calls(self):
        driver = Driver()
        driver.foo(10, 20, param1="test", param2=[1, 2, 3])
        driver.bar(30, 40, param3="test2", param4=[4, 5, 6])

        self.assertEqual(driver(), [{
            "function_name": "foo",
            "parameters": {
                "args": [
                    10,
                    20
                ],
                "kwargs": {
                    "param1": "test",
                    "param2": [
                        1,
                        2,
                        3
                    ]
                }
            }
        }, {
            "function_name": "bar",
            "parameters": {
                "args": [
                    30,
                    40
                ],
                "kwargs": {
                    "param3": "test2",
                    "param4": [
                        4,
                        5,
                        6
                    ]
                }
            }
        }])

        driver.foo(50, 60, param1="test3", param2=[7, 8, 9])
        driver.bar(70, 80, param3="test4", param4=[10, 11, 12])

        self.assertEqual(driver(), [{
            "function_name": "foo",
            "parameters": {
                "args": [
                    50,
                    60
                ],
                "kwargs": {
                    "param1": "test3",
                    "param2": [
                        7,
                        8,
                        9
                    ]
                }
            }
        }, {
            "function_name": "bar",
            "parameters": {
                "args": [
                    70,
                    80
                ],
                "kwargs": {
                    "param3": "test4",
                    "param4": [
                        10,
                        11,
                        12
                    ]
                }
            }
        }])

        self.assertEqual(driver(), [])

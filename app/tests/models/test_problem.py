from models import Problem, ProblemTest


def test_problem_create_no_tests():
    problem = Problem(name="test", description="testdescription", tip="tiptest")
    assert problem.name == "test"
    assert problem.description == "testdescription"
    assert problem.tip == "tiptest"
    assert len(problem.tests) == 0

def test_problemtest_create():
    test = ProblemTest(name="testname", tip="testtip", input="2", output="3")
    assert test.name == "testname"
    assert test.tip == "testtip"
    assert test.input == "2"
    assert test.output == "3"


def test_problem_create_with_tests():
    test1 = ProblemTest(name="testname", tip="testtip", input="2", output="3")
    test2 = ProblemTest(name="testname2", tip="testtip", input="2", output="3")
    problem = Problem(name="test", description="testdescription", tip="tiptest", tests=[test1, test2])
    assert len(problem.tests) == 2
    assert problem.tests[0].name == "testname"
    assert problem.tests[1].name == "testname2"


def test_problem_add_tests():
    problem = Problem(name="test", description="testdescription", tip="tiptest")
    problem.add_tests([{
				"name": "testname",
				"tip": "testtip",
				"input": "1",
				"output": "2"
			},
            {
                "name": "testname2",
				"input": "2",
				"output": "3"
			}
            ])
    assert problem.tests[0].name == "testname"
    assert problem.tests[1].name == "testname2"
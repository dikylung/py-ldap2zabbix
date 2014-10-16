import unittest
from scripttest import TestFileEnvironment

SCRIPT='../ldap2zabbix.py'

class CLITest(unittest.TestCase):

    def setUp(self):
        self.env = TestFileEnvironment('./.scratch')

    def tearDown(self):
        pass

    def test_can_run_script_without_arguments(self):
        result = self.env.run('%s' % (SCRIPT,), expect_error=True)
        assert result.returncode == 2

    def test_can_run_script_with_help(self):
        result = self.env.run('%s -h' % (SCRIPT,))
        assert result.returncode == 0

    def test_run_script_with_invalid_arg(self):
        result = self.env.run('%s --frob' % (SCRIPT,), expect_error=True)
        assert result.returncode == 2

if __name__ == '__main__':
    unittest.main()

import unittest
import ldap2zabbix
from unittest.mock import MagicMock, patch

class LDAPTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_search_method_called(self):
        lsearcher = ldap2zabbix.LDAPSearch('host', 389, 'dc=example,dc=com', 'user', 'pw')
        lsearcher.search = MagicMock(return_value='foo')
        assert lsearcher.list_group('acme') == 'foo'
        lsearcher.search.assert_called_with('(memberOf=cn=%s,cn=groups,cn=accounts,%s)' % ('acme', 'dc=example,dc=com'))

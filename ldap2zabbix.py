#!/usr/bin/env python3

import argparse
import yaml
from ldap3 import Server, Connection
from pyzabbix import ZabbixAPI

class LDAPSearch(object):
    def __init__(self, host, port, domain, user, password):
        self.host     = host
        self.port     = port
        self.domain   = domain
        self.user     = '%s,%s' % (user, domain)
        self.password = password

        self.search_base = 'cn=users,cn=accounts,%s' % (domain,)

    def list_group(self, groupname):
        return self.search('(memberOf=cn=%s,cn=groups,cn=accounts,%s)' % (groupname, self.domain))

    def search(self, search_filter):
        with Connection(Server(self.host, self.port),
                        user=self.user, password=self.password) as c:
            c.search(self.search_base, search_filter)
            return c.response

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ldapcfg", help="the file storing LDAP connection info")

    args = parser.parse_args()
    ldapcfg = yaml.load(open(args.ldapcfg, 'r'))
    lsearcher = LDAPSearch(ldapcfg['host'],
                           ldapcfg.get('port', 389),
                           ldapcfg['domain'],
                           ldapcfg['user'],
                           ldapcfg['password'])
    print(lsearcher.list_group(ldapcfg['group']))

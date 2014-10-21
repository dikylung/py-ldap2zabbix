#!/usr/bin/env python3

import argparse
import yaml
from ldap3 import Server, Connection
from pyzabbix import ZabbixAPI, ZabbixAPIException
from requests.exceptions import MissingSchema

LDAP_FILTER='(&(memberOf=cn=%s,cn=groups,cn=accounts,%s)(!(nsaccountlock=true)))'

class LDAPSearch(object):
    def __init__(self, host, port, domain, user, password):
        self.host     = host
        self.port     = port
        self.domain   = domain
        self.user     = '%s,%s' % (user, domain)
        self.password = password

        self.search_base = 'cn=users,cn=accounts,%s' % (domain,)

    @staticmethod
    def get_uid(dn):
        """
        :type dn: string
        :return: string
        """
        start_index = dn.find("uid=") + 4
        end_index = dn.find(",cn=")
        return dn[start_index:end_index]

    def list_group(self, groupname):
        return set(self.get_uid(res['dn']) for res in self.search(LDAP_FILTER % (groupname, self.domain)))

    def search(self, search_filter):
        with Connection(Server(self.host, self.port),
                        user=self.user, password=self.password) as c:
            c.search(self.search_base, search_filter)
            return c.response

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ldapcfg", help="the file storing LDAP connection info")
    parser.add_argument("zabbixcfg", help="the file storing Zabbix connection info")

    args = parser.parse_args()
    ldapcfg = yaml.load(open(args.ldapcfg, 'r'))
    lsearcher = LDAPSearch(ldapcfg['host'],
                           ldapcfg.get('port', 389),
                           ldapcfg['domain'],
                           ldapcfg['user'],
                           ldapcfg['password'])
    zabbixcfg = yaml.load(open(args.zabbixcfg, 'r'))
    try:
        zh = ZabbixAPI(zabbixcfg['host'])
        zh.login(zabbixcfg['user'], zabbixcfg['password'])
    except MissingSchema as ms:
        print("ERROR: Invalid Zabbix host URL")
        exit(1)
    except ZabbixAPIException as ze:
        print("ERROR: Invalid Zabbix username or password")
        exit(1)
    ldap_users = lsearcher.list_group(ldapcfg['group'])
    zabbix_users = set(u['alias'] for u in zh.user.get(output=["alias"]))
    print("LDAP users:   %s" % (ldap_users,))
    print("Zabbix users: %s" % (zabbix_users,))
    print ("To be added: %s" % ldap_users.difference(zabbix_users))



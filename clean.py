#!/usr/share/python/trove/bin/python

from cdbutils import vm


vm.clean()
vm.clear_databases()
vm.clear_vm()
vm.wipe_queues()
vm.local('mysql cdbproxy -e "DELETE FROM vips;"')
vm.populate_cdbproxy_db()

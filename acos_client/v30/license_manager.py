# Copyright (C) 2016, A10 Networks Inc. All rights reserved.

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import base

INTERVAL_MONTHLY = 1
INTERVAL_DAILY = 2
INTERVAL_HOURLY = 3

DEFAULT_LICENSE_PORT = 443


class LicenseManager(base.BaseV30):

    url_base = "/license-manager"

    def create(self, host_list=[], serial=None, instance_name=None,  use_mgmt_port=False,
               interval=None, bandwidth_base=None, bandwidth_unrestricted=None):
        """Form a complex number.

        Keyword arguments:
        instance_name -- license manager instance name
        host_list -- list(dict) a list of dictionaries of the format:
            {'ip': '127.0.0.1', 'port': 443}
        serial - (str) appliance serial number
        use_mgmt_port - (bool) use management for license interactions
        interval - (int) 1=Monthly, 2=Daily, 3=Hourly
        bandwidth_base - (int) Configure feature bandwidth base (Mb)
            Valid range - 10-102400
        bandwidth_unrestricted - (bool) Set the bandwidth to maximum
        """
        payload = self._build_payload(host_list, serial, instance_name, use_mgmt_port,
                                      interval, bandwidth_base, bandwidth_unrestricted)
        return self._post(self.url_base, payload)

    def update(self, host_list=[], serial=None, instance_name=None, use_mgmt_port=False,
               interval=None, bandwidth_base=None, bandwidth_unrestricted=None):
        """Form a complex number.

        Keyword arguments:
        instance_name -- license manager instance name
        host_list -- list(dict) a list of dictionaries of the format:
            {'ip': '127.0.0.1', 'port': 443}
        serial - (str) appliance serial number
        use_mgmt_port - (bool) use management for license interactions
        interval - (int) 1=Monthly, 2=Daily, 3=Hourly
        bandwidth_base - (int) Configure feature bandwidth base (Mb)
            Valid range - 10-102400
        bandwidth_unrestricted - (bool) Set the bandwidth to maximum
        """

        return self.create(host_list, serial, instance_name, use_mgmt_port,
                           interval, bandwidth_base, bandwidth_unrestricted)

    def get(self):
        return self._get(self.url_base)

    def connect(self, connect=False):
        url = self.url_base + "/connect"
        payload = {
            "connect": {
                "connect": 1 if connect else 0,
            }
        }
        return self._post(url, payload)

    def _build_payload(self, host_list=[], serial=None, instance_name=None, use_mgmt_port=False,
                       interval=None, bandwidth_base=None, bandwidth_unrestricted=None):
        rv = {"license-manager": {}}
        if host_list:
            for x in host_list:
                hosts = []
                hosts.append(self._build_host_entry(x["ip"], x.get("port")))

            rv["license-manager"]["host-list"] = hosts

        self._set_if_set(instance_name, rv["license-manager"], "instance-name")
        self._set_if_set(serial, rv["license-manager"], "sn")
        self._set_if_set(use_mgmt_port, rv["license-manager"], "use-mgmt-port")
        self._set_if_set(interval, rv["license-manager"], "interval")
        self._set_if_set(bandwidth_base, rv["license-manager"], "bandwidth-base")
        self._set_if_set(bandwidth_unrestricted, rv["license-manager"], "bandwidth-unrestricted")

        return rv

    def _build_host_entry(self, ip, port=DEFAULT_LICENSE_PORT):
        return {"host-ipv4": ip, "port": port or DEFAULT_LICENSE_PORT}

    def _set_if_set(self, src, dest, dest_key):
        if src is not None:
            dest[dest_key] = src

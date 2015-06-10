from sh import ErrorReturnCode
from functools import partial

from test_base import TestBase
from docker_host import DockerHost


class TestIpv6(TestBase):
    def test_ipv6(self):
        """
        Test mainline functionality with IPv6 addresses.
        """
        host = DockerHost('host')

        ip1, ip2 = "fd80:24e2:f998:72d6::1:1", "fd80:24e2:f998:72d6::1:2"
        # We use this image here because busybox doesn't have ping6.
        node1 = host.create_workload("node1", ip=ip1, image="phusion/baseimage:0.9.16")
        node2 = host.create_workload("node2", ip=ip2, image="phusion/baseimage:0.9.16")

        # Configure the nodes with the same profiles.
        host.calicoctl("profile add TEST_GROUP")
        host.calicoctl("profile TEST_GROUP member add %s" % node1)
        host.calicoctl("profile TEST_GROUP member add %s" % node2)

        node1.assert_can_ping(ip2, retries=3)

        # Check connectivity.
        self.assert_connectivity([node1, node2])
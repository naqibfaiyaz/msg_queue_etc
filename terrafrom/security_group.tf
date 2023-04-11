resource "openstack_networking_secgroup_v2" "allow_all" {
    name = "allow_all"
  
}

resource "openstack_networking_secgroup_rule_v2" "tcp_inbound" {
    direction = "ingress"
    ethertype = "IPv4"
    protocol = "tcp"
    security_group_id = openstack_networking_secgroup_v2.allow_all.id
    remote_ip_prefix  = "0.0.0.0/0"
}


resource "openstack_networking_secgroup_rule_v2" "tcp_outbound" {
    direction = "egress"
    ethertype = "IPv4"
    protocol = "tcp"
    security_group_id = openstack_networking_secgroup_v2.allow_all.id
    remote_ip_prefix  = "0.0.0.0/0"
}

resource "openstack_networking_secgroup_rule_v2" "ssh_inbound" {
    direction = "ingress"
    ethertype = "IPv4"
    protocol = "tcp"
    port_range_min = 22
    port_range_max = 22
    security_group_id = openstack_networking_secgroup_v2.allow_all.id
    remote_ip_prefix  = "0.0.0.0/0"
}


resource "openstack_networking_secgroup_rule_v2" "ssh_outbound" {
    direction = "egress"
    ethertype = "IPv4"
    protocol = "tcp"
    port_range_min = 22
    port_range_max = 22
    security_group_id = openstack_networking_secgroup_v2.allow_all.id
    remote_ip_prefix  = "0.0.0.0/0"
}

resource "openstack_networking_secgroup_rule_v2" "etcd_inbound" {
    direction = "ingress"
    ethertype = "IPv4"
    protocol = "tcp"
    port_range_min = 2379
    port_range_max = 2380
    security_group_id = openstack_networking_secgroup_v2.allow_all.id
    remote_ip_prefix  = "0.0.0.0/0"
}


resource "openstack_networking_secgroup_rule_v2" "etcd_outbound" {
    direction = "egress"
    ethertype = "IPv4"
    protocol = "tcp"
    port_range_min = 2379
    port_range_max = 2380
    security_group_id = openstack_networking_secgroup_v2.allow_all.id
    remote_ip_prefix  = "0.0.0.0/0"
}


resource "openstack_networking_secgroup_rule_v2" "icmp_inbound" {
    direction = "ingress"
    ethertype = "IPv4"
    protocol = "icmp"
    security_group_id = openstack_networking_secgroup_v2.allow_all.id
    remote_ip_prefix  = "0.0.0.0/0"
}


resource "openstack_networking_secgroup_rule_v2" "icmp_outbound" {
    direction = "egress"
    ethertype = "IPv4"
    protocol = "icmp"
    security_group_id = openstack_networking_secgroup_v2.allow_all.id
    remote_ip_prefix  = "0.0.0.0/0"
}

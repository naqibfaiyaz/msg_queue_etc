resource "openstack_networking_network_v2" "cloud" {
  name = "cloud"
}

resource "openstack_networking_subnet_v2" "cloud" {
  name       = "cloud"
  network_id = openstack_networking_network_v2.cloud.id
  cidr       = var.cloud_network["cidr"]
}


resource "openstack_networking_router_interface_v2" "router_interface_1" {
  router_id = openstack_networking_router_v2.router_1.id
  subnet_id = openstack_networking_subnet_v2.cloud.id
}

resource "openstack_networking_router_v2" "router_1" {
  name                = "my_router"
  admin_state_up      = true
  external_network_id = "<ID>"
}

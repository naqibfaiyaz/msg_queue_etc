resource "openstack_compute_instance_v2" "cloud" {
  for_each        = var.cloud_instances
  name            = each.key
  image_name      = var.compute_image
  flavor_name     = var.compute_flavor
  key_pair        = openstack_compute_keypair_v2.key.name
  security_groups = [openstack_networking_secgroup_v2.allow_all.name]
  network {
    port = openstack_networking_port_v2.cloud[each.key].id
  }
}

resource "openstack_networking_port_v2" "cloud" {
  for_each           = var.cloud_instances
  name               = "port_cloud_${each.key}"
  network_id         = openstack_networking_network_v2.cloud.id
  security_group_ids = [openstack_networking_secgroup_v2.allow_all.id]
  fixed_ip {
    subnet_id = openstack_networking_subnet_v2.cloud.id
  }
}

resource "openstack_compute_floatingip_v2" "cloud" {
  for_each = var.cloud_instances
  pool     = "ext-net"
}

resource "openstack_compute_floatingip_associate_v2" "cloud" {
  for_each    = var.cloud_instances
  floating_ip = openstack_compute_floatingip_v2.cloud[each.key].address
  instance_id = openstack_compute_instance_v2.cloud[each.key].id
}


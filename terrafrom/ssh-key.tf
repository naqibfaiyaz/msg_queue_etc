

resource "openstack_compute_keypair_v2" "key" {
    name = "keyyy"
    public_key = file("<PATH_TO_KEY>")
}

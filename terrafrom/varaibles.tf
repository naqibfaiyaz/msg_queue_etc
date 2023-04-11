variable "compute_image" {
  type    = string
  default = "Ubuntu-22-04-Jammy"
}

variable "compute_flavor" {
  type    = string
  default = "m1.medium"
}

variable "benchamrk_flavor" {
  type    = string
  default = "p1.large"
}

variable "cloud_network" {
  type = map(string)
  default = {
    subnet_name = "cloud"
    cidr        = "192.168.1.0/24"
  }
}

variable "cloud_instances" {
  type = set(string)
  default = ["etcd1", "etcd2", "etcd3", "etcd4", "etcd5"]
}

variable "benchamrk_instances" {
  type    = set(string)
  default = ["benchamrk"]
}

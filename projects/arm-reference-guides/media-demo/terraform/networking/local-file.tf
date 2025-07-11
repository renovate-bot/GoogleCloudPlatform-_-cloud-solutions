# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

locals {
  base_directory      = "${path.module}/../../"
  terraform_directory = "${local.base_directory}/terraform"
}

resource "local_file" "outputs_storage_auto_tfvars" {
  for_each = toset([
    "${local.terraform_directory}/container-cluster/networking-outputs.auto.tfvars",
  ])

  content = provider::terraform::encode_tfvars(
    {
      cluster_network_name    = local.network_name
      cluster_subnetwork_name = local.subnetwork_name
    }
  )
  file_permission = "0644"
  filename        = each.value
}

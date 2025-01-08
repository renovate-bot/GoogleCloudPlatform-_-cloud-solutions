# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

output "agent_name" {
  description = "The url to the agent service"
  value       = google_dialogflow_cx_agent.cc_agent.name
}

output "agent_gs_bucket" {
  description = "The gcs bucket to agent_playbook"
  value       = "gs://${google_storage_bucket.dialogflowcx_assets_bucket.name}"
}

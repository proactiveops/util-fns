variable "cloudwatch_vpce_security_group" {
  type        = string
  description = "ID of the security group containing the VPC endpoint for CloudWatch Logs"
  default     = null
}

variable "enabled_functions" {
  type        = list(string)
  description = "A list of functions to enable"
  default = [
    "ip_to_object",
    "jira_match",
    "redact"
  ]
}

variable "iam_role_permission_boundary" {
  type        = string
  description = "The ARN of the IAM policy to use as a permission boundary for the IAM role"
  default     = null
}

variable "iam_role_prefix" {
  type        = string
  description = "A prefix to use for the IAM role name"
  default     = ""
}

variable "namespace" {
  type        = string
  description = "The namespace prefix to use for all resources"
  default     = "util-fns"
}

variable "powertools_version" {
  type        = string
  description = "The version of the AWS Lambda Powertools Lambda layer"
  default     = "18"
}

variable "subnets" {
  type        = list(string)
  description = "A list of subnet IDs to use for the VPC"
}

variable "tags" {
  type        = map(string)
  description = "A map of tags to apply to all resources"
  default     = {}
}


locals {
  namespace       = var.namespace != "" ? "${var.namespace}-" : ""
  iam_role_prefix = var.iam_role_prefix != "" ? "${var.iam_role_prefix}-${local.namespace}" : local.namespace

  python_version = "python3.13"
}

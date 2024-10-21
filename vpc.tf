data "aws_subnet" "this" {
  for_each = toset(var.subnets)
  id       = each.value
}

data "aws_vpc" "this" {
  id = [for subnet in data.aws_subnet.this : subnet.vpc_id][0]
}

resource "aws_security_group" "this" {
  name_prefix = "${local.namespace}lambda-functions"

  description = "Security group for the ${local.namespace} lambda functions"

  vpc_id = data.aws_vpc.this.id

  tags = var.tags

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_vpc_security_group_egress_rule" "open" {
  count = var.cloudwatch_vpce_security_group == null ? 1 : 0

  security_group_id = aws_security_group.this.id
  description       = "Allow all HTTPS traffic out so we can log to CloudWatch"

  from_port = 443
  to_port   = 443

  ip_protocol = "tcp"
  cidr_ipv4   = "0.0.0.0/0"
}

resource "aws_vpc_security_group_egress_rule" "vpc" {
  count = var.cloudwatch_vpce_security_group != null ? 1 : 0

  security_group_id = aws_security_group.this.id
  description       = "Allow all traffic to the CWL VPCe"

  from_port = 443
  to_port   = 443

  ip_protocol = "tcp"

  referenced_security_group_id = var.cloudwatch_vpce_security_group
}

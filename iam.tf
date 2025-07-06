locals {
  iam_role_permission_boundary = var.iam_role_permission_boundary != null ? data.aws_iam_policy.permission_boundary[0].arn : null
}

data "aws_iam_policy" "permission_boundary" {
  count = var.iam_role_permission_boundary != null ? 1 : 0

  name = var.iam_role_permission_boundary
}

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = [
      "sts:AssumeRole"
    ]

    principals {
      type = "Service"
      identifiers = [
        "lambda.amazonaws.com"
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values = [
        data.aws_caller_identity.current.account_id
      ]
    }
  }
}

data "aws_iam_policy_document" "lambda" {

  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = [
      for group in aws_cloudwatch_log_group.lambda : "${group.arn}:log-stream:*"
    ]
  }

  statement {
    actions = [
      "ec2:CreateNetworkInterface",
      "ec2:DescribeNetworkInterfaces",
      "ec2:DeleteNetworkInterface",
    ]

    resources = ["*"]
  }
}

resource "aws_iam_role" "lambda" {
  name        = "${local.iam_role_prefix}lambda"
  description = "Used by the ${local.iam_role_prefix} lambda functions"

  assume_role_policy   = data.aws_iam_policy_document.lambda_assume.json
  permissions_boundary = local.iam_role_permission_boundary

  tags = var.tags
}

resource "aws_iam_policy" "lambda" {
  name        = aws_iam_role.lambda.name
  description = "Policy for lambda functions"
  policy      = data.aws_iam_policy_document.lambda.json

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "lambda" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda.arn
}

locals {
  functions = toset(var.enabled_functions)
}

data "archive_file" "this" {
  for_each = local.functions

  type = "zip"

  source_file = join("/", [path.module, "functions", each.key, "${each.key}.py"])
  output_path = join("/", [path.module, "functions", "${each.key}.zip"])
}

resource "aws_lambda_function" "lambda" {
  for_each = local.functions

  function_name = "${local.namespace}${each.key}"
  handler       = "${each.key}.handler"

  runtime       = "python3.12"
  timeout       = 5
  memory_size   = 128
  architectures = ["arm64"]

  role = aws_iam_role.lambda.arn

  filename         = data.archive_file.this[each.key].output_path
  source_code_hash = data.archive_file.this[each.key].output_sha256

  vpc_config {
    subnet_ids         = [for subnet in data.aws_subnet.this : subnet.id]
    security_group_ids = [aws_security_group.this.id]
  }

  layers = [
    "arn:aws:lambda:${data.aws_region.current.name}:017000801446:layer:AWSLambdaPowertoolsPythonV3-python312-arm64:${var.powertools_version}"
  ]

  tags = var.tags

  depends_on = [
    aws_iam_role_policy_attachment.lambda,
  ]
}

#tfsec:ignore:aws-cloudwatch-log-group-customer-key CWL-SSE is adequate the data being stored.
resource "aws_cloudwatch_log_group" "lambda" {
  for_each = local.functions

  name = "/aws/lambda/${local.namespace}${each.key}"

  retention_in_days = 30

  tags = var.tags
}

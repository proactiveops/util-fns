output "lambda_functions" {
  description = "A map of the Lambda function names to their ARNs"
  value = {
    for key, value in local.functions : key => aws_lambda_function.lambda[key].arn
  }
}

output "lambda_role" {
  description = "The ARN of the IAM role used by the Lambda functions"
  value       = aws_iam_role.lambda.arn
}

output "security_group" {
  description = "The ID of the security group used by the Lambda functions"
  value       = aws_security_group.this.id
}

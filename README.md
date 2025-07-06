# Utility Lambda Functions for AWS Step Functions

This is a collection of small AWS Lambda functions I use in my AWS Step Functions.

These functions adopt the [unix philosophy of "do one thing and do it well"](http://www.catb.org/esr/writings/taoup/html/ch01s06.html).

[AWS Powertools for Lambda](https://docs.powertools.aws.dev/lambda/python) is the only external run time dependency. This is included via a Lambda layer. Everything else comes from core Python.

These functions do not require network access. If you have a CloudWatch VPC endpoint, then the functions use it, otherwise HTTPS egress is open to the internet so logging works.

The functions all run on ARM64 using the default terraform configuration.

## Example

```hcl2
module "util_fns" {
  source = "git@github.com:proactiveops/util-fns.git?ref=main"

  cloudwatch_vpce_security_group = "sg-4badf00d"

  subnets = "subnet-d34db33f"
  tags    = var.tags

  enabled_functions = [
    "ip_to_object",
    "jira_match",
    "redact"
  ]
}
```

## IP to Object

Wrapper for [Python's core `ipaddress` library](https://docs.python.org/3/library/ipaddress.html). The function supports both IPv4 and IPv6 addresses.

Expected payload:

```json
{
    "ip": "198.51.100.1"
}
```

## Jira Match

Search for Jira ticket references in a string. Returns unique matches as a list.

Expected payload:

```json
{
    "body": "ABC-123 This string contains 2 ticket references ZYX-987"
}
```

## Redact Text

Redact PII entities in a string identified by Amazon Comprehend. Comprehend only supports redaction an asynchronous batch operation. This function performs the redaction on a string in real time. Other sources of redaction rules can be used, so long as they use [the Amazon Comprehend PII Entities schema](https://docs.aws.amazon.com/comprehend/latest/dg/how-pii.html#how-pii-locate).

Use the optional `ignored_entities` property with a list of entities to not redact.

```json
{
  "text": "Hello Paul Santos. The latest statement for your credit card account 4111-1111-1111-1111 was mailed to 123 Any Street, Seattle, WA 98109.",
  "entities": [
    {
      "Score": 0.9999669790267944,
      "Type": "NAME",
      "BeginOffset": 6,
      "EndOffset": 18
    },
    {
      "Score": 0.8905550241470337,
      "Type": "CREDIT_DEBIT_NUMBER",
      "BeginOffset": 69,
      "EndOffset": 88
    },
    {
      "Score": 0.9999889731407166,
      "Type": "ADDRESS",
      "BeginOffset": 103,
      "EndOffset": 138
    }
  ],
  "ignored_entities": [
    "NAME"
  ]
}
```

# Deprecated Functions

## In List

[Step Functions intrinsic functions provide some array operations](https://docs.aws.amazon.com/step-functions/latest/dg/intrinsic-functions.html#asl-intrsc-func-arrays). Unfortunately the `States.ArrayContains` function returns a boolean, rather than the position of the item in the list.

The position of the item in the zero based array is returned as an integer. -1 is returned if the item isn't found.

Expected payload:

```json
{
    "list": ["apple", "banana", "cherry"], 
    "item": "banana"
}
```

## In String

Searches for a substring within a string. Whitespace is trimmed from both the string and substring.

The function returns the starting position of the substring within the string. If the substring isn't found -1 is returned.

```json
{
    "string": "team",
    "substring": "i"
}
```

The following function are no longer being maintained. [Use JSONata in your Step Functions](https://aws.amazon.com/blogs/compute/simplifying-developer-experience-with-variables-and-jsonata-in-aws-step-functions/) instead.

## ISO Format to Timestamp

Converts an ISO 8601 format date time string to a unix timestamp. If the string isn't provided, the current UTC timestamp is returned.

Expected payload:

```json
{
    "isoformat": "1985-10-26T08:33:00Z"
}
```

## Lookup Key

The function looks up a key in a JSON object (or Python dictionary) and returns the value. If the key isn't found, null is returned.

Empty JSON objects are often converted to empty lists. This function handles this scenario and returns null.

Expected payload:

```json
{
    "values": {
        "key1": "value",
        "key2": "another-value"
    },
    "key": "key1"
}
```

## Unix Timestamp to ISO Format

Converts a unix timestamp to an ISO 8601 format date time string. If the timestamp isn't provided, the current time UTC is used.

Expected payload:

```json
{
    "timestamp": 499163580
}
```

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.0 |
| <a name="requirement_archive"></a> [archive](#requirement\_archive) | >= 2.0, < 3.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 5.0, < 6.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | 2.7.1 |
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.98.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_log_group.lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_iam_policy.lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_lambda_function.lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_security_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | resource |
| [aws_vpc_security_group_egress_rule.open](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc_security_group_egress_rule) | resource |
| [aws_vpc_security_group_egress_rule.vpc](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc_security_group_egress_rule) | resource |
| [archive_file.this](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [aws_iam_policy.permission_boundary](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy) | data source |
| [aws_iam_policy_document.lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.lambda_assume](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_region.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |
| [aws_subnet.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/subnet) | data source |
| [aws_vpc.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/vpc) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_cloudwatch_vpce_security_group"></a> [cloudwatch\_vpce\_security\_group](#input\_cloudwatch\_vpce\_security\_group) | ID of the security group containing the VPC endpoint for CloudWatch Logs | `string` | `null` | no |
| <a name="input_enabled_functions"></a> [enabled\_functions](#input\_enabled\_functions) | A list of functions to enable | `list(string)` | <pre>[<br/>  "ip_to_object",<br/>  "jira_match",<br/>  "redact"<br/>]</pre> | no |
| <a name="input_iam_role_permission_boundary"></a> [iam\_role\_permission\_boundary](#input\_iam\_role\_permission\_boundary) | The ARN of the IAM policy to use as a permission boundary for the IAM role | `string` | `null` | no |
| <a name="input_iam_role_prefix"></a> [iam\_role\_prefix](#input\_iam\_role\_prefix) | A prefix to use for the IAM role name | `string` | `""` | no |
| <a name="input_namespace"></a> [namespace](#input\_namespace) | The namespace prefix to use for all resources | `string` | `"util-fns"` | no |
| <a name="input_powertools_version"></a> [powertools\_version](#input\_powertools\_version) | The version of the AWS Lambda Powertools Lambda layer | `string` | `"18"` | no |
| <a name="input_subnets"></a> [subnets](#input\_subnets) | A list of subnet IDs to use for the VPC | `list(string)` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | A map of tags to apply to all resources | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_lambda_function_arns"></a> [lambda\_function\_arns](#output\_lambda\_function\_arns) | A map of the Lambda function ARNs indexed by their short name |
| <a name="output_lambda_function_names"></a> [lambda\_function\_names](#output\_lambda\_function\_names) | A map of the Lambda function names indexed by their short name |
| <a name="output_lambda_functions"></a> [lambda\_functions](#output\_lambda\_functions) | Deprecated. Use `lambda_function_arns` instead. |
| <a name="output_lambda_role"></a> [lambda\_role](#output\_lambda\_role) | The ARN of the IAM role used by the Lambda functions |
| <a name="output_security_group"></a> [security\_group](#output\_security\_group) | The ID of the security group used by the Lambda functions |
<!-- END_TF_DOCS -->
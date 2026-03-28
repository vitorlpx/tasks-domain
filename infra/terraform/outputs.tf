output "dynamodb_table_name" {
  description = "Nome da tabela DynamoDB criada"
  value       = aws_dynamodb_table.tasks.name
}

output "dynamodb_table_arn" {
  description = "ARN da tabela DynamoDB"
  value       = aws_dynamodb_table.tasks.arn
}

output "s3_bucket_name" {
  description = "Nome do bucket S3 criado"
  value       = var.enable_s3 ? aws_s3_bucket.uploads[0].id : "S3 não habilitado neste ambiente"
}
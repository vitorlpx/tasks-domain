variable "project_name" {
  description = "Nome do projeto"
  type        = string
}

variable "enviroment" {
  description = "Ambiente de execução (local, dev, hom, prod)"
  type        = string
}

variable "aws_region" {
  description = "Região AWS"
  type        = string
  default     = "us-east-1"
}

variable "dynamodb_table_name" {
  description = "Nome da tabela DynamoDB"
  type        = string
}

variable "enable_s3" {
  description = "Habilitar criação do bucket S3"
  type        = bool
  default     = false
}

variable "enable_s3_lifecycle" {
  description = "Habilitar lifecycle rules do S3 (não suportado no LocalStack free)"
  type        = bool
  default     = false
}

variable "s3_bucket_name" {
  description = "Nome do bucket S3"
  type        = string
  default     = ""
}

variable "localstack_endpoint" {
  description = "Endpoint do LocalStack — apenas para ambiente local"
  type        = string
  default     = ""
}
resource "aws_dynamodb_table" "tasks" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Project     = var.project_name
    Environment = var.enviroment
  }
}

resource "aws_s3_bucket" "uploads" {
  count  = var.enable_s3 ? 1 : 0
  bucket = var.s3_bucket_name

  tags = {
    Project     = var.project_name
    Environment = var.enviroment
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "uploads_lifecycle" {
  count  = var.enable_s3 && var.enable_s3_lifecycle ? 1 : 0
  bucket = aws_s3_bucket.uploads[0].id

  rule {
    id     = "transition-to-cheaper-storage"
    status = "Enabled"

    filter {}
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }
  }
}
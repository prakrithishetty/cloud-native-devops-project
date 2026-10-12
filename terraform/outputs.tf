
output "aws_region" {
  description = "AWS region configured for this project"
  value       = var.aws_region
}

output "project_name" {
  description = "Project name"
  value       = var.project_name
}

output "environment" {
  description = "Configured environment"
  value       = var.environment
}

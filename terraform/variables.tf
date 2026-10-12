
variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Name of the DevOps project"
  type        = string
  default     = "cloud-native-devops"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "development"
}

variable "aws_region" {
    description = "AWS region"
    default = "eu-west-3"
}

variable "instance_type" {
    description = "EC2 instance type"
    default = "t3.micro"
}

variable "project_name"{
    description = "Project name"
    default = "ml-devops-pipeline"
}
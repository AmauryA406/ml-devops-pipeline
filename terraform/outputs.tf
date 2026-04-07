output "instance_public_ip" {
    description = "Public IP of the EC2 instance"
    value = aws_instance.main.public_ip
}

output "ecr_repository_url" {
    description = "ECR repository URL"
    value = aws_ecr_repository.main.repository_url
}
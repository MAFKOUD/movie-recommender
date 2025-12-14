terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket  = "infrastats-g2mg05"
    key     = "g2mg05.tfstate"
    region  = "eu-west-3"
    encrypt = true
  }
}

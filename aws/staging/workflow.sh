# Login to the ECR registry
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 556359875842.dkr.ecr.us-east-2.amazonaws.com

# Build and push application image
docker build --file Dockerfile --tag 556359875842.dkr.ecr.us-east-2.amazonaws.com/backend:staging .
docker push 556359875842.dkr.ecr.us-east-2.amazonaws.com/backend:staging

# Register task definition
aws ecs register-task-definition --cli-input-json file://aws/staging/task.json

# Run the latest version of the task
aws ecs run-task --cluster staging --task-definition application-staging --count 1

# Run the migration task
aws ecs run-task --cluster staging --task-definition application-staging --overrides file://aws/staging/migration-override.json --enable-execute-command --count 1

# Create and start service
aws ecs create-service --cli-input-json file://aws/staging/service.json

# Update service
aws ecs update-service --cluster staging --service application-staging --task-definition application-staging --force-new-deployment

import pulumi
import pulumi_aws as aws
import json
import os

# Configuration
config = pulumi.Config()
aws_config = pulumi.Config("aws")
region = aws_config.require("region")

# Create IAM Role for Lambda
lambda_role = aws.iam.Role("lambda-managed-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            }
        }]
    }),
    tags={
        "Name": "lambda-managed-instances-role",
        "Project": "Lambda-Managed-Server"
    }
)

# Attach basic Lambda execution policy
lambda_policy_attachment = aws.iam.RolePolicyAttachment("lambda-basic-execution",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
)

# Demo 1: Data Processing Lambda Function
data_processor_function = aws.lambda_.Function("data-processor",
    runtime="python3.13",
    role=lambda_role.arn,
    handler="data_processor.handler",
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./lambda")
    }),
    timeout=900,  # 15 minutes
    memory_size=3008,  # 3 GB
    environment={
        "variables": {
            "INSTANCE_TYPE": "managed",
            "DEMO_NAME": "Data Processing Pipeline"
        }
    },
    tags={
        "Name": "data-processor-managed",
        "Demo": "Data Processing",
        "Project": "Lambda-Managed-Server"
    }
)

# Function URL for Data Processor
data_processor_url = aws.lambda_.FunctionUrl("data-processor-url",
    function_name=data_processor_function.name,
    authorization_type="NONE",
    cors={
        "allow_origins": ["*"],
        "allow_methods": ["GET", "POST"],
        "allow_headers": ["*"],
        "max_age": 3600
    }
)

# Demo 2: API Handler Lambda Function
api_handler_function = aws.lambda_.Function("api-handler",
    runtime="python3.13",
    role=lambda_role.arn,
    handler="api_handler.handler",
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./lambda")
    }),
    timeout=300,  # 5 minutes
    memory_size=2048,  # 2 GB
    environment={
        "variables": {
            "INSTANCE_TYPE": "managed",
            "DEMO_NAME": "API with Connection Pooling",
            "MAX_CONNECTIONS": "100"
        }
    },
    tags={
        "Name": "api-handler-managed",
        "Demo": "API Handler",
        "Project": "Lambda-Managed-Server"
    }
)

# Function URL for API Handler
api_handler_url = aws.lambda_.FunctionUrl("api-handler-url",
    function_name=api_handler_function.name,
    authorization_type="NONE",
    cors={
        "allow_origins": ["*"],
        "allow_methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["*"],
        "max_age": 3600
    }
)

# Demo 3: WebSocket Handler Lambda Function
websocket_handler_function = aws.lambda_.Function("websocket-handler",
    runtime="python3.13",
    role=lambda_role.arn,
    handler="websocket_handler.handler",
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./lambda")
    }),
    timeout=300,  # 5 minutes
    memory_size=1024,  # 1 GB
    environment={
        "variables": {
            "INSTANCE_TYPE": "managed",
            "DEMO_NAME": "WebSocket Handler"
        }
    },
    tags={
        "Name": "websocket-handler-managed",
        "Demo": "WebSocket",
        "Project": "Lambda-Managed-Server"
    }
)

# Function URL for WebSocket Handler
websocket_handler_url = aws.lambda_.FunctionUrl("websocket-handler-url",
    function_name=websocket_handler_function.name,
    authorization_type="NONE",
    cors={
        "allow_origins": ["*"],
        "allow_methods": ["GET", "POST"],
        "allow_headers": ["*"],
        "max_age": 3600
    }
)

# Export outputs
pulumi.export("region", region)
pulumi.export("data_processor_url", data_processor_url.function_url)
pulumi.export("api_handler_url", api_handler_url.function_url)
pulumi.export("websocket_handler_url", websocket_handler_url.function_url)
pulumi.export("data_processor_function_name", data_processor_function.name)
pulumi.export("api_handler_function_name", api_handler_function.name)
pulumi.export("websocket_handler_function_name", websocket_handler_function.name)

# Export test commands
pulumi.export("test_commands", {
    "data_processor_small": data_processor_url.function_url.apply(lambda url: f"curl \"{url}?file_size=small\""),
    "data_processor_large": data_processor_url.function_url.apply(lambda url: f"curl \"{url}?file_size=large\""),
    "api_handler": api_handler_url.function_url.apply(lambda url: f"curl {url}"),
    "websocket_handler": websocket_handler_url.function_url.apply(lambda url: f"curl {url}")
})

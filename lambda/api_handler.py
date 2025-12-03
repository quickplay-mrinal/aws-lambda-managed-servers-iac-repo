import json
import time
import os
from datetime import datetime

# Simulate connection pool (in real scenario, use database connection)
connection_pool = {
    "initialized": False,
    "connections": 0,
    "max_connections": 100
}

def initialize_connection_pool():
    """Initialize persistent database connection pool"""
    if not connection_pool["initialized"]:
        print("Initializing connection pool...")
        time.sleep(0.5)  # Simulate connection setup
        connection_pool["initialized"] = True
        connection_pool["connections"] = 10
        print(f"Connection pool initialized with {connection_pool['connections']} connections")

def handler(event, context):
    """
    Demo 2: API with Database Connection Pooling
    Demonstrates persistent connections with Lambda Managed Instances
    """
    
    # Initialize connection pool (persists across invocations)
    initialize_connection_pool()
    
    # Parse request
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    
    # Simulate database query
    start_query = time.time()
    time.sleep(0.1)  # Simulate DB query
    query_time = time.time() - start_query
    
    # Sample data
    users = [
        {"id": 1, "name": "Alice", "role": "Admin"},
        {"id": 2, "name": "Bob", "role": "Developer"},
        {"id": 3, "name": "Charlie", "role": "Manager"}
    ]
    
    response_body = {
        "message": "API request processed successfully!",
        "demo": "Lambda Managed Instances - API with Connection Pooling",
        "request": {
            "method": http_method,
            "path": path,
            "timestamp": datetime.utcnow().isoformat()
        },
        "data": users,
        "performance": {
            "query_time_ms": round(query_time * 1000, 2),
            "connection_pool_active": connection_pool["initialized"],
            "available_connections": connection_pool["connections"],
            "cold_start": not connection_pool["initialized"]
        },
        "instance_info": {
            "type": "managed",
            "memory_mb": os.environ.get('AWS_LAMBDA_FUNCTION_MEMORY_SIZE', 'N/A'),
            "function_name": os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'N/A')
        },
        "benefits": [
            "Persistent database connections",
            "Reduced connection overhead",
            "Improved API response times",
            "Connection pooling optimization"
        ]
    }
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "X-Connection-Pool": "Active" if connection_pool["initialized"] else "Initializing"
        },
        "body": json.dumps(response_body)
    }

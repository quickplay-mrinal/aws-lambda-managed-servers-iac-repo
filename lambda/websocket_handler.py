import json
import time
import os
from datetime import datetime

# Simulate WebSocket connection state
websocket_connections = {
    "active_connections": 0,
    "messages_processed": 0,
    "last_activity": None
}

def handler(event, context):
    """
    Demo 3: WebSocket Handler
    Demonstrates real-time connection handling with Lambda Managed Instances
    """
    
    route_key = event.get('requestContext', {}).get('routeKey', 'UNKNOWN')
    connection_id = event.get('requestContext', {}).get('connectionId', 'N/A')
    
    # Handle different WebSocket events
    if route_key == '$connect':
        websocket_connections["active_connections"] += 1
        action = "Connected"
        message = f"WebSocket connection established: {connection_id}"
        
    elif route_key == '$disconnect':
        websocket_connections["active_connections"] = max(0, websocket_connections["active_connections"] - 1)
        action = "Disconnected"
        message = f"WebSocket connection closed: {connection_id}"
        
    elif route_key == '$default':
        websocket_connections["messages_processed"] += 1
        action = "Message Received"
        
        # Parse message body
        body = json.loads(event.get('body', '{}'))
        message = f"Processed message: {body.get('message', 'No message')}"
        
    else:
        action = "Unknown"
        message = f"Unknown route: {route_key}"
    
    websocket_connections["last_activity"] = datetime.utcnow().isoformat()
    
    response_body = {
        "action": action,
        "message": message,
        "demo": "Lambda Managed Instances - WebSocket Handler",
        "connection_info": {
            "connection_id": connection_id,
            "route": route_key,
            "timestamp": datetime.utcnow().isoformat()
        },
        "statistics": {
            "active_connections": websocket_connections["active_connections"],
            "messages_processed": websocket_connections["messages_processed"],
            "last_activity": websocket_connections["last_activity"]
        },
        "instance_info": {
            "type": "managed",
            "memory_mb": os.environ.get('AWS_LAMBDA_FUNCTION_MEMORY_SIZE', 'N/A'),
            "function_name": os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'N/A')
        },
        "benefits": [
            "Persistent WebSocket connections",
            "Real-time message processing",
            "Reduced connection overhead",
            "Scalable real-time applications"
        ]
    }
    
    return {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }

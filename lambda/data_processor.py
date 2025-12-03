import json
import time
import os
from datetime import datetime

def handler(event, context):
    """
    Demo 1: Data Processing Pipeline
    Demonstrates Lambda Managed Instances for long-running data processing
    """
    
    start_time = time.time()
    
    # Simulate processing large dataset
    file_size = event.get('queryStringParameters', {}).get('file_size', 'medium')
    
    processing_times = {
        'small': 2,
        'medium': 5,
        'large': 10
    }
    
    process_duration = processing_times.get(file_size, 5)
    
    # Simulate data processing
    records_processed = 0
    batch_size = 1000
    
    for i in range(process_duration):
        time.sleep(1)
        records_processed += batch_size
        print(f"Processed {records_processed} records...")
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "message": "Data processing completed successfully!",
            "demo": "Lambda Managed Instances - Data Processing",
            "details": {
                "file_size": file_size,
                "records_processed": records_processed,
                "execution_time_seconds": round(execution_time, 2),
                "timestamp": datetime.utcnow().isoformat(),
                "instance_type": "managed",
                "memory_mb": os.environ.get('AWS_LAMBDA_FUNCTION_MEMORY_SIZE', 'N/A'),
                "function_name": os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'N/A')
            },
            "benefits": [
                "Extended execution time for large datasets",
                "Optimized memory usage",
                "Cost-efficient per-second billing",
                "Automatic scaling"
            ]
        })
    }
    
    return response

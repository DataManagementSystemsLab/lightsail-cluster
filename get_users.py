import boto3

# Initialize the DynamoDB resource
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")  # Replace with your region
users_table = dynamodb.Table("owuser")

def dump_all_users():
    try:
        response = users_table.scan()
        items = response.get("Items", [])

        # Continue scanning if there are more items
        while "LastEvaluatedKey" in response:
            response = users_table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            items.extend(response.get("Items", []))

        return items
    except Exception as e:
        print(f"Error scanning DynamoDB: {e}")
        return []

if __name__ == "__main__":
    all_users = dump_all_users()
    for user in all_users:
        print(user)

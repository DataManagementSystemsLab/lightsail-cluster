import hashlib
import time
import pyotp

from datetime import datetime , timezone, timedelta
import datetime as datetime2
import boto3
from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Key
import logging

log = logging.getLogger(__name__)
def get_hashed_password(user, p):
    st= user+p
    h1=hashlib.sha1(st.encode("utf-8"))
    
    hash_p= str(h1.hexdigest())
    log.debug(hash_p)
    print(hash_p)
    return hash_p

def get_user(dynamotable, user_id):
    response = dynamotable.query(
        ProjectionExpression="username,  password, secret_code",
        KeyConditionExpression=(
            Key('username').eq(user_id)
        )
    )
    if 'Items' not in response:
        log.info("User not found.")

        return None
    if response['Count']==0:
        log.info("could not find user")
        
        log.info(user_id)
        return None

    return response['Items'][0]


def update_user(dynamotable, user_id):
    current_time = datetime.now(timezone.utc)
    response = dynamotable.update_item(
    Key={
        "username": user_id  # Replace with your primary key
    },
    UpdateExpression="SET last_login = :val",  # Set new value
    ExpressionAttributeValues={
        ":val":  current_time.isoformat()   # New value to update
    },
        ReturnValues="UPDATED_NEW"  # Return the updated attributes
    )
    print("Updated Item:", response["Attributes"])
    

def check_user(userid, passwd,code):
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1") # N. Virginia")  # Change to your AWS region
    table_name = "owuser"
    dynamotable = dynamodb.Table(table_name)  # Replace with your table name
    current_time = datetime.now(timezone.utc)
    
    #timestamp = datetime.strptime(datetime.now(), '%b %d %Y %H:%M:%S %Z')
    #unix_timestamp=time.mktime(timestamp.timetuple())
    try:
        code=int(code)
        is_valid=False
    
        passwd=get_hashed_password(userid, passwd)
    
        user=get_user(dynamotable,userid)
        print(user)
        log.info(user)
        if  user is not None:
          if passwd==user['password']:  
              secret_key=user['secret_code']
              totp = pyotp.TOTP(secret_key)
              prev_comp=-1
              for delta in range(-50,100,4):
                  comp = totp.at(current_time + datetime2.timedelta(seconds=delta))  # Fix timedelta argument            
                  comp= int(comp)
                  if comp==prev_comp:
                      continue
                  prev_comp=comp
                  log.debug(comp)
                  is_valid = comp == code
                  if is_valid:
                    break
        if is_valid:
            update_user(dynamotable,userid)      
    except:
        is_valid=False
    return is_valid            



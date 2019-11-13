import os
import boto3
from botocore.exceptions import (
    NoRegionError,
    PartialCredentialsError,
    NoCredentialsError,
    ClientError
)

from .settings import (
    SEPARATOR,
    NO_REGION_ERROR,
    NO_CREDENTIALS_ERROR,
    WRONG_CREDENTIALS_ERROR
)

def get_aws_ecs_clusters():
    try:
        return boto3.client('ecs').list_clusters()['clusterArns']
    except NoRegionError:
        print(NO_REGION_ERROR)
        exit(1)
    except (PartialCredentialsError, NoCredentialsError):
        print(NO_CREDENTIALS_ERROR)
        exit(1)
    except ClientError:
        print(WRONG_CREDENTIALS_ERROR)
        exit(1)

def get_aws_ecs_services(cluster):
    try:
        return boto3.client('ecs').list_services(cluster=cluster)['serviceArns']
    except NoRegionError:
        print(NO_REGION_ERROR)
        exit(1)
    except (PartialCredentialsError, NoCredentialsError):
        print(NO_CREDENTIALS_ERROR)
        exit(1)
    except ClientError:
        print(WRONG_CREDENTIALS_ERROR)
        exit(1)

def get_aws_ecs_tasks(cluster, service):
    try:
        return boto3.client('ecs').list_tasks(cluster=cluster, serviceName=service, desiredStatus='RUNNING')['taskArns']
    except NoRegionError:
        print(NO_REGION_ERROR)
        exit(1)
    except (PartialCredentialsError, NoCredentialsError):
        print(NO_CREDENTIALS_ERROR)
        exit(1)
    except ClientError:
        print(WRONG_CREDENTIALS_ERROR)
        exit(1)

def get_aws_ecs_instance(cluster, tasks):
    try:
        return boto3.client('ecs').describe_tasks(cluster=cluster, tasks=task)['containerInstanceArn']
    except NoRegionError:
        print(NO_REGION_ERROR)
        exit(1)
    except (PartialCredentialsError, NoCredentialsError):
        print(NO_CREDENTIALS_ERROR)
        exit(1)
    except ClientError:
        print(WRONG_CREDENTIALS_ERROR)
        exit(1)
CONTAINER_INSTANCE_ID=$( aws ecs describe-tasks --cluster=$CLUSTER --tasks $TASK_ID --output json | jq -r '.tasks[0].containerInstanceArn' )
EC2_INSTANCE=$( aws ecs describe-container-instances --cluster=staging --container-instances $CONTAINER_INSTANCE_ID --output json | jq -r '.containerInstances[0].ec2InstanceId' )
EC2_IP=$( aws ec2 describe-instances --instance-ids $EC2_INSTANCE --output json | jq -r '.Reservations[0].Instances[0].PublicIpAddress' )


def new(region):
    ecs_data = {}
    ecs_data[region] = {}
    ecs_data[region]['clusters'] = {}
    clusters = get_aws_ecs_clusters()
    for cluster in clusters:
        ecs_data[region]['clusters'][cluster] = get_aws_ecs_services(cluster)
        for service in ecs_data[region][cluster]:
            ecs_data[region][cluster][service] = get_aws_ecs_tasks(cluster, service)

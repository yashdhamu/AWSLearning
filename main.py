import boto3


class AWSEC2Instance:
    def __init__(self):
        self.AWS_ACCESS_KEY_ID = ""
        self.AWS_SECRET_ACCESS_KEY = ''
        self.REGION = "us-east-1"
        self.ec2 = boto3.resource('ec2',
                                  region_name=self.REGION,
                                  aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY)

    def createEC2Instance(self, AMI_ID='ami-0c7217cdde317cfec',
                          INSTANCE_TYPE='t2.micro',
                          SECURITY_GROUP='launch-wizard-1',
                          KEY_PAIR='yashdhamu'):
        instance = self.ec2.create_instances(
            ImageId=AMI_ID,
            MinCount=1,
            MaxCount=1,
            InstanceType=INSTANCE_TYPE,
            KeyName=KEY_PAIR,
            SecurityGroups=[SECURITY_GROUP],
            TagSpecifications=[
                                {
                                    'ResourceType': 'instance',
                                    'Tags': [{'Key': 'Name','Value': 'WebTier'}]
                                }
                               ]
        )
        print("Instance created with ID:", instance[0].id)
        print('Details:\n', instance)
        return instance[0].id

    def startEC2Instance(self, instance_id):
        instance = self.ec2.Instance(instance_id)
        instance.start()
        print("Instance started with ID:", instance_id)

    def stopEC2Instance(self, instance_id):
        instance = self.ec2.Instance(instance_id)
        instance.stop()
        print("Instance stopped with ID:", instance_id)

    def terminateEC2Instance(self, instance_id):
        instance = self.ec2.Instance(instance_id)
        instance.terminate()
        print("Instance terminated with ID:", instance_id)

class AWSEllasticIP:
    def __init__(self):
        self.AWS_ACCESS_KEY_ID = ""
        self.AWS_SECRET_ACCESS_KEY = ''
        self.REGION = "us-east-1"
        self.ec2 = boto3.client('ec2',
                                  region_name=self.REGION,
                                  aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY)

    def allocateElasticIP(self):
        response = self.ec2.allocate_address(Domain='vpc')
        print("Elastic IP allocated with ID:", response['AllocationId'])
        print("Details:\n", response)
        return response['AllocationId']

    def associateElasticIP(self, instance_id, allocation_id):
        response = self.ec2.associate_address(AllocationId=allocation_id, InstanceId=instance_id)
        print("Elastic IP associated with instance ID:", instance_id, "using association ID:", response['AssociationId'])
        print("Details:\n", response)
        return response['AssociationId']

    def disassociateElasticIP(self, association_id):
        response = self.ec2.disassociate_address(AssociationId=association_id)
        print("Elastic IP disassociated with association ID:", association_id)
        print("Details:\n", response)
        return response

    def releaseElasticIP(self, allocation_id):
        response = self.ec2.release_address(AllocationId=allocation_id)
        print("Elastic IP released with allocation ID:", allocation_id)
        print("Details:\n", response)
        return response






def main():
    # ec2 = AWSEC2Instance()
    elasticIP = AWSEllasticIP()
    # instance_id = ec2.createEC2Instance() #i-0dd18108ca8838dcb
    # allocation_id = elasticIP.allocateElasticIP() # eipalloc-0d0eb43f5191a925b
    # instance_id = 'i-0dd18108ca8838dcb'
    allocation_id = 'eipalloc-0d0eb43f5191a925b'
    # association_id = elasticIP.associateElasticIP(instance_id, allocation_id)
    # print(association_id)
    # association_id = 'eipassoc-0c22970734046057c'
    # elasticIP.disassociateElasticIP(association_id)
    elasticIP.releaseElasticIP(allocation_id)
    # ec2.startEC2Instance(instance_id)
    # ec2.stopEC2Instance(instance_id)
    # ec2.terminateEC2Instance(instance_id)


if __name__ == '__main__':
    main()

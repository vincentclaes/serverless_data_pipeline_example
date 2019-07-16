# SERVERLESS-DATA-PIPELINE

Using AWS Cloud Services Lambda, S3, Glue and Athena we are going to build a data pipeline written in python and deploy it using the Serverless Framework.

You can read the tutorial here: 

https://medium.com/@vincentclaes_43752/build-a-serverless-data-pipeline-on-aws-7c7d498d9707

# Deploy and run the data pipeline

make sure you have correct user and roles defined:

### Create a user to access AWS

create an admin user using the AWS console and set the credentials under a [serverless] section in the credentials file located in 
    
    ~/.aws/credentials

a step by step guide can be found here: https://medium.com/@vincentclaes_43752/create-a-user-for-the-serverless-framework-8e5c336d47c7

### Create the necessary roles
for our project we need two roles; 
* one for lambda 
* one for glue.

create a role with administrator access for both these roles and keep the ARN somewhere accessible. 
A step by step guide to creating a role can be found here: https://medium.com/@vincentclaes_43752/create-a-role-on-aws-for-the-serverless-framework-for-any-resource-c49712a5eee0

Replace the ARN of the lambda role and the ARN of the Glue role with the ones defined in the serverless.yml file.
There is a comment above both roles that indicates that you should replace the ARN.

### configure your local environment

under the root of this project execute:

    export AWS_PROFILE="serverless"
    pip install awscli
    sudo npm install -g serverless
    npm install serverless-s3-remover
    
to deploy the data pipeline execute:

    # replace the `unique-identifier` with something unique
    sls deploy --stage unique-identifier
    
to remove the data pipeline execute:

    # replace the `unique-identifier` with something unique
    sls remove --stage unique-identifier
    
to get more context please refer to the article: https://medium.com/@vincentclaes_43752/build-a-serverless-data-pipeline-on-aws-7c7d498d9707

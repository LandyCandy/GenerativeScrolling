#! /bin/bash

#exit on non-zero return from any command, export vars inherited by subsequent commands
set -ea

# run tests
. ../setenv.sh
../dev-env/bin/python3 -m py_compile ./lambda_function.py

# Clean previous archive
rm -f generative-scrolling-serve-page-lambda-package.zip

# Zip lambda function file into archive
zip generative-scrolling-serve-page-lambda-package.zip *.py
zip -g generative-scrolling-serve-page-lambda-package.zip *.html

# Upload to s3 location for automatic deployment to lambda
aws s3 cp generative-scrolling-serve-page-lambda-package.zip s3://myshitbucket/lambda_deployment_zips/generative-scrolling-serve-page-lambda-package.zip

# Deploy code to lambda
aws lambda update-function-code --region us-east-1 --function-name generative-scrolling-serve-page --s3-bucket myshitbucket --s3-key lambda_deployment_zips/generative-scrolling-serve-page-lambda-package.zip
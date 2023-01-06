#! /bin/bash

#exit on non-zero return from any command, export vars inherited by subsequent commands
set -ea

# run tests
. ../setenv.sh
../dev-env/bin/python3 -m py_compile ./lambda_function.py

# Clean previous archive
rm -f generative-scrolling-initial-page-lambda-package.zip

# Navigate to libraries dir
cd ./python/lib/python3.9/site-packages

# Zip libs into new archive
zip -r ../../../../generative-scrolling-initial-page-lambda-package.zip .

# Navigate up to source dir
cd ../../../../

# Zip lambda function file into archive
zip -g generative-scrolling-initial-page-lambda-package.zip *.py

# Upload to s3 location for automatic deployment to lambda
aws s3 cp generative-scrolling-initial-page-lambda-package.zip s3://myshitbucket/lambda_deployment_zips/generative-scrolling-initial-page-lambda-package.zip

# Deploy code to lambda
aws lambda update-function-code --region us-east-1 --function-name generative-scrolling-generate-snip --s3-bucket myshitbucket --s3-key lambda_deployment_zips/generative-scrolling-initial-page-lambda-package.zip
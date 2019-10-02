#!/bin/bash
# Create a datascience-bot.zip file for deployment to AWS Lambda

EPOCH=$(date +%s)
VERSION=$(python setup.py --version)
TEMPDIR="temp-${VERSION}"
rm -rf TEMPDIR

# Copy required files to TEMPDIR
mkdir ${TEMPDIR}
cp LICENSE ${TEMPDIR}
cp README.md ${TEMPDIR}
cp praw.ini ${TEMPDIR}
cp requirements.txt ${TEMPDIR}
cp lambda_function.py ${TEMPDIR}
cp -r datascience_bot/ ${TEMPDIR}/datascience_bot

# step into dir
pushd ${TEMPDIR}

# remove __pycache__ files
find . -name __pycache__ -exec rm -r {} \;

## Import requirements for AWS Lambda
## https://aws.amazon.com/premiumsupport/knowledge-center/build-python-lambda-deployment-package/
pip install -r requirements.txt -t ./
chmod -R 755 .
zip -r "../datascience-bot.zip" .

popd

rm -rf ${TEMPDIR}

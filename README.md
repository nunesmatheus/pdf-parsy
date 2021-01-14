# PDF Parsy

Extract text and images from PDFs through and endpoint that runs as a lambda function built with the [serverless framework](https://www.serverless.com/)

## Invoke local

``` bash
docker-compose build
docker-compose run --rm app pip install -r requirements_dev.txt
docker-compose run --rm -e S3_SAMPLE_OBJECT_KEY=my_s3_bucket -e S3_SAMPLE_IMAGES_FOLDER=my_s3_folder app python initial_setup.py
docker-compose run --rm -e S3_BUCKET=my_bucket -e S3_ACCESS_KEY_ID=my_access_key_id -e S3_SECRET_ACCESS_KEY=my_aws_secret_access_key app sls invoke local -f pdf_to_text -p fixtures/pdf_input.json
```

AWS credentials should have permissions to:
- Read from the provided S3 bucket that stores the PDF to be analyzed
- Write the extracted images from the PDF on the provided folder

- Run the function:

``` bash
docker-compose run --rm app sls invoke local -f pdf_to_text -p fixtures/pdf_input.json
```

## Deploy

- Configure an AWS account locally with [AWS CLI](https://aws.amazon.com/cli), then run:

``` bash
sls deploy --verbose
```

- Set the following env vars on the AWS page for your newly created lamba function:
- **S3_BUCKET**
- **AWS_ACCESS_KEY_ID**
- **AWS_SECRET_ACCESS_KEY**

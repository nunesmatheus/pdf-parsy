# PDF Parsy

Extract text and images from PDFs through and endpoint that runs as a lambda function built with the [serverless framework](https://www.serverless.com/)

## Invoke local

- Set a environment var for S3_BUCKET locally:

``` bash
export S3_BUCKET=YOUR_BUCKET_NAME
```

- Run the function:

``` bash
sls invoke local -f pdf_to_text -p fixtures/pdf_input.json
```

## Deploy

- Configure an AWS account locally with [AWS CLI](https://aws.amazon.com/cli), then run:

``` bash
sls deploy --verbose
```

- Set a S3_BUCKET environment var on the AWS page for your newly created lamba function

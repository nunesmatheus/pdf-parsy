# PDF Parsy

Extract text and images from PDFs through and endpoint that runs as a lambda function built with the [serverless framework](https://www.serverless.com/)

## Invoke local

``` bash
sls invoke local -f pdftotext -p fixtures/pdf_input.json
```

## Deploy

- Configure an AWS account locally with [AWS CLI](https://aws.amazon.com/cli), then run:

``` bash
sls deploy --verbose
```

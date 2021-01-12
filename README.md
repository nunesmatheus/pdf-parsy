# PDF Parsy

Get text from PDFs with this lambda function built with the [serverless framework](https://www.serverless.com/)

## Invoke local

``` bash
sls invoke local -f pdftotext -p pdf_input.json
```

## Deploy

- Configure an AWS account locally with [AWS CLI](https://aws.amazon.com/cli), then run:

``` bash
sls deploy --verbose
```

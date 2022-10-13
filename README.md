# Subtitle Extractor 

## Tech Stack
- Django (web app)
- Pysrt (subtitle handling)
- Celery (background tasks)
- redis (celery server)
- AWS DynamoDB (database)
- AWS S3 (storage)

## Features
- Extracts subtitle from video
- Upload subtitles to AWS DynamoDB
- Uploads Video to AWS S3 bucket
- Search for subtitle inside video
- Stores User search query in dynamoDB
- Uses celery for asynchronous tasks like subtitle extracting

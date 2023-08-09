from gcs.gcs import GCSDownloader
from dotenv import load_dotenv
import os
import logging
import sys
from scraper.scraper import clean_content, valid_article, article_to_content
import argparse
import dataclasses

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

load_dotenv()


def main():
    project = os.getenv('GCLOUD_PROJECT')
    bucket_name = os.getenv('GCS_BUCKET')

    parser = argparse.ArgumentParser(description='newspaper checker')
    parser.add_argument('--obj', type=str,
                        help='gcs object id', required=True)
    parser.add_argument('--file', type=str,
                        help='file with list of objects (not implemented)')

    args = parser.parse_args()

    object_name = args.obj  # "003503d1-e865-59d3-8607-9f99528d1740.html"

    downloader = GCSDownloader(gcp_project=project)
    res = downloader.download(bucket_name, object_name)
    if res is None:
        log.error("resource not found: %s/%s", bucket_name, object_name)
        return

    article = clean_content(res)
    if article is None:
        log.error("resource not cleaned: %s/%s", bucket_name, object_name)

    content = article_to_content(article)
    print(dataclasses.asdict(content))

    log.info("success: %s/%s", bucket_name, object_name)


if __name__ == "__main__":
    main()


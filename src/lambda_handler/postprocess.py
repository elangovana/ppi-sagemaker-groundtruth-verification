import datetime
import json
import logging
import math
from urllib.parse import urlparse

import boto3

import common


def lambda_handler(event, context):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.debug("{}".format(event))

    result = PostProcessPPIAnnotation().process(event)

    return result


class PostProcessPPIAnnotation:

    def __init__(self):
        self.s3_client = None

    @property
    def logger(self):
        return logging.getLogger(__name__)

    @property
    def s3_client(self):
        self.__s3_client__ = self.__s3_client__ or boto3.resource('s3')
        return self.__s3_client__

    @s3_client.setter
    def s3_client(self, value):
        self.__s3_client__ = value

    def process(self, event):

        payload_uri = event["payload"]["s3Uri"]
        label_attribute_name = event["labelAttributeName"]
        labeling_job_arn = event["labelingJobArn"]
        bucket_name = urlparse(payload_uri).netloc
        key = urlparse(payload_uri).path.strip("/")

        payload_object = self.s3_client.Object(bucket_name, key)
        payload = payload_object.get()["Body"].read().decode('utf-8')
        self.logger.debug("{}".format(payload))

        result = []
        for r in json.loads(payload):
            labels_dict = self._create_label_lookup(common.labels)

            annotations_hit = {}
            valid_annotation = None
            confidence_score = 0

            # Consolidate annotaions for the same record from various workers..
            # Annotations for various workers for the same record.. Pick the majority ones
            num_workers = len(r["annotations"])
            # threshold atleast 10% of the workers should have identified this
            threshold = math.ceil(num_workers * 10 / 100)

            for a in r["annotations"]:
                classification_annotations = json.loads(a["annotationData"]["content"])

                label = classification_annotations["category"]["label"]

                if label not in annotations_hit: annotations_hit[label] = 0

                annotations_hit[label] += 1
                # TODO Fix confidence score..
                if annotations_hit[label] == threshold:
                    valid_annotation = label
                    confidence_score = 0.0

            result.append({
                "datasetObjectId": r["datasetObjectId"],
                "consolidatedAnnotation": {
                    "content": {
                        label_attribute_name: {"label": labels_dict[valid_annotation]},
                        label_attribute_name + "-metadata": {"class-name": valid_annotation,
                                                             "job-name": labeling_job_arn,
                                                             "confidence": confidence_score,
                                                             "type": "groundtruth/text-classification",
                                                             "human-annotated": "yes",
                                                             "creation-date": datetime.datetime.today().isoformat()},
                    }
                }
            })
        return result

    def _create_label_lookup(self, labels_in_order):
        result = {}
        for i, l in enumerate(labels_in_order):
            result[l] = i
        return result

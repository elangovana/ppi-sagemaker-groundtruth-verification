import json
import logging
from urllib.parse import urlparse

import boto3


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

            labels_vote_dict = {}

            for a in r["annotations"]:
                classification_annotations = json.loads(a["annotationData"]["content"])

                label = classification_annotations["category"]["label"]

                if label not in labels_vote_dict: labels_vote_dict[label] = 0

                labels_vote_dict[label] += 1

            majority_label = self._get_majority_label(labels_vote_dict)

            result.append({
                "datasetObjectId": r["datasetObjectId"],
                "consolidatedAnnotation": {
                    "content": {
                        label_attribute_name: {"result": majority_label
                                               }
                    }
                }
            })
        return result

    def _get_majority_label(self, labels_vote_dict):
        """
        Return the label with max votes
        :param labels_vote_dict:
        :return:
        """
        labels, votes = [], []
        for l, v in labels_vote_dict.items():
            labels.append(l)
            votes.append(v)
        index_max_votes = votes.index(max(votes))
        majority_label = labels[index_max_votes]
        return majority_label

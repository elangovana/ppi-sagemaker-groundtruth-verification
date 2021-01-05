import json
from io import BytesIO
from unittest import TestCase
from unittest.mock import Mock

from postprocess import PostProcessPPIAnnotation


class TestPostProcessNERAnnotation(TestCase):

    def test_post_process(self):
        # Arrange
        sut = PostProcessPPIAnnotation()

        event = {
            'version': '2018-10-06',
            'labelingJobArn': 'arn:aws:sagemaker:us-east-2:111:labeling-job/ppi-clone-2-phosphorylation-clone',
            'payload': {
                's3Uri': 's3://bucket-data/pubmed_asbtract_groundtruth/predictions_multi_ppi-bert-2021-01-02-08_m_2021010212_summary/ppi-clone-2-phosphorylation-clone/annotations/consolidated-annotation/consolidation-request/iteration-1/2021-01-05_01:36:23.json'
            },
            'labelAttributeName': 'ppi-clone-2-phosphorylation-clone',
            'roleArn': 'arn:aws:iam::111:role/service-role/AmazonSageMaker-ExecutionRole-20210104T161547',
            'outputConfig': 's3://bucket-data/pubmed_asbtract_groundtruth/predictions_multi_ppi-bert-2021-01-02-08_m_2021010212_summary/ppi-clone-2-phosphorylation-clone/annotations',
            'maxHumanWorkersPerDataObject': 1
        }
        payload = [
            {
                "datasetObjectId": "7",
                "dataObject":
                    {
                        "content": "{\"abstract\": \"Mitogen-activated protein kinase-activated protein kinase 2 (MK2) is an important intracellular mediator of stress signals. In this report, a novel target of MK2 has been identified, the ETS transcription factor family member ER81, whose dysregulation contributes to tumorigenesis and whose normal function is required during development. MK2 phosphorylates ER81 in vitro within its central inhibitory domain, and overexpression of MK2 leads to increased in vivo phosphorylation of ER81. Two serine residues, ER81 amino acids 191 and 216, were identified as MK2 phosphorylation sites. MK2 suppresses basal ER81-dependent transcription, and this suppressive effect is alleviated upon mutation of the MK2 phosphorylation sites in a cell type-specific manner. However, MK2 can also interfere with ER81-mediated transcription independently of serine 191 and serine 216 phosphorylation. Furthermore, MK2 overexpression counteracts the stimulation of ER81 activity by p38 mitogen-activated protein kinase. Altogether, MK2 may regulate ER81 transcriptional activity in a cell type-specific manner and thereby modulate various physiological processes beyond stress responses.\", \"annotations\": [{\"start\": \"0\", \"end\": \"59\", \"name\": \"Mitogen-activated protein kinase-activated protein kinase 2\", \"normalised_id\": \"9261\", \"type\": \"Gene\"}, {\"start\": \"61\", \"end\": \"64\", \"name\": \"MK2\", \"normalised_id\": \"9261\", \"type\": \"Gene\"}, {\"start\": \"158\", \"end\": \"161\", \"name\": \"MK2\", \"normalised_id\": \"9261\", \"type\": \"Gene\"}, {\"start\": \"226\", \"end\": \"230\", \"name\": \"ER81\", \"normalised_id\": \"2115\", \"type\": \"Gene\"}, {\"start\": \"339\", \"end\": \"342\", \"name\": \"MK2\", \"normalised_id\": \"9261\", \"type\": \"Gene\"}, {\"start\": \"358\", \"end\": \"362\", \"name\": \"ER81\", \"normalised_id\": \"2115\", \"type\": \"Gene\"}, {\"start\": \"432\", \"end\": \"435\", \"name\": \"MK2\", \"normalised_id\": \"9261\", \"type\": \"Gene\"}, {\"start\": \"482\", \"end\": \"486\", \"name\": \"ER81\", \"normalised_id\": \"2115\", \"type\": \"Gene\"}, {\"start\": \"509\", \"end\": \"513\", \"name\": \"ER81\", \"normalised_id\": \"2115\", \"type\": \"Gene\"}, {\"start\": \"558\", \"end\": \"561\", \"name\": \"MK2\", \"normalised_id\": \"9261\", \"type\": \"Gene\"}, {\"start\": \"585\", \"end\": \"588\", \"name\": \"MK2\", \"normalised_id\": \"9261\", \"type\": \"Gene\"}, {\"start\": \"606\", \"end\": \"610\", \"name\": \"ER81\", \"normalised_id\": \"2115\", \"type\": \"Gene\"}, {\"start\": \"699\", \"end\": \"702\", \"name\": \"MK2\", \"normalised_id\": \"9261\", \"type\": \"Gene\"}, {\"start\": \"766\", \"end\": \"769\", \"name\": \"MK2\", \"normalised_id\": \"9261\", \"type\": \"Gene\"}, {\"start\": \"794\", \"end\": \"798\", \"name\": \"ER81\", \"normalised_id\": \"2115\", \"type\": \"Gene\"}, {\"start\": \"895\", \"end\": \"898\", \"name\": \"MK2\", \"normalised_id\": \"9261\", \"type\": \"Gene\"}, {\"start\": \"945\", \"end\": \"949\", \"name\": \"ER81\", \"normalised_id\": \"2115\", \"type\": \"Gene\"}, {\"start\": \"1012\", \"end\": \"1015\", \"name\": \"MK2\", \"normalised_id\": \"9261\", \"type\": \"Gene\"}, {\"start\": \"1029\", \"end\": \"1033\", \"name\": \"ER81\", \"normalised_id\": \"2115\", \"type\": \"Gene\"}], \"gene_id_map\": {\"2115\": \"P50549\", \"9261\": \"P49137\"}, \"normalised_abstract\": \"P49137 (P49137) is an important intracellular mediator of stress signals. In this report, a novel target of P49137 has been identified, the ETS transcription factor family member P50549, whose dysregulation contributes to tumorigenesis and whose normal function is required during development. P49137 phosphorylates P50549 in vitro within its central inhibitory domain, and overexpression of P49137 leads to increased in vivo phosphorylation of P50549. Two serine residues, P50549 amino acids 191 and 216, were identified as P49137 phosphorylation sites. P49137 suppresses basal P50549-dependent transcription, and this suppressive effect is alleviated upon mutation of the P49137 phosphorylation sites in a cell type-specific manner. However, P49137 can also interfere with P50549-mediated transcription independently of serine 191 and serine 216 phosphorylation. Furthermore, P49137 overexpression counteracts the stimulation of P50549 activity by p38 mitogen-activated protein kinase. Altogether, P49137 may regulate P50549 transcriptional activity in a cell type-specific manner and thereby modulate various physiological processes beyond stress responses.\", \"participant1Id\": \"P49137\", \"participant2Id\": \"P50549\", \"pubmedId\": 11551945, \"predicted\": \"phosphorylation\", \"confidence_scores\": {\"acetylation\": 0.0009346937, \"demethylation\": 0.0007648038, \"dephosphorylation\": 0.0015891847, \"deubiquitination\": 0.0011488960000000002, \"methylation\": 0.0007394949, \"other\": 0.1217244928, \"phosphorylation\": 0.8720072359000001, \"ubiquitination\": 0.0010911978}, \"acetylation\": 0.0009346937, \"demethylation\": 0.0007648038, \"dephosphorylation\": 0.0015891847, \"deubiquitination\": 0.0011488960000000002, \"methylation\": 0.0007394949, \"other\": 0.1217244928, \"phosphorylation\": 0.8720072359000001, \"ubiquitination\": 0.0010911978, \"predicted_confidence\": 0.8720072359000001, \"PubmedInTrainingData\": false}"
                    },
                "annotations": [
                    {
                        "workerId": "private.us-east-2.1b499e35c94f835e",
                        "annotationData": {
                            "content": "{\"category\":{\"label\":\"Correct\"}}"
                        }
                    }
                ]
            },
            {
                "datasetObjectId": "5",
                "dataObject": {
                    "content": "{\"abstract\": \"PP2A(Cdc55) is a highly conserved serine-threonine protein phosphatase that is involved in diverse cellular processes. In budding yeast, meiotic cells lacking PP2A(Cdc55) activity undergo a premature exit from meiosis I which results in a failure to form bipolar spindles and divide nuclei. This defect is largely due to its role in negatively regulating the Cdc Fourteen Early Anaphase Release (FEAR) pathway. PP2A(Cdc55) prevents nucleolar release of the Cdk (Cyclin-dependent kinase)-antagonising phosphatase Cdc14 by counteracting phosphorylation of the nucleolar protein Net1 by Cdk. CDC55 was identified in a genetic screen for monopolins performed by isolating suppressors of spo11 spo12 lethality suggesting that Cdc55 might have a role in meiotic chromosome segregation. We investigated this possibility by isolating cdc55 alleles that suppress spo11 spo12 lethality and show that this suppression is independent of PP2A(Cdc55)\u0027s FEAR function. Although the suppressor mutations in cdc55 affect reductional chromosome segregation in the absence of recombination, they have no effect on chromosome segregation during wild type meiosis. We suggest that Cdc55 is required for reductional chromosome segregation during achiasmate meiosis and this is independent of its FEAR function.\", \"annotations\": [{\"type\": \"Gene\", \"name\": \"PP2A\", \"start\": \"0\", \"end\": \"4\", \"normalised_id\": \"5524\"}, {\"type\": \"Species\", \"name\": \"yeast\", \"start\": \"130\", \"end\": \"135\", \"normalised_id\": \"4932\"}, {\"type\": \"Gene\", \"name\": \"PP2A\", \"start\": \"159\", \"end\": \"163\", \"normalised_id\": \"5524\"}, {\"type\": \"Gene\", \"name\": \"PP2A\", \"start\": \"411\", \"end\": \"415\", \"normalised_id\": \"5524\"}, {\"type\": \"Gene\", \"name\": \"Cdc14\", \"start\": \"512\", \"end\": \"517\", \"normalised_id\": \"8556\"}, {\"type\": \"Gene\", \"name\": \"Net1\", \"start\": \"576\", \"end\": \"580\", \"normalised_id\": \"10276\"}, {\"type\": \"Gene\", \"name\": \"spo11\", \"start\": \"683\", \"end\": \"688\", \"normalised_id\": \"23626\"}, {\"type\": \"Gene\", \"name\": \"spo11\", \"start\": \"683\", \"end\": \"688\", \"normalised_id\": \"7009056\"}, {\"type\": \"Gene\", \"name\": \"spo12\", \"start\": \"689\", \"end\": \"694\", \"normalised_id\": \"7008991\"}, {\"type\": \"Gene\", \"name\": \"spo11\", \"start\": \"854\", \"end\": \"859\", \"normalised_id\": \"23626\"}, {\"type\": \"Gene\", \"name\": \"spo11\", \"start\": \"854\", \"end\": \"859\", \"normalised_id\": \"7009056\"}, {\"type\": \"Gene\", \"name\": \"spo12\", \"start\": \"860\", \"end\": \"865\", \"normalised_id\": \"7008991\"}, {\"type\": \"Gene\", \"name\": \"PP2A\", \"start\": \"925\", \"end\": \"929\", \"normalised_id\": \"5524\"}], \"gene_id_map\": {\"5524\": \"Q15257\", \"10276\": \"Q7Z628\", \"8556\": \"Q9UNH5\", \"7008991\": \"7008991\", \"23626\": \"Q9Y5K1\", \"7009056\": \"7009056\"}, \"normalised_abstract\": \"Q15257(Cdc55) is a highly conserved serine-threonine protein phosphatase that is involved in diverse cellular processes. In budding yeast, meiotic cells lacking Q15257(Cdc55) activity undergo a premature exit from meiosis I which results in a failure to form bipolar spindles and divide nuclei. This defect is largely due to its role in negatively regulating the Cdc Fourteen Early Anaphase Release (FEAR) pathway. Q15257(Cdc55) prevents nucleolar release of the Cdk (Cyclin-dependent kinase)-antagonising phosphatase Q9UNH5 by counteracting phosphorylation of the nucleolar protein Q7Z628 by Cdk. CDC55 was identified in a genetic screen for monopolins performed by isolating suppressors of Q7009056 7008991 lethality suggesting that Cdc55 might have a role in meiotic chromosome segregation. We investigated this possibility by isolating cdc55 alleles that suppress Q7009056 7008991 lethality and show that this suppression is independent of Q15257(Cdc55)\u0027s FEAR function. Although the suppressor mutations in cdc55 affect reductional chromosome segregation in the absence of recombination, they have no effect on chromosome segregation during wild type meiosis. We suggest that Cdc55 is required for reductional chromosome segregation during achiasmate meiosis and this is independent of its FEAR function.\", \"participant1Id\": \"Q7Z628\", \"participant2Id\": \"Q9Y5K1\", \"pubmedId\": 27455870, \"predicted\": \"phosphorylation\", \"confidence_scores\": {\"acetylation\": 0.0131888911, \"demethylation\": 0.0012853862, \"dephosphorylation\": 0.1905595742, \"deubiquitination\": 0.0029850648000000002, \"methylation\": 0.0017364092, \"other\": 0.025877110300000002, \"phosphorylation\": 0.7603727451000001, \"ubiquitination\": 0.0039948221}, \"acetylation\": 0.0131888911, \"demethylation\": 0.0012853862, \"dephosphorylation\": 0.1905595742, \"deubiquitination\": 0.0029850648000000002, \"methylation\": 0.0017364092, \"other\": 0.025877110300000002, \"phosphorylation\": 0.7603727451000001, \"ubiquitination\": 0.0039948221, \"predicted_confidence\": 0.7603727451000001, \"PubmedInTrainingData\": false}"
                },
                "annotations": [
                    {
                        "workerId": "private.us-east-2.1b499e35c94f835e",
                        "annotationData": {
                            "content": "{\"category\":{\"label\":\"Incorrect - NER\"}}"
                        }
                    }
                ]
            }

        ]

        expected = [
            {
                'consolidatedAnnotation':
                    {
                        'content': {
                            'ppi-clone-2-phosphorylation-clone': "0"

                        }
                    },
                'datasetObjectId': '7'
            },
            {
                'consolidatedAnnotation':
                    {
                        'content':
                            {
                                'ppi-clone-2-phosphorylation-clone': "1"

                            }
                    },
                'datasetObjectId': '5'
            }
        ]
        mock_s3_client = Mock()
        mock_s3_Object = Mock()
        mock_s3_Object.get.return_value = {"Body": BytesIO(json.dumps(payload).encode("utf-8"))}
        mock_s3_client.Object.return_value = mock_s3_Object
        sut.s3_client = mock_s3_client

        # Act
        actual = sut.process(event)

        # Assert
        self.assertEqual(actual, expected)

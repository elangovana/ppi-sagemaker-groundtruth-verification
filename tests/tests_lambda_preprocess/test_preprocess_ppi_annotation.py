import json
from unittest import TestCase

from preprocess import PreProcessPPIAnnotation


class TestPreProcessPPIAnnotation(TestCase):

    def test_process_all_fields(self):
        # Arrange
        sample_json = {
            "abstract": "The proto-oncogene BCL6 encodes a BTB/POZ-zinc finger transcriptional repressor that is necessary for germinal-center formation and has been implicated in the pathogenesis of B-cell lymphomas. Here we show that the co-activator p300 binds and acetylates BCL6 in vivo and inhibits its function. Acetylation disrupts the ability of BCL6 to recruit histone deacetylases (HDACs), thereby hindering its capacity to repress transcription and to induce cell transformation. BCL6 is acetylated under physiologic conditions in normal germinal-center B cells and in germinal center-derived B-cell tumors. Treatment with specific inhibitors shows that levels of acetylation of BCL6 are controlled by both HDAC-dependent and SIR2-dependent pathways. Pharmacological inhibition of these pathways leads to the accumulation of the inactive acetylated BCL6 and to cell-cycle arrest and apoptosis in B-cell lymphoma cells. These results identify a new mechanism of regulation of the proto-oncogene BCL6 with potential for therapeutic exploitation. Furthermore, these findings provide a new mechanism by which acetylation can promote transcription not only by modifying histones and activating transcriptional activators, but also by inhibiting transcriptional repressors.",
            "annotations": [{"normalised_id": "604", "end": "23", "start": "19", "name": "BCL6", "type": "Gene"},
                            {"normalised_id": "2033", "end": "232", "start": "228", "name": "p300", "type": "Gene"},
                            {"normalised_id": "604", "end": "258", "start": "254", "name": "BCL6", "type": "Gene"},
                            {"normalised_id": "604", "end": "334", "start": "330", "name": "BCL6", "type": "Gene"},
                            {"normalised_id": "604", "end": "471", "start": "467", "name": "BCL6", "type": "Gene"},
                            {"normalised_id": "604", "end": "670", "start": "666", "name": "BCL6", "type": "Gene"},
                            {"normalised_id": "22933", "end": "717", "start": "713", "name": "SIR2", "type": "Gene"},
                            {"normalised_id": "604", "end": "840", "start": "836", "name": "BCL6", "type": "Gene"},
                            {"normalised_id": "604", "end": "985", "start": "981", "name": "BCL6", "type": "Gene"}],
            "gene_id_map": {"2033": "Q09472", "604": "P41182", "22933": "Q8IXJ6"},
            "normalised_abstract": "The proto-oncogene P41182 encodes a BTB/POZ-zinc finger transcriptional repressor that is necessary for germinal-center formation and has been implicated in the pathogenesis of B-cell lymphomas. Here we show that the co-activator Q09472 binds and acetylates P41182 in vivo and inhibits its function. Acetylation disrupts the ability of P41182 to recruit histone deacetylases (HDACs), thereby hindering its capacity to repress transcription and to induce cell transformation. P41182 is acetylated under physiologic conditions in normal germinal-center B cells and in germinal center-derived B-cell tumors. Treatment with specific inhibitors shows that levels of acetylation of P41182 are controlled by both HDAC-dependent and Q8IXJ6-dependent pathways. Pharmacological inhibition of these pathways leads to the accumulation of the inactive acetylated P41182 and to cell-cycle arrest and apoptosis in B-cell lymphoma cells. These results identify a new mechanism of regulation of the proto-oncogene P41182 with potential for therapeutic exploitation. Furthermore, these findings provide a new mechanism by which acetylation can promote transcription not only by modifying histones and activating transcriptional activators, but also by inhibiting transcriptional repressors.",
            "participant1Id": "P41182", "participant2Id": "Q09472", "pubmedId": 12402037, "predicted": "acetylation",
            "confidence_scores": {"acetylation": 0.9025735795000001, "demethylation": 0.0129228815,
                                  "dephosphorylation": 0.007053328100000001, "deubiquitination": 0.020006244000000003,
                                  "methylation": 0.014541742600000001, "other": 0.018704607300000002,
                                  "phosphorylation": 0.0038712035000000003, "ubiquitination": 0.0203264001},
            "acetylation": 0.9025735795000001, "demethylation": 0.0129228815, "dephosphorylation": 0.007053328100000001,
            "deubiquitination": 0.020006244000000003, "methylation": 0.014541742600000001,
            "other": 0.018704607300000002, "phosphorylation": 0.0038712035000000003, "ubiquitination": 0.0203264001,
            "predicted_confidence": 0.9025735795000001, "PubmedInTrainingData": False}
        expected = sample_json
        input_data = {"source": json.dumps(sample_json)}

        sut = PreProcessPPIAnnotation()

        # Act
        actual = sut.process(input_data)

        # Assert
        for k, v in expected.items():
            self.assertEqual(expected[k], actual[k])

    def test_process_display(self):
        # Arrange
        sample_json = {
            "annotations": [{"normalised_id": "2033", "end": "232", "start": "228", "name": "p300", "type": "Gene"},
                            {"normalised_id": "604", "end": "258", "start": "254", "name": "BCL6", "type": "Gene"},
                            ],
            "gene_id_map": {"2033": "Q09472", "604": "P41182"},
            "normalised_abstract": "co-activator Q09472 binds and acetylates P41182",
            "participant1Id": "P41182",
            "participant2Id": "Q09472"
        }
        expected_display_abstract = "co-activator <mark>p300 (Q09472)</mark> binds and acetylates <mark>BCL6 (P41182)</mark>"
        input_data = {"source": json.dumps(sample_json)}

        sut = PreProcessPPIAnnotation()

        # Act
        actual = sut.process(input_data)

        # Assert
        self.assertEqual(expected_display_abstract, actual["display_abstract"])

    def test_process_display_particpants(self):
        # Arrange
        sample_json = {
            "annotations": [{"normalised_id": "2033", "end": "232", "start": "228", "name": "p300", "type": "Gene"},
                            {"normalised_id": "604", "end": "258", "start": "254", "name": "BCL6", "type": "Gene"},
                            {"normalised_id": "22933", "end": "717", "start": "713", "name": "SIR2", "type": "Gene"}

                            ],
            "gene_id_map": {"2033": "Q09472", "604": "P41182", "22933": "Q8IXJ6"},
            "normalised_abstract": "Q09472 binds and acetylates P41182 Q8IXJ6-dependent pathways",
            "participant1Id": "P41182",
            "participant2Id": "Q09472"
        }
        expected_display_participants = sorted(["p300 (Q09472)", "BCL6 (P41182)"])
        input_data = {"source": json.dumps(sample_json)}

        sut = PreProcessPPIAnnotation()

        # Act
        actual = sut.process(input_data)

        # Assert
        self.assertEqual(expected_display_participants, sorted(actual["display_participants"]))

    def test_process_display_particpants_shortest_name(self):
        # Arrange
        sample_json = {
            "annotations": [
                {'start': '0', 'end': '59', 'name': 'Mitogen-activated protein kinase-activated protein kinase 2',
                 'normalised_id': '9261', 'type': 'Gene'},
                {'start': '61', 'end': '64', 'name': 'MK2', 'normalised_id': '9261', 'type': 'Gene'},
                {'start': '158', 'end': '161', 'name': 'MK2', 'normalised_id': '9261', 'type': 'Gene'},
                {'start': '226', 'end': '230', 'name': 'ER81', 'normalised_id': '2115', 'type': 'Gene'}
            ],
            "gene_id_map": {'2115': 'P50549', '9261': 'P49137'},
            "normalised_abstract": "P49137 (P49137) is an important intracellular mediator of stress signals",
            "participant1Id": "P50549",
            "participant2Id": "P49137"
        }
        expected_display_participants = sorted(["MK2 (P49137)", "ER81 (P50549)"])
        input_data = {"source": json.dumps(sample_json)}

        sut = PreProcessPPIAnnotation()

        # Act
        actual = sut.process(input_data)

        # Assert
        self.assertEqual(expected_display_participants, sorted(actual["display_participants"]))

    def test_process_display_segments(self):
        # Arrange
        sample_json = {
            "annotations": [{"normalised_id": "2033", "end": "232", "start": "228", "name": "p300", "type": "Gene"},
                            {"normalised_id": "604", "end": "258", "start": "254", "name": "BCL6", "type": "Gene"},
                            ],
            "gene_id_map": {"2033": "Q09472", "604": "P41182"},
            "normalised_abstract": "Q09472 binds and acetylates P41182",
            "participant1Id": "P41182",
            "participant2Id": "Q09472"
        }
        expected_display_segments = [{"text": "", "highlight": False},
                                     {"text": "p300 (Q09472)", "highlight": True},
                                     {"text": " binds and acetylates ", "highlight": False},
                                     {"text": "BCL6 (P41182)", "highlight": True},
                                     {"text": "", "highlight": False}
                                     ]

        sut = PreProcessPPIAnnotation()
        input_data = {"source": json.dumps(sample_json)}

        # Act
        actual = sut.process(input_data)

        # Assert
        self.assertEqual(expected_display_segments, actual["display_segments"])

    def test_process_display_segments_non_participant(self):
        # Arrange
        sample_json = {
            "annotations": [{"normalised_id": "2033", "end": "232", "start": "228", "name": "p300", "type": "Gene"},
                            {"normalised_id": "604", "end": "258", "start": "254", "name": "BCL6", "type": "Gene"},
                            {"normalised_id": "22933", "end": "717", "start": "713", "name": "SIR2", "type": "Gene"}

                            ],
            "gene_id_map": {"2033": "Q09472", "604": "P41182", "22933": "Q8IXJ6"},
            "normalised_abstract": "Q09472 binds and acetylates P41182 Q8IXJ6-dependent pathways",
            "participant1Id": "P41182",
            "participant2Id": "Q09472"
        }
        expected_display_segments = [{"text": "", "highlight": False},
                                     {"text": "p300 (Q09472)", "highlight": True},
                                     {"text": " binds and acetylates ", "highlight": False},
                                     {"text": "BCL6 (P41182)", "highlight": True},
                                     {"text": " SIR2 (Q8IXJ6)-dependent pathways", "highlight": False}
                                     ]
        input_data = {"source": json.dumps(sample_json)}

        sut = PreProcessPPIAnnotation()

        # Act
        actual = sut.process(input_data)

        # Assert
        self.assertEqual(expected_display_segments, actual["display_segments"])

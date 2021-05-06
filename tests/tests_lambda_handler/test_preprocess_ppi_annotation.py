import json
from unittest import TestCase

from preprocess import PreProcessPPIAnnotation


class TestPreProcessPPIAnnotation(TestCase):

    def test_process_all_fields(self):
        # Arrange
        sample_json = {
            "pubmedId": 17141222,
            "pubmedabstract": "Regulation of growth factor dependent cell survival is crucial for development and ",
            "annotations": [
                {
                    "start": "140",
                    "end": "143",
                    "name": "Src",
                    "type": "Gene",
                    "normalised_id": "6714"
                },
                {
                    "start": "1093",
                    "end": "1096",
                    "name": "Src",
                    "type": "Gene",
                    "normalised_id": "5156"
                }
            ],

            "normalised_abstract": "Regulation of growth factor dependent cell survival is crucial for development and ",
            "normalised_abstract_annotations": [
                {
                    "charOffset": 140,
                    "len": 6,
                    "text": "P22681"
                },
                {
                    "charOffset": 295,
                    "len": 6,
                    "text": "P12931"
                },

            ],
            "participant1Id": "P22681",
            "participant2Id": "P12931",
            "gene_to_uniprot_map": {
                "5156": [
                   "P22681"
                ],
                "6714": [
                    "P12931"
                ]
            },
            "class": "phosphorylation",
            "prediction": "other",
        }
        expected = sample_json
        input_data = {"source": json.dumps(sample_json)}

        sut = PreProcessPPIAnnotation()

        # Act
        actual = sut.process(input_data)

        # Assert
        for k, v in expected.items():
            self.assertEqual(expected[k], actual[k])

    def test_process_display_particpants(self):
        # Arrange
        sample_json = {
            "annotations": [{"normalised_id": "2033", "end": "232", "start": "228", "name": "p300", "type": "Gene"},
                            {"normalised_id": "604", "end": "258", "start": "254", "name": "BCL6", "type": "Gene"},
                            {"normalised_id": "22933", "end": "717", "start": "713", "name": "SIR2", "type": "Gene"}

                            ],
            "gene_to_uniprot_map": {"2033": "Q09472", "604": "P41182", "22933": "Q8IXJ6"},
            "normalised_abstract": "Q09472 binds and acetylates P41182 Q8IXJ6-dependent pathways",
            "normalised_abstract_annotations": [
                {
                    "charOffset": 0,
                    "len": 6,
                    "text": "Q09472"
                },
                {
                    "charOffset": 28,
                    "len": 6,
                    "text": "P41182"
                },
                {
                    "charOffset": 35,
                    "len": 6,
                    "text": "Q8IXJ6"
                },

            ],
            "participant1Id": "P41182",
            "participant2Id": "Q09472",
            "class": "phosphorylation"
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
            "gene_to_uniprot_map": {'2115': 'P50549', '9261': 'P49137'},
            "normalised_abstract": "P49137 (P50549) is an important intracellular mediator of stress signals",
            "participant1Id": "P50549",
            "participant2Id": "P49137",
            "class": "phosphorylation",
            "normalised_abstract_annotations": [
                {
                    "charOffset": 0,
                    "len": 6,
                    "text": "P49137"
                },
                {
                    "charOffset": 8,
                    "len": 6,
                    "text": "P50549"
                }
            ],

        }
        expected_display_participants = sorted(["MK2 (P49137)", "ER81 (P50549)"])
        input_data = {"source": json.dumps(sample_json)}

        sut = PreProcessPPIAnnotation()

        # Act
        actual = sut.process(input_data)

        # Assert
        self.assertEqual(expected_display_participants, sorted(actual["display_participants"]))

    def test_process_display_labels(self):
        # Arrange
        sample_json =  sample_json = {
            "annotations": [{"normalised_id": "2033", "end": "232", "start": "228", "name": "p300", "type": "Gene"},
                            {"normalised_id": "604", "end": "258", "start": "254", "name": "BCL6", "type": "Gene"},
                            {"normalised_id": "22933", "end": "717", "start": "713", "name": "SIR2", "type": "Gene"}

                            ],
            "gene_to_uniprot_map": {"2033": "Q09472", "604": "P41182", "22933": "Q8IXJ6"},
            "normalised_abstract": "Q09472 binds and acetylates P41182 Q8IXJ6-dependent pathways",
            "normalised_abstract_annotations": [
                {
                    "charOffset": 0,
                    "len": 6,
                    "text": "Q09472"
                },
                {
                    "charOffset": 28,
                    "len": 6,
                    "text": "P41182"
                },
                {
                    "charOffset": 35,
                    "len": 6,
                    "text": "Q8IXJ6"
                },

            ],
            "participant1Id": "P41182",
            "participant2Id": "Q09472",
            "class": "phosphorylation"
        }
        expected_display_labels = "['Correct', 'Incorrect - NER', 'Incorrect - DNA Methylation', 'Incorrect - No trigger word', 'Incorrect - Opposite type', 'Incorrect - Not related to PPI', 'Incorrect - relationship not described', 'Not - sure']"
        input_data = {"source": json.dumps(sample_json)}

        sut = PreProcessPPIAnnotation()

        # Act
        actual = sut.process(input_data)

        # Assert
        self.assertEqual(expected_display_labels, actual["display_labels"])

    def test_process_display_segments(self):
        # Arrange
        sample_json = {
            "annotations": [{"normalised_id": "2033", "end": "232", "start": "228", "name": "p300", "type": "Gene"},
                            {"normalised_id": "604", "end": "258", "start": "254", "name": "BCL6", "type": "Gene"},
                            ],
            "gene_to_uniprot_map": {"2033": [ "AAAAAA","Q09472" ], "604": "P41182"},
            "normalised_abstract": "Q09472 binds and acetylates P41182",
            "participant1Id": "P41182",
            "participant2Id": "Q09472",
            "class": "phosphorylation",
            "normalised_abstract_annotations": [
                {
                    "charOffset": 0,
                    "len": 6,
                    "text": "Q09472"
                },
                {
                    "charOffset": 28,
                    "len": 6,
                    "text": "P41182"
                }

            ]
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
            "gene_to_uniprot_map": {"2033": "Q09472", "604": "P41182", "22933": "Q8IXJ6"},
            "normalised_abstract": "Q09472 binds and acetylates P41182 Q8IXJ6-dependent pathways",
            "normalised_abstract_annotations": [
                {
                    "charOffset": 0,
                    "len": 6,
                    "text": "Q09472"
                },
                {
                    "charOffset": 28,
                    "len": 6,
                    "text": "P41182"
                },
                {
                    "charOffset": 35,
                    "len": 6,
                    "text": "Q8IXJ6"
                },

            ],
            "participant1Id": "P41182",
            "participant2Id": "Q09472",
            "class": "phosphorylation"
        }
        expected_display_segments = [{"text": "", "highlight": False},
                                     {"text": "p300 (Q09472)", "highlight": True},
                                     {"text": " binds and acetylates ", "highlight": False},
                                     {"text": "BCL6 (P41182)", "highlight": True},
                                     {'highlight': False, 'text': ' '},
                                     {'highlight': False, 'text': 'SIR2 (Q8IXJ6)'},
                                     {'highlight': False, 'text': '-dependent pathways'}
                                     ]
        input_data = {"source": json.dumps(sample_json)}

        sut = PreProcessPPIAnnotation()

        # Act
        actual = sut.process(input_data)

        # Assert
        self.assertEqual(expected_display_segments, actual["display_segments"])

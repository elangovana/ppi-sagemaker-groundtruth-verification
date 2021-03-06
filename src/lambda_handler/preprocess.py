import json
import logging
import re


def lambda_handler(event, context):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.debug("{}".format(event))

    data = PreProcessPPIAnnotation().process(event['dataObject'])

    result = {
        "taskInput": data,
        "humanAnnotationRequired": True
    }
    logger.debug("{}".format(result))
    return result


class PreProcessPPIAnnotation:

    def __init__(self):
        self.labels = ['Correct', 'Incorrect - NER', 'Incorrect - DNA Methylation',
                       'Incorrect - No trigger word', 'Incorrect - Opposite type',
                       'Incorrect - Not related to PPI', "Incorrect - relationship not described", 'Not - sure']

    def process(self, json_input):
        source_input_dict = json.loads(json_input["source"])

        # if training data then has no prediction label
        label = source_input_dict["prediction"] if "prediction" in source_input_dict else source_input_dict[
            "class"]

        source_input_dict["ppi_relationship_type"] = label

        norm_abstract = source_input_dict["normalised_abstract"]
        particpant_uniprots = [source_input_dict["participant1Id"], source_input_dict["participant2Id"]]

        gene_to_uniprot_map = {}
        normalised_abstract_annotations = source_input_dict["normalised_abstract_annotations"]
        normalised_abstract_uniprots = {a["text"] for a in normalised_abstract_annotations}
        for n, u_list in source_input_dict["gene_to_uniprot_map"].items():
            if len(u_list) == 0: continue

            # If uniprot is a list, just use the first one
            u = u_list
            if not isinstance(u_list, str):
                u = list(filter(lambda x: x in normalised_abstract_uniprots, u_list))[0]

            gene_to_uniprot_map[n] = u

        display_segments = []
        last_pos = 0
        for norm_anno in normalised_abstract_annotations:
            uniprot_id = norm_anno["text"]
            pos = norm_anno["charOffset"]
            text_len = norm_anno["len"]
            highlight = uniprot_id in particpant_uniprots

            friendly_name = self.get_display_friendly_gene_name(uniprot_id, source_input_dict["annotations"],
                                                                gene_to_uniprot_map)

            display_segments.append({"text": norm_abstract[last_pos: pos], "highlight": False})
            display_segments.append({"text": friendly_name, "highlight": highlight})

            last_pos = pos + text_len

        display_segments.append({"text": norm_abstract[last_pos:], "highlight": False})

        source_input_dict["display_participants"] = [
            self.get_display_friendly_gene_name(p, source_input_dict["annotations"],
                                                gene_to_uniprot_map) for p in particpant_uniprots
        ]

        source_input_dict["display_segments"] = display_segments

        # [{"text": i, "highlight": any(map(i.__contains__, particpant_uniprots))}
        #                                          for i in re.split("<mark>|</mark>", display_abstract)]

        source_input_dict["labels"] = self.labels

        comma_sep_labels_str = ", ".join(["'{}'".format(l) for l in source_input_dict["labels"]])
        source_input_dict["display_labels"] = "[{}]".format(comma_sep_labels_str)

        return source_input_dict

    def get_display_friendly_gene_name(self, uniprot_id, annotations, gene_uniprot_map):
        display_friendly_nomalised_name = uniprot_id

        ncbi = list(filter(lambda kv: kv[1] == uniprot_id, gene_uniprot_map.items()))

        if len(ncbi) == 0:
            return display_friendly_nomalised_name

        ncbi, _ = ncbi[0]
        # Make sure we select the shortest name.
        gene_name = list(sorted(filter(lambda a: a["type"] == 'Gene' and a["normalised_id"] == ncbi,
                                       annotations), key=lambda a: len(a["name"])))[0]["name"]

        display_friendly_nomalised_name = "{} ({})".format(gene_name, uniprot_id)
        return display_friendly_nomalised_name

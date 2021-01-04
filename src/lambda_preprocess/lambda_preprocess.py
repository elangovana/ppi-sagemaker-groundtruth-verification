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

    def process(self, json_input):
        source_input_dict = json_input["source"]

        norm_abstract = source_input_dict["normalised_abstract"]
        particpant_uniprots = [source_input_dict["participant1Id"], source_input_dict["participant2Id"]]
        display_abstract = norm_abstract

        display_participants = []
        for n, u in source_input_dict["gene_id_map"].items():
            friendly_name = self.get_display_friendly_gene_name(u, source_input_dict, particpant_uniprots)
            display_abstract = display_abstract.replace(u, friendly_name)
            if u in particpant_uniprots:
                display_participants.append("{}".format(re.sub("<mark>|</mark>", "", friendly_name)))

        source_input_dict["display_abstract"] = display_abstract
        source_input_dict["display_participants"] = display_participants

        source_input_dict["display_segments"] = [{"text": i, "highlight": any(map(i.__contains__, particpant_uniprots))}
                                                 for i in re.split("<mark>|</mark>", display_abstract)]

        return source_input_dict

    def get_display_friendly_gene_name(self, uniprot_id, source_input_dict, particpant_uniprots):
        ncbi, _ = list(filter(lambda kv: kv[1] == uniprot_id, source_input_dict["gene_id_map"].items()))[0]
        gene_name = list(filter(lambda a: a["type"] == 'Gene' and a["normalised_id"] == ncbi,
                                source_input_dict["annotations"]))[0]["name"]

        if uniprot_id in particpant_uniprots:
            display_friendly_nomalised_name = "<mark>{} ({})</mark>".format(gene_name,
                                                                            uniprot_id)

        else:
            display_friendly_nomalised_name = "{} ({})".format(gene_name, uniprot_id)
        return display_friendly_nomalised_name

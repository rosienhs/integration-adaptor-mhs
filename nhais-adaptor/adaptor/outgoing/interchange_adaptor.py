from adaptor.outgoing.message_adaptor import MessageAdaptor
from adaptor.outgoing.fhir_helpers.operation_definition import OperationDefinitionHelper as odh
from edifact.models.interchange import Interchange
from edifact.models.message import Messages
from adaptor.outgoing.fhir_helpers.constants import ParameterName


class InterchangeAdaptor:
    """
    An adaptor to take in fhir models and generate an edifact interchange
    """

    @staticmethod
    def create_interchange(fhir_operation):
        """
        Create the edifact interchange from the fhir operation definition
        :param fhir_operation:
        :return: Interchange
        """
        interchange_sequence_number = odh.get_parameter_value(fhir_operation,
                                                              parameter_name=ParameterName.INTERCHANGE_SEQ_NO)
        sender_cypher = odh.get_parameter_value(fhir_operation, parameter_name=ParameterName.SENDER_CYPHER)
        nhais_cypher = odh.get_parameter_value(fhir_operation, parameter_name=ParameterName.NHAIS_CYPHER)
        recipient = ''
        if len(nhais_cypher) == 3:
            recipient = nhais_cypher + '1'
        elif len(nhais_cypher) == 2:
            recipient = nhais_cypher + "01"

        messages = Messages(messages=[MessageAdaptor.create_message(fhir_operation)])

        interchange = Interchange(sender=sender_cypher, recipient=recipient,
                                  sequence_number=interchange_sequence_number,
                                  date_time=fhir_operation.date.as_json(), messages=messages).to_edifact()
        return interchange

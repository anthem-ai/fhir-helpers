import logging
from typing import Union

from fhir_types import FHIR_Bundle
from proto.google.fhir.proto.r4.core.resources.bundle_and_contained_resource_pb2 import (  # noqa: E501
    Bundle,
)

from .allergy_intolerance import (
    AllergyIntoleranceDict,
    AllergyIntoleranceProto,
    AllergyIntolerances,
)
from .condition import ConditionDict, ConditionProto, Conditions
from .encounter import EncounterDict, EncounterProto, Encounters
from .immunization import ImmunizationDict, ImmunizationProto, Immunizations
from .medication_dispense import (
    MedicationDispenseDict,
    MedicationDispenseProto,
    MedicationDispenses,
)
from .medication_request import (
    MedicationRequestDict,
    MedicationRequestProto,
    MedicationRequests,
)
from .observation import ObservationDict, ObservationProto, Observations
from .patient import Patient, PatientDict, PatientProto
from .practitioner import PractitionerDict, PractitionerProto, Practitioners
from .procedure import ProcedureDict, ProcedureProto, Procedures

log = logging.getLogger(__name__)


class LPR:
    def __init__(self, lpr: Union[FHIR_Bundle, Bundle]) -> None:
        self.lpr = lpr

        self.patient: Patient
        self.encounters = Encounters()
        self.observations = Observations()
        self.medication_dispenses = MedicationDispenses()
        self.medication_requests = MedicationRequests()
        self.procedures = Procedures()
        self.conditions = Conditions()
        self.practitioners = Practitioners()
        self.immunizations = Immunizations()
        self.practitioners = Practitioners()
        self.allergy_intolerances = AllergyIntolerances()

        if isinstance(lpr, Bundle):
            self._parse_lpr_proto(lpr)
        else:
            self._parse_lpr_dict(lpr)

    def _parse_lpr_dict(self, lpr: FHIR_Bundle) -> None:
        for entry in lpr["entry"]:
            resource_type = entry["resource"]["resourceType"]

            if resource_type == "Patient":
                self.patient = PatientDict(entry["resource"])
            elif resource_type == "Immunization":
                self.immunizations.add(ImmunizationDict(entry["resource"]))
            elif resource_type == "Observation":
                self.observations.add(ObservationDict(entry["resource"]))
            elif resource_type == "MedicationDispense":
                self.medication_dispenses.add(MedicationDispenseDict(entry["resource"]))
            elif resource_type == "MedicationRequest":
                self.medication_requests.add(
                    MedicationRequestDict(entry["resource"], self)
                )
            elif resource_type == "Procedure":
                self.procedures.add(ProcedureDict(entry["resource"]))
            elif resource_type == "Condition":
                self.conditions.add(ConditionDict(entry["resource"]))
            elif resource_type == "Practitioner":
                self.practitioners.add(PractitionerDict(entry["resource"]))
            elif resource_type == "AllergyIntolerance":
                self.allergy_intolerances.add(AllergyIntoleranceDict(entry["resource"]))
            elif resource_type == "Encounter":
                self.encounters.add(EncounterDict(entry["resource"]))
            else:
                log.debug(f"Unmapped JSON resource type: {resource_type}")

    def _parse_lpr_proto(self, lpr: Bundle) -> None:
        for entry in lpr.entry:
            if entry.resource.HasField("patient"):
                self.patient = PatientProto(entry.resource.patient)
            elif entry.resource.HasField("observation"):
                self.observations.add(ObservationProto(entry.resource.observation))
            elif entry.resource.HasField("condition"):
                self.conditions.add(ConditionProto(entry.resource.condition))
            elif entry.resource.HasField("procedure"):
                self.procedures.add(ProcedureProto(entry.resource.procedure))
            elif entry.resource.HasField("medication_dispense"):
                self.medication_dispenses.add(
                    MedicationDispenseProto(entry.resource.medication_dispense)
                )
            elif entry.resource.HasField("medication_request"):
                self.medication_requests.add(
                    MedicationRequestProto(entry.resource.medication_request, self)
                )
            elif entry.resource.HasField("immunization"):
                self.immunizations.add(ImmunizationProto(entry.resource.immunization))
            elif entry.resource.HasField("practitioner"):
                self.practitioners.add(PractitionerProto(entry.resource.practitioner))
            elif entry.resource.HasField("allergy_intolerance"):
                self.allergy_intolerances.add(
                    AllergyIntoleranceProto(entry.resource.allergy_intolerance)
                )
            elif entry.resource.HasField("encounter"):
                self.encounters.add(EncounterProto(entry.resource.encounter))
            else:
                log.debug("Unmapped protobuf resource type")

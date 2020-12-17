from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from fhir_types import (
    FHIR_Bundle_Entry,
    FHIR_CodeableConcept,
    FHIR_Coding,
    FHIR_Narrative,
    FHIR_RiskAssessment,
    FHIR_RiskAssessment_Prediction,
)

from .codeable_concept import CodeableConcept


class InvalidArgumentError(Exception):
    """Invalid argument(s) used. Bad argument, etc. Don't retry."""

    pass


def _get_uuid() -> str:
    return uuid4().hex


@dataclass
class RiskAssessment:
    """
    Potential outcomes for a subject with likelihood. See `FHIR RiskAssessment
    <https://hl7.org/fhir/riskassessment.html>`_ for more detail
    """

    class Likelihood(Enum):
        """
        Likelihood of specified outcome as a qualitative value.  See `FHIR Risk
        Probability <https://hl7.org/fhir/valueset-risk-probability.html>`_ for
        more detail
        """

        #: **Negligible likelihood**.
        #: The specified outcome is exceptionally unlikely.
        NEGLIGIBLE = "negligible"

        #: **Low likelihood**.
        #: The specified outcome is possible but unlikely
        LOW = "low"

        #: **Moderate likelihood**.
        #: The specified outcome has a reasonable likelihood of occurrence.
        MODERATE = "moderate"

        #: **High likelihood**.
        #: The specified outcome is more likely to occur than not.
        HIGH = "high"

        #: **Certain**.
        #: The specified outcome is effectively guaranteed.
        CERTAIN = "certain"

    patient_id: str  #: ID of the patient or group the risk assessment applies to
    outcome: CodeableConcept  #: Possible outcome for the subject
    likelihood: Likelihood  #: Likelihood of specified outcome as a qualitative value

    #: Likelihood of specified outcome as a percentage
    probability: Optional[float] = None

    date: Optional[str] = None  #: When was assessment made?

    #: ID of the risk assessment. Defaults to a random UUID
    uuid: str = field(default_factory=_get_uuid)

    def __post_init__(self) -> None:
        if not self.patient_id:
            raise InvalidArgumentError("Patient ID is required")

        if not self.outcome or not isinstance(self.outcome, CodeableConcept):
            raise InvalidArgumentError("RiskAssessment requires an outcome")

        if not self.likelihood or not isinstance(
            self.likelihood, RiskAssessment.Likelihood
        ):
            raise InvalidArgumentError("RiskAssessment requires a Likelihood")

    def get_entries(self) -> List[FHIR_Bundle_Entry]:
        resource: FHIR_RiskAssessment = {
            "resourceType": "RiskAssessment",
            "id": "diabetes",
            "text": self._get_text(),
            "identifier": [{"use": "temp", "value": self.uuid}],
            "status": "preliminary",
            "code": self._get_outcome_code(),
            "subject": {"reference": f"Patient/{self.patient_id}"},
            "prediction": self._get_prediction(),
        }

        if self.date is not None:
            resource["occurrenceDateTime"] = self.date

        return [
            {
                "fullUrl": f"urn:uuid:{self.uuid}",
                "resource": resource,
            }
        ]

    def _get_outcome_code(self) -> FHIR_CodeableConcept:
        codings: List[FHIR_Coding] = []
        for code in self.outcome.codings:
            codings.append(
                {"system": code.system, "code": code.code, "display": code.display}
            )
        outcome: FHIR_CodeableConcept = {
            "text": self.outcome.text,
        }
        if len(codings) > 0:
            outcome["coding"] = codings
        return outcome

    def _get_likelihood_display(self) -> str:
        return {
            RiskAssessment.Likelihood.CERTAIN: "Certain",
            RiskAssessment.Likelihood.HIGH: "High likelihood",
            RiskAssessment.Likelihood.MODERATE: "Moderate likelihood",
            RiskAssessment.Likelihood.LOW: "Low likelihood",
            RiskAssessment.Likelihood.NEGLIGIBLE: "Negligible likelihood",
        }.get(self.likelihood, "")

    def _get_text(self) -> FHIR_Narrative:
        risk_score_row = ""

        if self.probability:
            risk_score_row = f"""
            <tr>
                <th>Risk score</th>
                <td>{round(self.probability, 17)}</td>
            </tr>
            """.strip()

        text_value = f"""
        <div xmlns="http://www.w3.org/1999/xhtml">
            <table>
            <tr>
                <td colspan="2">
                <h1>{self.outcome.text}</h1>
                <h2>Risk Assessment</h2>
                </td>
            </tr>
            {risk_score_row}
            <tr>
                <th>Likelihood</th>
                <td>{self._get_likelihood_display()}</td>
            </tr>
            </table>
        </div>
        """

        return {"status": "generated", "div": text_value}

    def _get_prediction(self) -> List[FHIR_RiskAssessment_Prediction]:
        prediction: FHIR_RiskAssessment_Prediction = {
            "outcome": self._get_outcome_code(),
            "qualitativeRisk": self._get_qualitative_risk(),
        }
        if self.probability is not None:
            probability = round(self.probability, 17)
            prediction["probabilityDecimal"] = probability
        return [prediction]

    def _get_qualitative_risk(self) -> FHIR_CodeableConcept:
        return {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/risk-probability",
                    "code": self.likelihood.value,
                    "display": self._get_likelihood_display(),
                }
            ],
            "text": self.likelihood.value,
        }

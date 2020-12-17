import pytest

from fhir_helpers.models import (
    CodeableConcept,
    Coding,
    InvalidArgumentError,
    RiskAssessment,
)


def test_no_patient_id_exception() -> None:
    with pytest.raises(InvalidArgumentError):
        RiskAssessment(
            patient_id=None,  # type: ignore
            outcome=CodeableConcept(text="test"),
            likelihood=RiskAssessment.Likelihood.MODERATE,
        )


def test_no_outcome_exception() -> None:
    with pytest.raises(InvalidArgumentError):
        RiskAssessment(
            patient_id="test",
            outcome=None,  # type: ignore
            likelihood=RiskAssessment.Likelihood.MODERATE,
        )


def test_bad_outcome_exception() -> None:
    with pytest.raises(InvalidArgumentError):
        RiskAssessment(
            patient_id="test",
            outcome=6,  # type: ignore
            likelihood=RiskAssessment.Likelihood.MODERATE,
        )


def test_no_likelihood_exception() -> None:
    with pytest.raises(InvalidArgumentError):
        RiskAssessment(
            patient_id="test",
            outcome=CodeableConcept(text="test"),
            likelihood=None,  # type: ignore
        )


def test_bad_likelihood_exception() -> None:
    with pytest.raises(InvalidArgumentError):
        RiskAssessment(
            patient_id="test",
            outcome=CodeableConcept(text="test"),
            likelihood=7,  # type: ignore
        )


def test_get_likelihood_display() -> None:
    ra = RiskAssessment(
        patient_id="test",
        outcome=CodeableConcept(text="test"),
        likelihood=RiskAssessment.Likelihood.MODERATE,
    )

    assert "Moderate likelihood" == ra._get_likelihood_display()

    ra.likelihood = RiskAssessment.Likelihood.LOW

    assert "Low likelihood" == ra._get_likelihood_display()


def test_get_text() -> None:
    ra = RiskAssessment(
        patient_id="test",
        outcome=CodeableConcept(text="test"),
        likelihood=RiskAssessment.Likelihood.MODERATE,
        probability=0.50,
    )
    narrative = ra._get_text()
    assert narrative["status"] == "generated"
    assert "<td>Moderate likelihood</td>" in narrative["div"]


def test_occurrence() -> None:
    date = "2020-07-06T13:21:30+00:00"
    ra = RiskAssessment(
        date=date,
        patient_id="test",
        outcome=CodeableConcept(text="test", codings=[Coding("a", "b", "c")]),
        likelihood=RiskAssessment.Likelihood.MODERATE,
        probability=0.50,
    )

    entries = ra.get_entries()
    assert len(entries) == 1

    assert entries[0]["resource"]["occurrenceDateTime"] == date

    # TODO: Test occurrenceX value

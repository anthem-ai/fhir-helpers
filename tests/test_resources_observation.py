from datetime import datetime

from fhir_helpers.resources.lpr import LPR
from fhir_helpers.resources.observation import Observations

from .helpers import (
    get_example_bundle,
    get_example_bundle_proto,
    get_example_values_bundle,
    get_example_values_bundle_proto,
)


def test_observations_find() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())
    assert len(lpr_dict.observations) == 137
    assert len(lpr_proto.observations) == 137

    observations_dict = lpr_dict.observations.find_by_coding(
        "85354-9", system="http://loinc.org"
    )
    observations_proto = lpr_proto.observations.find_by_coding(
        "85354-9", system="http://loinc.org"
    )
    assert len(observations_dict) == 10
    assert len(observations_proto) == 10

    assert len(lpr_dict.observations.find_by_coding("85354-9", system="1234")) == 0
    assert len(lpr_proto.observations.find_by_coding("85354-9", system="1234")) == 0
    assert len(lpr_dict.observations.find_by_coding(system="http://loinc.org")) == 137
    assert len(lpr_proto.observations.find_by_coding(system="http://loinc.org")) == 137

    three_years_ago = datetime(year=2018, month=3, day=6)

    observations_dict_temp = observations_dict.find_after_date(three_years_ago)
    observations_proto_temp = observations_proto.find_after_date(three_years_ago)
    assert len(observations_dict_temp) == 3
    assert len(observations_proto_temp) == 3

    observations_dict_temp = observations_dict.find_before_date(three_years_ago)
    observations_proto_temp = observations_proto.find_before_date(three_years_ago)
    assert len(observations_dict_temp) == 7
    assert len(observations_proto_temp) == 7


def test_observation_search() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert len(lpr_dict.observations.find_by_text_match("Body Mass")) == 18
    assert len(lpr_proto.observations.find_by_text_match("Body Mass")) == 18


def test_observations_find_by_value() -> None:
    lpr_dict = LPR(get_example_values_bundle())
    lpr_proto = LPR(get_example_values_bundle_proto())

    obs = lpr_dict.observations.find_by_coding("39156-5").find_by_value(
        {"comparator": "<", "quantity_value": 20}
    )
    assert len(obs) == 1

    obs = lpr_proto.observations.find_by_coding("39156-5").find_by_value(
        {"comparator": "<", "quantity_value": 20}
    )
    assert len(obs) == 1


def test_observation_quantity_values() -> None:
    lpr_dict = LPR(get_example_values_bundle())
    dict_obs = lpr_dict.observations

    assert len(dict_obs.find_by_coding("39156-5").lt(20)) == 1
    assert len(dict_obs.find_by_coding("39156-5").gt(20)) == 2
    assert len(dict_obs.find_by_coding("39156-5").eq(22)) == 1
    assert len(dict_obs.find_by_coding("39156-5").lte(22)) == 2
    assert len(dict_obs.find_by_coding("39156-5").gte(22)) == 2


def test_observation_component_values() -> None:
    lpr_dict = LPR(get_example_values_bundle())
    lpr_proto = LPR(get_example_values_bundle_proto())

    component_dict = lpr_dict.observations.find_by_coding("85354-9")
    component_proto = lpr_proto.observations.find_by_coding("85354-9")

    obs = component_dict.find_by_component_value(
        code="8462-4",
        value_query={
            "quantity_value": 90,
            "quantity_unit": "mm[Hg]",
            "comparator": "<",
        },
    )
    assert len(obs) == 1

    obs = component_proto.find_by_component_value(
        code="8462-4",
        value_query={
            "quantity_value": 90,
            "quantity_unit": "mm[Hg]",
            "comparator": "<",
        },
    )
    assert len(obs) == 1

    # check >=
    obs = component_dict.find_by_component_value(
        code="8462-4",
        value_query={
            "quantity_value": 83,
            "quantity_unit": "mm[Hg]",
            "comparator": ">=",
        },
    )
    assert len(obs) == 1

    obs = component_proto.find_by_component_value(
        code="8462-4",
        value_query={
            "quantity_value": 83,
            "quantity_unit": "mm[Hg]",
            "comparator": ">=",
        },
    )
    assert len(obs) == 1

    # none < 50
    obs = component_dict.find_by_component_value(
        code="8462-4",
        value_query={
            "quantity_value": 80,
            "quantity_unit": "mm[Hg]",
            "comparator": "<",
        },
    )
    assert len(obs) == 0

    obs = component_proto.find_by_component_value(
        code="8462-4",
        value_query={
            "quantity_value": 80,
            "quantity_unit": "mm[Hg]",
            "comparator": "<",
        },
    )
    assert len(obs) == 0

    # bad unit
    obs = component_dict.find_by_component_value(
        code="8462-4",
        value_query={
            "quantity_value": 90,
            "quantity_unit": "123[Hg]",
            "comparator": "<",
        },
    )
    assert len(obs) == 0

    obs = component_proto.find_by_component_value(
        code="8462-4",
        value_query={
            "quantity_value": 90,
            "quantity_unit": "123[Hg]",
            "comparator": "<",
        },
    )
    assert len(obs) == 0


def test_procedure_sort() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    sorted_dict = lpr_dict.observations.sort_by_date()
    sorted_proto = lpr_proto.observations.sort_by_date()
    sorted_dict_reverse = lpr_dict.observations.sort_by_date(reverse=True)
    sorted_proto_reverse = lpr_proto.observations.sort_by_date(reverse=True)

    dates = sorted([p.effective_datetime for p in sorted_dict if p.effective_datetime])
    dates_reverse = sorted(dates, reverse=True)

    for i in range(len(dates)):
        assert sorted_dict.get(i).effective_datetime == dates[i]
        assert sorted_proto.get(i).effective_datetime == dates[i]
        assert sorted_dict_reverse.get(i).effective_datetime == dates_reverse[i]
        assert sorted_proto_reverse.get(i).effective_datetime == dates_reverse[i]


def test_filter() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    obs_dict = lpr_dict.observations.filter(lambda o: o is not None)
    obs_proto = lpr_proto.observations.filter(lambda o: o is not None)

    assert isinstance(obs_dict, Observations)
    assert len(obs_dict) == 137
    assert isinstance(obs_proto, Observations)
    assert len(obs_proto) == 137


def test_union() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    three_years_ago = datetime(year=2018, month=3, day=6)

    before = lpr_dict.observations.find_before_date(three_years_ago)
    after = lpr_proto.observations.find_after_date(three_years_ago)

    union_observations = Observations().union(before, after)

    assert isinstance(union_observations, Observations)
    assert len(union_observations) == 137

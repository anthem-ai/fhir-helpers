import json
import os
from datetime import datetime

from fhir_helpers.resources.lpr import LPR
from fhir_helpers.utils import calc_time_ago


def get_insights() -> None:
    filename = "85e52038-4d69-50e9-9e46-e379b8d830af.json"

    # Uncomment this line to read filename from command-line
    # filename = sys.argv[1]

    if not os.path.exists(filename):
        print(f"File {filename} does not exist")
        return

    try:
        f = open(filename, "r")
        x = f.read()
        y = json.loads(x)
    except ValueError:
        print(f"Decoding JSON in {filename} has failed")
        return

    lpr = LPR(y)

    birth_date = lpr.patient.birthdate

    print(f"Patient birth date is {birth_date}")

    patient_age = lpr.patient.age

    print(f"Patient age is {patient_age} years old")

    # Helper function to calculate time_ago
    three_years_ago = calc_time_ago(years=3)

    print("\n*** Patient observations: ***")

    observations = lpr.observations.find_after_date(after_date=three_years_ago)

    for observation in observations:
        print(f"\n\tDate: {observation.effective_datetime}")

        if observation.value is not None:
            value = ""

            codes = observation.code.coding
            for code in codes:
                print(f"\tObservation: {code.display}")
                print(f"\tCode: {code.code}")
                print(f"\tSystem: {code.system}")

            if observation.value.value_codeable_concept is not None:
                codes = observation.value.value_codeable_concept.coding
                for code in codes:
                    value = f"{code.display}"
                    print(f"\tValue: {code.display}")
                    print(f"\tCode: {code.code}")
                    print(f"\tSystem: {code.system}")

            if len(value) == 0:
                if (
                    observation.value.value_quantity is not None
                    and str(observation.value.value_quantity) != "None"
                ):
                    print(
                        f"\tValue quantity: {observation.value.value_quantity.value} \
                            {observation.value.value_quantity.unit}"
                    )

                if observation.value.value_int is not None:
                    print(f"\tValue int: {observation.value.value_int}")

                if observation.value.value_string is not None:
                    print(f"\tValue string: {observation.value.value_string}")

                if observation.value.value_boolean is not None:
                    print(f"\tValue boolean: {observation.value.value_boolean}")

    print("\n*** Patient procedures: ***")

    procedures = lpr.procedures.find_after_date(after_date=three_years_ago)

    for procedure in procedures:
        # Display all procedure dates
        print(f"\n\tDate: {procedure.performed_datetime}")

        # Only display details for procedures on date of interest
        assert procedure.performed_datetime is not None

        if (
            procedure.performed_datetime.date()
            == datetime.fromisoformat("2019-11-16").date()
        ):
            codes = procedure.code.coding
            for code in codes:
                print(f"\tProcedure: {code.display}")
                print(f"\tCode: {code.code}")
                print(f"\tSystem: {code.system}")

    """
    # Alternate approach: string match
    for procedure in procedures:
        if procedure.search_text("2019-11-16"):
            print (f"\n\tDate: {procedure.performed_datetime}")

            codes = procedure.code.coding
            for code in codes:
                print(f"\tProcedure: {code.display}")
                print(f"\tCode: {code.code}")
                print(f"\tSystem: {code.system}")
    """

    print("\n*** Patient conditions: ***")

    conditions = lpr.conditions.find_after_date(after_date=three_years_ago)

    for condition in conditions:
        print(f"\n\tDate: {condition.recorded_date}")

        # Only display details for conditions on date of interest
        assert condition.recorded_date is not None

        if (
            condition.recorded_date.date()
            == datetime.fromisoformat("2019-11-16").date()
        ):
            codes = condition.code.coding
            for code in codes:
                print(f"\tCondition: {code.display}")
                print(f"\tCode: {code.code}")
                print(f"\tSystem: {code.system}")

    print("\n*** Patient medication requests: ***")

    medication_requests = lpr.medication_requests.find_after_date(
        after_date=three_years_ago
    )

    for medication_request in medication_requests:
        print(f"\n\tDate: {medication_request.authored_on}")

        # Only display details for medication requests on date of interest
        assert medication_request.authored_on is not None

        if (
            medication_request.authored_on.date()
            == datetime.fromisoformat("2019-11-16").date()
        ):
            codes = medication_request.medication_codeable_concept.coding
            for code in codes:
                print(f"\tMedication: {code.display}")
                print(f"\tCode: {code.code}")
                print(f"\tSystem: {code.system}")

    print("\n*** End of Patient resources ***\n")

    # Covid search_text() example
    covid = [
        (str(cond.code.coding[0].display) + " at " + str(cond.onset_datetime))
        for cond in lpr.conditions.sort_by_date()
        if cond.search_text("covid")
    ]

    covid_display = "\n## Covid conditions:\n" + (
        "None" if not covid else "\n".join(f"* {cond}" for cond in covid)
    )

    print(covid_display + "\n")


if __name__ == "__main__":
    get_insights()

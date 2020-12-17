# basic example

This example uses the [FHIR Helpers](https://github.com/anthem-ai/fhir-helpers "FHIR Helpers") package to display a patient's health trajectory and Covid history.

## Getting started

Getting started is pretty simple.

1. Make sure `python` (v3.8 or v3.9) is installed.
1. Run `pip3 install fhir-helpers` if you have not already installed the FHIR Helpers package on your system.
    ```shell
    pip3 install fhir-helpers
    ```
1. Create a virtual env for this project.
    ```shell
    python3 -m venv .venv
    ```
1. Activate the virtual env.
    ```shell
    # in MacOS
    source .venv/bin/activate
    ```
1. Install the dependencies with existing `make` scripts
    ```shell
    make install-dev
    ```
1. Run the app
    ```shell
    python3 main.py
    ```

**Success!**

## Developing with `fhir-helpers`

The `fhir-helpers` Python package is installed as part of the `make install` command. You will need to import specific classes and functions from the package.

## Resource fetch examples

This example uses a synthetic data record to illustrate using `fhir-helpers` to retrieve values from the record and constructing a patient trajectory or timeline.

### Use `LPR` and helper function

The `LPR` class lets you read values from the patient record without having to traverse it manually. `LPR` contains references to the resources included in the file, and allows you to read a complete resource as well as specific fields and values in the resource.

Start by importing the `LPR` class and the `calc_time_ago()` helper function.

```python
from fhir_helpers.resources.lpr import LPR
from fhir_helpers.utils import calc_time_ago
```

### Load the JSON file

The LPR JSON filename to load is hardcoded, but the source code contains instrucitons for including the filename as the first command-line argument. If the file does not exist or cannot be read, then the program displays an error message and exits.

```python
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
```

If successful, the loaded JSON is used to instantiate a LPR object.

```python
    lpr = LPR(y)
```
### Get patient age

The patient's current age is a property of the LPR. Instantiate a `LPR` object and then reference the `patient_age` property. Alternatively, the patient birthdate is also a property of the LPR.

```python
    birth_date = lpr.patient.birthdate
    patient_age = lpr.patient.age

    print(f"Patient age is {patient_age} years old.")
```

Run `main.py` and include the patient record file as a commmand-line argument. It should print the patient age to the console.

```bash
% python3 main.py 85e52038-4d69-50e9-9e46-e379b8d830af.json
Patient age is 14 years old.
```

## Retrieve resources from the LPR

For this example, fetch resources from the `LPR` in the order in which a clinician would typically read the timeline. This is the scenario: A patient displays an elevated temperature (and possibly other symptoms). This `Observation` may lead a clinician to suspect something is wrong. The clinician orders a `Procedure`, such as a throat swab. If the `Procedure` comes back positive it may indicate a `Condition` such as strep throat. The clinician may order a `MedicationRequest` (or prescription) for the patient.

The `LPR` contains many resources covering multiple years. Together, these provide the *trajectory* of the patient care. The examples provided here start with the big picture and then focus on specific dates in the patient record.

### Set the earliest date of interest

The `calc_time_ago()` function imported from `fhir_helpers.utils` accepts several arguments and returns a `datetime` object offset from today.

```python
def calc_time_ago(years: int = 0, months: int = 0, days: int = 0) -> datetime:
```

In this app we use it to calculate a `datetime` three years in the past.

```python
    # Helper function to calculate time_ago
    three_years_ago = calc_time_ago(years=3)
```

In the following sections `three_years_ago` is used as the cutoff date when retrieving resources from the LPR.

### Retrieve Observations

For each of the resource types we follow the same pattern: fetch the resources, then iterate over the set and display readable values.

#### Fetch the list

 The first resource type of interest is `Observation`. The LPR has a property (`observations`) that aggregates all `Observation` resources. Chaining the `find_after_date()` method to the `observations` property prunes the list and returns only those `Observations` that satisfy the function argument.

```python
    observations = lpr.observations.find_after_date(after_date=three_years_ago)
```

#### Iterate over the list

This example illustrates one approach to finding resources of interest by printing out the properties in the `Observation`. You may want to add logic to prune the result set.

The following sequence illustrates a complex relationship between the codes that comprise the `Observation`. The `Observation` has a `CodeableConcept` object that applies to the resource, and the `Observation.value` property also has its own `CodeableConcept`. Together they fill-in the details of the `Observation`.

```python
    for observation in observations:
        print (f"\n\tDate: {observation.effective_datetime}")

        if observation.value is not None:
            value = ''
            
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
                if observation.value.value_quantity is not None and str(observation.value.value_quantity) != 'None':
                    print (f"\tValue quantity: {observation.value.value_quantity.value} {observation.value.value_quantity.unit}")
. . .
```

When run against the sample LPR, we get the following:

```bash
% python3 main.py 85e52038-4d69-50e9-9e46-e379b8d830af.json
*** Patient observations: ***

	Date: 2018-12-22 20:35:35-07:00
	Observation: Body Height
	Code: 8302-2
	System: http://loinc.org
	Value quantity: 147.4 cm

	Date: 2018-12-22 20:35:35-07:00
	Observation: Pain severity - 0-10 verbal numeric rating [Score] - Reported
	Code: 72514-3
	System: http://loinc.org
	Value quantity: 4 {score}

	Date: 2018-12-22 20:35:35-07:00
	Observation: Body Weight
	Code: 29463-7
	System: http://loinc.org
	Value quantity: 40.7 kg
. . .
%
```

There are nine `Observations` from the date 2018-12-22, and they may part of a wellness check or annual visit.

Looking further down the list reveals:

```bash
	Date: 2019-11-16 20:35:35-07:00
	Observation: Body temperature
	Code: 8310-5
	System: http://loinc.org
	Observation: Oral temperature
	Code: 8331-1
	System: http://loinc.org
	Value quantity: 37.323 Cel
```
That is equivalent to 99.2 Fahrenheit, so the patient had a mild elevation in temperature. That is the only `Observation` for 2019-11-16, so let's look at other resources and see if there is any connection.

### Retrieve Procedures

Follow the same approach in retrieving all `Procedures`.

```python
    print(f"\n*** Patient procedures: ***")

    procedures = lpr.procedures.find_after_date(after_date=three_years_ago)

    for procedure in procedures:
        print (f"\n\tDate: {procedure.performed_datetime}")

        codes = procedure.code.coding
        for code in codes:
            print(f"\tProcedure: {code.display}")
            print(f"\tCode: {code.code}")
            print(f"\tSystem: {code.system}")

```

That results in a lot of noise. Modify the code to display details only for `Procedures` from 2019-11-16.

```python
    print(f"\n*** Patient procedures: ***")

    procedures = lpr.procedures.find_after_date(after_date=three_years_ago)

    for procedure in procedures:
        # Display all procedure dates
        print (f"\n\tDate: {procedure.performed_datetime}")

        # Only display details for procedures on date of interest
        if procedure.performed_datetime.date() == datetime.fromisoformat("2019-11-16").date():
            codes = procedure.code.coding
            for code in codes:
                print(f"\tProcedure: {code.display}")
                print(f"\tCode: {code.code}")
                print(f"\tSystem: {code.system}")
```

This displays a throat culture from that date.

```bash
*** Patient procedures: ***

	Date: 2018-12-22 20:35:35-07:00

	Date: 2019-11-16 20:35:35-07:00
	Procedure: Throat culture (procedure)
	Code: 117015009
	System: http://snomed.info/sct

	Date: 2019-12-07 20:35:35-07:00
. . .
```

This appears to be useful information. First we found the elevated temperature `Observation`, then a throat culture `Procedure`. Next, continue searching for other resources on that date.

### Retrieve Conditions

Perform the same focused lookup for `Condition`.

```python
    print(f"\n*** Patient conditions: ***")

    conditions = lpr.conditions.find_after_date(after_date=three_years_ago)

    for condition in conditions:
        print(f"\n\tDate: {condition.recorded_date}")

        # Only display details for conditions on date of interest
        if condition.recorded_date.date() == datetime.fromisoformat("2019-11-16").date():
            codes = condition.code.coding
            for code in codes:
                print(f"\tCondition: {code.display}")
                print(f"\tCode: {code.code}")
                print(f"\tSystem: {code.system}")
``` 

This results in:

```bash
*** Patient conditions: ***

	Date: 2019-11-16 20:35:35-07:00
	Condition: Streptococcal sore throat (disorder)
	Code: 43878008
	System: http://snomed.info/sct
. . .
```

### Retrieve MedicationRequests

Finally, check for `MedicationRequests` on that date.

```python
    print(f"\n*** Patient medication requests: ***")

    medication_requests = lpr.medication_requests.find_after_date(after_date=three_years_ago)

    for medication_request in medication_requests:
        print (f"\n\tDate: {medication_request.authored_on}")

        # Only display details for medication requests on date of interest
        if medication_request.authored_on.date() == datetime.fromisoformat("2019-11-16").date():
            codes = medication_request.medication_codeable_concept.coding
            for code in codes:
                print(f"\tMedication: {code.display}")
                print(f"\tCode: {code.code}")
                print(f"\tSystem: {code.system}")
```

This displays the following:

```bash
*** Patient medication requests: ***

	Date: 2019-11-16 20:35:35-07:00
	Medication: Penicillin V Potassium 250 MG Oral Tablet
	Code: 834061
	System: http://www.nlm.nih.gov/research/umls/rxnorm
. . .
```

### Tie it together

Starting with the elevated temperature `Observation`, we found that a throat culture `Procedure` was performed, which confirmed a Streptococcal sore throat `Condition`, for which the clinician created a `MedicationRequest` for Penicillin.

### Exercise

Using similar techniques as above, determine what led to the MedicationRequest for Acetaminophen on 2019-12-22.

## `search_text()` example

This app includes a block that uses the `search_text()` function in `fhir-helpers` to find all `Condition` resources in a Longitudinal Patient Record (LPR) that contain the string "covid". Each occurrence is added to an array variable named `covid`. The array contents are then appended to a string variable.

```python
    covid = [
        (str(cond.code.coding[0].display) + " at " + str(cond.onset_datetime))
        for cond in lpr.conditions
        if cond.search_text("covid")
    ]

    covid_display = "\n## Covid conditions:\n" + (
        "None" if not covid else "\n".join(f"* {cond}" for cond in covid)
    )
```

 Running this code against the sample LPR `85e52038-4d69-50e9-9e46-e379b8d830af.json`, and then printing the variable `covid_display`, displays the following:

```bash
## Covid conditions:
* Suspected COVID-19 at 2020-03-11 21:35:35-06:00
* COVID-19 at 2020-03-11 22:50:35-06:00

```

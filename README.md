# FHIR Helpers

## Introduction

The FHIR Helpers package (`fhir-helpers`) provides an easy way to find resources and values in a Longitudinal Patient Record (LPR). When used in your code, `fhir-helpers` eliminates the need for code to traverse the patient record looking for matching resources.

This document includes an [example](./example/basic "example") and synthetic data record that illustrates using `fhir-helpers` to retrieve values from the record and constructing a patient trajectory or timeline.


## Supported resource types

`fhir-helpers` supports many FHIR R4 resources, including Patient, Condition, Observation, MedicationRequest, Procedure, and others. The classes defining the resources are in `fhir_helpers/resources/`.


## Capabilities of `fhir-helpers`

`fhir-helpers` supports the following operations for finding resources:
- Date arithmetic and matching
- String searches using `<Resource>.search_text()`, matching a portion of the text you want to find
- Code searches, for finding resources that match a specific code value
- Numeric comparisons (less than, greater than, and so on). These can also be included in method chaining, allowing you to prune the result set very quickly.

Find out more about resources and coding systems using the links listed in the [`More information`](#more-info) section of this document.


## Getting started

The included [example](./example/basic "example") and synthetic data record illustrate using `fhir-helpers` to retrieve values from the record and constructing a sample patient trajectory or timeline.


## More information {: #more-info }

This document does not describe coding systems or FHIR R4. The following websites provide more information:
- [LOINC codes](http://loinc.org "Clinical terminology")
- [SNOMED codes](http://snomed.info/sct "Clinical Terminology")
- [National Library of Medicine](http://www.nlm.nih.gov/research/umls/rxnorm "Normalized drug names")
- [HL7 FHIR R4](http://hl7.org/fhir/R4/ "FHIR R4 spec")

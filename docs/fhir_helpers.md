# FHIR Helpers


### _class_ fhir_helpers.resources.allergy_intolerance.AllergyIntolerance(lpr: LPR)
Bases: `fhir_helpers.resources.resource.Resource`


#### _abstract property_ onset_datetime(_: Optional[datetime.datetime_ )

#### _abstract property_ code(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

### _class_ fhir_helpers.resources.allergy_intolerance.AllergyIntoleranceDict(data: fhir_types.FHIR_AllergyIntolerance.FHIR_AllergyIntolerance)
Bases: `fhir_helpers.resources.allergy_intolerance.AllergyIntolerance`


#### _property_ onset_datetime(_: Optional[datetime.datetime_ )

#### _property_ code(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.allergy_intolerance.AllergyIntoleranceProto(data_proto: proto.google.fhir.proto.r4.core.resources.allergy_intolerance_pb2.AllergyIntolerance)
Bases: `fhir_helpers.resources.allergy_intolerance.AllergyIntolerance`


#### _property_ onset_datetime(_: Optional[datetime.datetime_ )

#### _property_ code(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.allergy_intolerance.AllergyIntolerances(items: List[fhir_helpers.resources.resource_list.T] = [])
Bases: `fhir_helpers.resources.resource_list.ResourceList`[`fhir_helpers.resources.allergy_intolerance.AllergyIntolerance`]


#### find_by_coding(code: str = '', system: str = '', display: str = '')

### _class_ fhir_helpers.resources.codeable_concept.CodeableConcept()
Bases: `abc.ABC`


#### _abstract property_ coding(_: List[fhir_helpers.resources.coding.Coding_ )

#### empty()

#### has_coding(code_str: str = '', system_str: str = '', display_str: str = '')

### _class_ fhir_helpers.resources.codeable_concept.CodeableConceptDict(data: fhir_types.FHIR_CodeableConcept.FHIR_CodeableConcept)
Bases: `fhir_helpers.resources.codeable_concept.CodeableConcept`


#### _property_ coding(_: List[fhir_helpers.resources.coding.Coding_ )

### _class_ fhir_helpers.resources.codeable_concept.CodeableConceptProto(concept: proto.google.fhir.proto.r4.core.datatypes_pb2.CodeableConcept)
Bases: `fhir_helpers.resources.codeable_concept.CodeableConcept`


#### _property_ coding(_: List[fhir_helpers.resources.coding.Coding_ )

### _class_ fhir_helpers.resources.coding.Coding()
Bases: `abc.ABC`


#### _abstract property_ code(_: st_ )

#### _abstract property_ system(_: st_ )

#### _abstract property_ display(_: st_ )

### _class_ fhir_helpers.resources.coding.CodingDict(data: fhir_types.FHIR_Coding.FHIR_Coding)
Bases: `fhir_helpers.resources.coding.Coding`


#### _property_ code(_: st_ )

#### _property_ system(_: st_ )

#### _property_ display(_: st_ )

### _class_ fhir_helpers.resources.coding.CodingProto(coding: proto.google.fhir.proto.r4.core.datatypes_pb2.Coding)
Bases: `fhir_helpers.resources.coding.Coding`


#### _property_ code(_: st_ )

#### _property_ system(_: st_ )

#### _property_ display(_: st_ )

### _class_ fhir_helpers.resources.condition.Condition(lpr: LPR)
Bases: `fhir_helpers.resources.resource.Resource`


#### _abstract property_ recorded_date(_: Optional[datetime.datetime_ )

#### _abstract property_ onset_datetime(_: Optional[datetime.datetime_ )

#### _abstract property_ code(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

### _class_ fhir_helpers.resources.condition.ConditionDict(data: fhir_types.FHIR_Condition.FHIR_Condition)
Bases: `fhir_helpers.resources.condition.Condition`


#### _property_ recorded_date(_: Optional[datetime.datetime_ )

#### _property_ onset_datetime(_: Optional[datetime.datetime_ )

#### _property_ code(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.condition.ConditionProto(condition: proto.google.fhir.proto.r4.core.resources.condition_pb2.Condition)
Bases: `fhir_helpers.resources.condition.Condition`


#### _property_ recorded_date(_: Optional[datetime.datetime_ )

#### _property_ onset_datetime(_: Optional[datetime.datetime_ )

#### _property_ code(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.condition.Conditions(items: List[fhir_helpers.resources.resource_list.T] = [])
Bases: `fhir_helpers.resources.resource_list.ResourceList`[`fhir_helpers.resources.condition.Condition`]


#### find_by_coding(code: str = '', system: str = '', display: str = '')

### _class_ fhir_helpers.resources.encounter.Encounter(lpr: LPR)
Bases: `fhir_helpers.resources.resource.Resource`


#### _abstract property_ period(_: fhir_helpers.resources.period.Perio_ )

#### _abstract property_ type(_: List[fhir_helpers.resources.codeable_concept.CodeableConcept_ )

### _class_ fhir_helpers.resources.encounter.EncounterDict(data: fhir_types.FHIR_Encounter.FHIR_Encounter)
Bases: `fhir_helpers.resources.encounter.Encounter`


#### _property_ period(_: fhir_helpers.resources.period.Perio_ )

#### _property_ type(_: List[fhir_helpers.resources.codeable_concept.CodeableConcept_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.encounter.EncounterProto(data_proto: proto.google.fhir.proto.r4.core.resources.encounter_pb2.Encounter)
Bases: `fhir_helpers.resources.encounter.Encounter`


#### _property_ period(_: fhir_helpers.resources.period.Perio_ )

#### _property_ type(_: List[fhir_helpers.resources.codeable_concept.CodeableConcept_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.encounter.Encounters(items: List[fhir_helpers.resources.resource_list.T] = [])
Bases: `fhir_helpers.resources.resource_list.ResourceList`[`fhir_helpers.resources.encounter.Encounter`]


#### find_by_coding(code: str = '', system: str = '', display: str = '')

### _class_ fhir_helpers.resources.human_name.HumanName()
Bases: `abc.ABC`


#### _abstract property_ text(_: st_ )

#### _abstract property_ family(_: st_ )

#### _abstract property_ given(_: List[str_ )

#### _abstract property_ prefix(_: List[str_ )

#### _abstract property_ suffix(_: List[str_ )

#### _abstract property_ use(_: Literal['usual', 'official', 'temp', 'nickname', 'anonymous', 'old', 'maiden'_ )

#### _property_ display_name(_: st_ )

### _class_ fhir_helpers.resources.human_name.HumanNameDict(data: fhir_types.FHIR_HumanName.FHIR_HumanName)
Bases: `fhir_helpers.resources.human_name.HumanName`


#### _property_ text(_: st_ )

#### _property_ family(_: st_ )

#### _property_ given(_: List[str_ )

#### _property_ prefix(_: List[str_ )

#### _property_ suffix(_: List[str_ )

#### _property_ use(_: Literal['usual', 'official', 'temp', 'nickname', 'anonymous', 'old', 'maiden'_ )

### _class_ fhir_helpers.resources.human_name.HumanNameProto(human_name: proto.google.fhir.proto.r4.core.datatypes_pb2.HumanName)
Bases: `fhir_helpers.resources.human_name.HumanName`


#### _property_ text(_: st_ )

#### _property_ family(_: st_ )

#### _property_ given(_: List[str_ )

#### _property_ prefix(_: List[str_ )

#### _property_ suffix(_: List[str_ )

#### _property_ use(_: Literal['usual', 'official', 'temp', 'nickname', 'anonymous', 'old', 'maiden'_ )

### _class_ fhir_helpers.resources.immunization.Immunization(lpr: LPR)
Bases: `fhir_helpers.resources.resource.Resource`


#### _abstract property_ occurrence_datetime(_: Optional[datetime.datetime_ )

#### _abstract property_ vaccine_code(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

### _class_ fhir_helpers.resources.immunization.ImmunizationDict(data: fhir_types.FHIR_Immunization.FHIR_Immunization)
Bases: `fhir_helpers.resources.immunization.Immunization`


#### _property_ occurrence_datetime(_: Optional[datetime.datetime_ )

#### _property_ vaccine_code(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.immunization.ImmunizationProto(data_proto: proto.google.fhir.proto.r4.core.resources.immunization_pb2.Immunization)
Bases: `fhir_helpers.resources.immunization.Immunization`


#### _property_ occurrence_datetime(_: Optional[datetime.datetime_ )

#### _property_ vaccine_code(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.immunization.Immunizations(items: List[fhir_helpers.resources.resource_list.T] = [])
Bases: `fhir_helpers.resources.resource_list.ResourceList`[`fhir_helpers.resources.immunization.Immunization`]


#### find_by_coding(code: str = '', system: str = '', display: str = '')

### _class_ fhir_helpers.resources.lpr.LPR(lpr: Union[fhir_types.FHIR_Bundle.FHIR_Bundle, proto.google.fhir.proto.r4.core.resources.bundle_and_contained_resource_pb2.Bundle])
Bases: `object`


### _class_ fhir_helpers.resources.medication_dispense.MedicationDispense(lpr: LPR)
Bases: `fhir_helpers.resources.resource.Resource`


#### _abstract property_ when_handed_over(_: Optional[datetime.datetime_ )

#### _abstract property_ medication_codeable_concept(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### _abstract property_ status(_: st_ )

### _class_ fhir_helpers.resources.medication_dispense.MedicationDispenseDict(data: fhir_types.FHIR_MedicationDispense.FHIR_MedicationDispense)
Bases: `fhir_helpers.resources.medication_dispense.MedicationDispense`


#### _property_ when_handed_over(_: Optional[datetime.datetime_ )

#### _property_ medication_codeable_concept(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### _property_ status(_: st_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.medication_dispense.MedicationDispenseProto(medication_dispense: proto.google.fhir.proto.r4.core.resources.medication_dispense_pb2.MedicationDispense)
Bases: `fhir_helpers.resources.medication_dispense.MedicationDispense`


#### _property_ when_handed_over(_: Optional[datetime.datetime_ )

#### _property_ medication_codeable_concept(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### _property_ status(_: st_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.medication_dispense.MedicationDispenses(items: List[fhir_helpers.resources.resource_list.T] = [])
Bases: `fhir_helpers.resources.resource_list.ResourceList`[`fhir_helpers.resources.medication_dispense.MedicationDispense`]


#### find_by_coding(code: str = '', system: str = '', display: str = '')

### _class_ fhir_helpers.resources.medication_request.MedicationRequest(lpr: LPR)
Bases: `fhir_helpers.resources.resource.Resource`


#### _abstract property_ authored_on(_: Optional[datetime.datetime_ )

#### _abstract property_ medication_codeable_concept(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### _abstract property_ requester(_: fhir_helpers.resources.reference.Referenc_ )

#### _property_ requester_practitioner(_: Optional[fhir_helpers.resources.practitioner.Practitioner_ )

#### _abstract property_ status(_: st_ )

### _class_ fhir_helpers.resources.medication_request.MedicationRequestDict(data: fhir_types.FHIR_MedicationRequest.FHIR_MedicationRequest, lpr: LPR)
Bases: `fhir_helpers.resources.medication_request.MedicationRequest`


#### _property_ authored_on(_: Optional[datetime.datetime_ )

#### _property_ medication_codeable_concept(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### _property_ requester(_: fhir_helpers.resources.reference.Referenc_ )

#### _property_ status(_: st_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.medication_request.MedicationRequestProto(medication_request: proto.google.fhir.proto.r4.core.resources.medication_request_pb2.MedicationRequest, lpr: LPR)
Bases: `fhir_helpers.resources.medication_request.MedicationRequest`


#### _property_ authored_on(_: Optional[datetime.datetime_ )

#### _property_ medication_codeable_concept(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### _property_ requester(_: fhir_helpers.resources.reference.Referenc_ )

#### _property_ status(_: st_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.medication_request.MedicationRequests(items: List[fhir_helpers.resources.resource_list.T] = [])
Bases: `fhir_helpers.resources.resource_list.ResourceList`[`fhir_helpers.resources.medication_request.MedicationRequest`]


#### find_by_coding(code: str = '', system: str = '', display: str = '')

### _class_ fhir_helpers.resources.observation_component.ObservationComponent()
Bases: `abc.ABC`


#### _abstract property_ codeable_concept(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### _abstract property_ value(_: fhir_helpers.resources.observation_value.ObservationValu_ )

### _class_ fhir_helpers.resources.observation_component.ObservationComponentDict(data: fhir_types.FHIR_Observation_Component.FHIR_Observation_Component)
Bases: `fhir_helpers.resources.observation_component.ObservationComponent`


#### _property_ codeable_concept(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### _property_ value(_: fhir_helpers.resources.observation_value.ObservationValu_ )

### _class_ fhir_helpers.resources.observation_component.ObservationComponentProto(data: proto.google.fhir.proto.r4.core.resources.observation_pb2.Component)
Bases: `fhir_helpers.resources.observation_component.ObservationComponent`


#### _property_ codeable_concept(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### _property_ value(_: fhir_helpers.resources.observation_value.ObservationValu_ )

### _class_ fhir_helpers.resources.observation.Observation(lpr: LPR)
Bases: `fhir_helpers.resources.resource.Resource`


#### _abstract property_ effective_datetime(_: Optional[datetime.datetime_ )

#### _abstract property_ code(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### _abstract property_ value(_: fhir_helpers.resources.observation_value.ObservationValu_ )

#### _abstract property_ component(_: List[fhir_helpers.resources.observation_component.ObservationComponent_ )

### _class_ fhir_helpers.resources.observation.ObservationDict(data: fhir_types.FHIR_Observation.FHIR_Observation)
Bases: `fhir_helpers.resources.observation.Observation`


#### _property_ effective_datetime(_: Optional[datetime.datetime_ )

#### _property_ code(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### _property_ value(_: fhir_helpers.resources.observation_value.ObservationValu_ )

#### _property_ component(_: List[fhir_helpers.resources.observation_component.ObservationComponent_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.observation.ObservationProto(observation: proto.google.fhir.proto.r4.core.resources.observation_pb2.Observation)
Bases: `fhir_helpers.resources.observation.Observation`


#### _property_ effective_datetime(_: Optional[datetime.datetime_ )

#### _property_ code(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### _property_ value(_: fhir_helpers.resources.observation_value.ObservationValu_ )

#### _property_ component(_: List[fhir_helpers.resources.observation_component.ObservationComponent_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.observation.Observations(items: List[fhir_helpers.resources.resource_list.T] = [])
Bases: `fhir_helpers.resources.resource_list.ResourceList`[`fhir_helpers.resources.observation.Observation`]


#### find_by_coding(code: str = '', system: str = '', display: str = '')

#### find_by_value(value_query: fhir_helpers.resources.observation_value.ValueQuery = {})

#### find_by_component_value(code: str = '', system: str = '', display: str = '', value_query: fhir_helpers.resources.observation_value.ValueQuery = {})

#### eq(value_float: float)

#### gt(value_float: float)

#### lt(value_float: float)

#### gte(value_float: float)

#### lte(value_float: float)

### _class_ fhir_helpers.resources.observation_value.ValueQuery(\*args, \*\*kwargs)
Bases: `dict`


#### quantity_value(_: floa_ )

#### quantity_unit(_: st_ )

#### quantity_system(_: st_ )

#### quantity_code(_: st_ )

#### codeable_concept_code(_: st_ )

#### codeable_concept_system(_: st_ )

#### codeable_concept_display(_: st_ )

#### string_value(_: st_ )

#### integer_value(_: floa_ )

#### comparator(_: Literal['=', '>', '>=', '<', '<='_ )

### _class_ fhir_helpers.resources.observation_value.ObservationValue(value_quantity: fhir_helpers.resources.quantity.Quantity, value_codeable_concept: fhir_helpers.resources.codeable_concept.CodeableConcept, value_int: Optional[float] = None, value_string: Optional[str] = None, value_boolean: Optional[bool] = None)
Bases: `object`


#### match(value_query: fhir_helpers.resources.observation_value.ValueQuery = {})

#### _classmethod_ build_from_dict(observation: Union[fhir_types.FHIR_Observation.FHIR_Observation, fhir_types.FHIR_Observation_Component.FHIR_Observation_Component])

#### _classmethod_ build_from_proto(observation: Union[proto.google.fhir.proto.r4.core.resources.observation_pb2.Observation, proto.google.fhir.proto.r4.core.resources.observation_pb2.Component])

### _class_ fhir_helpers.resources.patient.Patient()
Bases: `abc.ABC`


#### _abstract property_ name(_: List[fhir_helpers.resources.human_name.HumanName_ )

#### _abstract property_ gender(_: st_ )

#### _abstract property_ birthdate(_: Optional[datetime.date_ )

#### _property_ display_name(_: st_ )

#### _abstract property_ id(_: st_ )

#### _property_ age(_: Optional[int_ )

#### _abstract property_ deceased_boolean(_: Optional[bool_ )

#### _abstract property_ deceased_datetime(_: Optional[datetime.datetime_ )

#### _property_ is_deceased(_: boo_ )

### _class_ fhir_helpers.resources.patient.PatientDict(data: fhir_types.FHIR_Patient.FHIR_Patient)
Bases: `fhir_helpers.resources.patient.Patient`


#### _property_ name(_: List[fhir_helpers.resources.human_name.HumanName_ )

#### _property_ gender(_: st_ )

#### _property_ birthdate(_: Optional[datetime.date_ )

#### _property_ id(_: st_ )

#### _property_ deceased_boolean(_: Optional[bool_ )

#### _property_ deceased_datetime(_: Optional[datetime.datetime_ )

### _class_ fhir_helpers.resources.patient.PatientProto(patient: proto.google.fhir.proto.r4.core.resources.patient_pb2.Patient)
Bases: `fhir_helpers.resources.patient.Patient`


#### _property_ name(_: List[fhir_helpers.resources.human_name.HumanName_ )

#### _property_ gender(_: st_ )

#### _property_ birthdate(_: Optional[datetime.date_ )

#### _property_ id(_: st_ )

#### _property_ deceased_boolean(_: Optional[bool_ )

#### _property_ deceased_datetime(_: Optional[datetime.datetime_ )

### _class_ fhir_helpers.resources.period.Period()
Bases: `abc.ABC`


#### _abstract property_ start(_: Optional[datetime.datetime_ )

#### end()

### _class_ fhir_helpers.resources.period.PeriodDict(data: fhir_types.FHIR_Period.FHIR_Period)
Bases: `fhir_helpers.resources.period.Period`


#### _property_ start(_: Optional[datetime.datetime_ )

#### _property_ end(_: Optional[datetime.datetime_ )

### _class_ fhir_helpers.resources.period.PeriodProto(period: proto.google.fhir.proto.r4.core.datatypes_pb2.Period)
Bases: `fhir_helpers.resources.period.Period`


#### _property_ start(_: Optional[datetime.datetime_ )

#### _property_ end(_: Optional[datetime.datetime_ )

### _class_ fhir_helpers.resources.practitioner.Practitioner(lpr: LPR)
Bases: `fhir_helpers.resources.resource.Resource`


#### _abstract property_ id(_: st_ )

#### _abstract property_ name(_: List[fhir_helpers.resources.human_name.HumanName_ )

#### _abstract property_ gender(_: st_ )

### _class_ fhir_helpers.resources.practitioner.PractitionerDict(data: fhir_types.FHIR_Practitioner.FHIR_Practitioner)
Bases: `fhir_helpers.resources.practitioner.Practitioner`


#### _property_ id(_: st_ )

#### _property_ name(_: List[fhir_helpers.resources.human_name.HumanName_ )

#### _property_ gender(_: st_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.practitioner.PractitionerProto(practitioner: proto.google.fhir.proto.r4.core.resources.practitioner_pb2.Practitioner)
Bases: `fhir_helpers.resources.practitioner.Practitioner`


#### _property_ id(_: st_ )

#### _property_ name(_: List[fhir_helpers.resources.human_name.HumanName_ )

#### _property_ gender(_: st_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.practitioner.Practitioners(items: List[fhir_helpers.resources.resource_list.T] = [])
Bases: `fhir_helpers.resources.resource_list.ResourceList`[`fhir_helpers.resources.practitioner.Practitioner`]


#### find_by_id(id: str)

### _class_ fhir_helpers.resources.procedure.Procedure(lpr: LPR)
Bases: `fhir_helpers.resources.resource.Resource`


#### _abstract property_ performed_datetime(_: Optional[datetime.datetime_ )

#### _abstract property_ code(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

### _class_ fhir_helpers.resources.procedure.ProcedureDict(data: fhir_types.FHIR_Procedure.FHIR_Procedure)
Bases: `fhir_helpers.resources.procedure.Procedure`


#### _property_ performed_datetime(_: Optional[datetime.datetime_ )

#### _property_ code(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.procedure.ProcedureProto(procedure: proto.google.fhir.proto.r4.core.resources.procedure_pb2.Procedure)
Bases: `fhir_helpers.resources.procedure.Procedure`


#### _property_ performed_datetime(_: Optional[datetime.datetime_ )

#### _property_ code(_: fhir_helpers.resources.codeable_concept.CodeableConcep_ )

#### search_text(search_str: str)

### _class_ fhir_helpers.resources.procedure.Procedures(items: List[fhir_helpers.resources.resource_list.T] = [])
Bases: `fhir_helpers.resources.resource_list.ResourceList`[`fhir_helpers.resources.procedure.Procedure`]


#### find_by_coding(code: str = '', system: str = '', display: str = '')

### _class_ fhir_helpers.resources.quantity.Quantity()
Bases: `abc.ABC`


#### _abstract property_ value(_: Optional[float_ )

#### _abstract property_ unit(_: st_ )

#### _abstract property_ code(_: st_ )

#### _abstract property_ system(_: st_ )

#### empty()

#### match(comparator: Literal['=', '>', '>=', '<', '<='], value_num: float, unit_str: str = '', system_str: str = '', code_str: str = '')

### _class_ fhir_helpers.resources.quantity.QuantityDict(data: fhir_types.FHIR_Quantity.FHIR_Quantity)
Bases: `fhir_helpers.resources.quantity.Quantity`


#### _property_ value(_: Optional[float_ )

#### _property_ unit(_: st_ )

#### _property_ code(_: st_ )

#### _property_ system(_: st_ )

### _class_ fhir_helpers.resources.quantity.QuantityProto(quantity: proto.google.fhir.proto.r4.core.datatypes_pb2.Quantity)
Bases: `fhir_helpers.resources.quantity.Quantity`


#### _property_ value(_: Optional[float_ )

#### _property_ unit(_: st_ )

#### _property_ code(_: st_ )

#### _property_ system(_: st_ )

### _class_ fhir_helpers.resources.reference.Reference()
Bases: `abc.ABC`


#### _abstract property_ reference(_: st_ )

#### _abstract property_ display(_: st_ )

### _class_ fhir_helpers.resources.reference.ReferenceDict(data: fhir_types.FHIR_Reference.FHIR_Reference)
Bases: `fhir_helpers.resources.reference.Reference`


#### _property_ reference(_: st_ )

#### _property_ display(_: st_ )

### _class_ fhir_helpers.resources.reference.ReferenceProto(data_proto: proto.google.fhir.proto.r4.core.datatypes_pb2.Reference)
Bases: `fhir_helpers.resources.reference.Reference`


#### _property_ reference(_: st_ )

#### _property_ display(_: st_ )

### _class_ fhir_helpers.resources.resource_list.ResourceList(items: List[fhir_helpers.resources.resource_list.T] = [])
Bases: `Generic`[`fhir_helpers.resources.resource_list.T`]


#### TResourceList()
alias of TypeVar(‘TResourceList’, bound=`ResourceList[T]`)


#### all()

#### add(item: fhir_helpers.resources.resource_list.T)

#### get(index: int)

#### exists()

#### first()

#### last()

#### filter(filter_func: Callable[[fhir_helpers.resources.resource_list.T], bool])

#### union(\*args: fhir_helpers.resources.resource_list.TResourceList)

#### or_(\*args: Callable[[fhir_helpers.resources.resource_list.TResourceList], fhir_helpers.resources.resource_list.TResourceList])

#### find_by_text_match(search_str: str)

#### find_after_date(after_date: datetime.datetime)

#### find_before_date(before_date: datetime.datetime)

#### sort_by_date(reverse: bool = False)

### _class_ fhir_helpers.resources.resource.Resource(lpr: LPR)
Bases: `abc.ABC`


#### _abstract_ search_text(search_str: str)

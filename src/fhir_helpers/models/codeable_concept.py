from dataclasses import dataclass, field
from typing import List

from .coding import Coding


@dataclass
class CodeableConcept:
    """
    Concept - reference to a terminology or just text. See `FHIR CodeableConcept
    <https://www.hl7.org/fhir/datatypes.html#CodeableConcept>`_ for more detail
    """

    text: str  #: Plain text representation of the concept

    #: codes defined by a terminology system
    codings: List[Coding] = field(default_factory=list)

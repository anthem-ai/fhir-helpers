from dataclasses import dataclass


@dataclass
class Coding:
    """
    A representation of a defined concept using a symbol from a defined "code system".
    See `FHIR Coding <https://www.hl7.org/fhir/datatypes.html#Coding>`_ for more detail
    """

    system: str  #: Identity of the terminology system
    code: str  #: Symbol in syntax defined by the system
    display: str  #: Representation defined by the system

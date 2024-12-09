from __future__ import annotations
from abc import ABC
from typing import Literal, TypeAlias


from pydantic import BaseModel, computed_field

from schema.metadata import Reference


class Species(BaseModel):
    """A chemical species."""

    # if points/molecular entities for a species are given, then identifiers can be derived from the set of molecular entity descriptors
    identifiers: list[SpeciesIdentifier]
    """descriptors of each species

    Identifiers are combined with a logical and, e.g., if the constitution "O2"
    and multiplicty 1 are supplied as identifiers, the species refers to
    single oxygen and not "oxygen or any molecule in a singlet state"
    """

    consists_of: list[Species]
    """lumping of more detailed species"""
    definition: list[SpeciesDefinition]
    """the ensemble of molecular entities that is is this species"""

class MolecularEntity(BaseModel):
    """identifiable and distinguishable entity"""

    constitution: Constitution
    connectivity: MolecularConnectivity
    isotope: Isotopes|None = None
    stereo: Stereochemistry|None = None
    el_struc: ElectronicStructure|None = None
    """usually the ground state is assumed"""

    # TODO introduce separate Molecular entity definiton? -> e.g. what about crystals, other materials

class SpeciesDefinition(BaseModel):
    """Connects a chemical species and the molecular entities that make up the species. This class assigns the role of the molecular entities."""

    type: Literal['conformer', 'ME lumped', 'general']  # all sub-types need to be listed here
    references: list[Reference]|None = None
    """How a species is defined through combining molecular entities depends a lot on the specific case and may be different for each study. Hence, this field allows to specify references that describe the lumping"""
    entities: list[MolecularEntity]

class ConformerEnsemble(SpeciesDefinition):
    """One of the simplest cases where a species is modeled as an ensemble of conformers"""

    type: Literal['conformer']

    # TODO additional fields that describe how the conformers were grouped (e.g. based on rotational constants or dihedral angles or ...)

class MasterEqnLumped(SpeciesDefinition):

    # TODO more general name and concept

    type: Literal['ME lumped']

    # TODO additional fields

class CoarseNode(BaseModel):
    """Node in a reaction network"""

    # can be extended, if necessary, subclasses for some roles can
    # add additional fields
    role: Literal['reactant', 'product', 'solvent', 'catalyst']
    species: Species

class CoarseEdge(BaseModel):        # TODO maybe rename "Reaction"
    """A chemical reaction"""

    nodes: list[CoarseNode]
    definition: ReactionDefinition

class ReactionDefinition(BaseModel):
    """analogous to SpeciesDefinition: connects the coarse edge to detailed
    edges
    """

    type: str
    references: list[Reference]|None = None
    """Literature reference where the detailed data was combined to a
    phenomenological reaction (rate). """
    entity: list[MolecularEntity]

class ReactionStep(ReactionDefinition):
    """elementary step in a stepwise reaction"""

    type: Literal['step']

class ReactionChannel(ReactionDefinition):
    """one of more parallel, competing reaction channels"""

    type: Literal['parallel']



##############################################################################
# identifiers -> move to separate module?
##############################################################################

class Constitution(BaseModel):
    """Molecular constitution"""

    element_count: dict[str, int]
    """example {"C": 1, "H": 4}"""

class Isotopes(BaseModel):
    """Isotope information for each atom"""

    n_neutrons: list[int]
    """number of neutrons for each atom"""

class MolecularConnectivity(BaseModel):
    """Connectivity between atoms"""

    # TODO graph data structure + canonical form for easy comparison
    # TODO special values for formed and broken bonds (for transition states, etc.)

class Stereochemistry(BaseModel):
    """Definition of the Stereochemistry"""

    # TODO define via stereocenters

class ElectronicStructure(BaseModel):
    """Definition of the electronic state"""

    charge: int
    spin: int

    # TODO: ensure extendibility, e.g., to add TermSymbols or group repr. later

    @computed_field
    def spin_multiplicity(self):
        return 2*self.spin+1


class StringIdentifier(BaseModel, ABC):

    type: str   # for easy identification of subtypes during validation
    value: str
    canonical_repr: str

class StandardInChI(StringIdentifier):
    """Standard IUPAC International Chemical Identifier

    Its value is the canonical_repr, since it is a canonical string
    representation."""

    type: Literal['SInChI']


class SMILES(StringIdentifier):
    """..."""

    type: Literal['SMILES']


SpeciesIdentifier: TypeAlias = Constitution|StandardInChI|SMILES
"""implementation detail: validation schemas do not support inheritance in the
classical sense. Instead, all subclasses have to be validated against."""


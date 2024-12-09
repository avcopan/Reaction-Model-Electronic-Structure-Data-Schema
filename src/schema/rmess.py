"""Defining the Reaction Model Electronic Structure Schema

See this link for a few examples of what you can do:
https://docs.pydantic.dev/latest/concepts/json_schema/#generating-json-schema
"""

import json

from pydantic import BaseModel

from el_struc_schema.src.schema.species import MolecularEntity


# Species
class Calculation(BaseModel):
    """An individual point/calculation"""

    # AVC question: Our SQL schema separates Point (geometry) from Calculation (input)
    #              Is this worth doing here as well?
    symbols: list[str]
    coordinates: list[tuple[float, float, float]]
    charge: int
    multiplicity: int
    frequencies: list[float]
    electronic_energy: float
    gibbs_energy: float


class Conformer(BaseModel):
    calculations: list[Calculation]  # see comment above about Point and Calculation


class Species(BaseModel):
    conformers: list[Conformer]


class Point(MolecularEntity):
    """set of molecular coordinates"""

    calculations: list[Calculation]


# Detail network elements
# Each detailed network will connect specific points at a specific level of theory
class DetailNodeBase(BaseModel):
    """A Node/"NetworkStage" in a detailed PES network"""

    role: str
    entities: list[MolecularEntity]

class DetailEdge(BaseModel):
    """An Edge/"ReactionStep" in a detailed PES network"""

    nodes: list[DetailNodeBase]


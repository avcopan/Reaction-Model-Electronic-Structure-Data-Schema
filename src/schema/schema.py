
# Full Schema
from el_struc_schema.src.schema.mech import Species


class Schema(BaseModel):
    """The final schema, encapsulating all information"""

    plural_species: list[Species]

if __name__ == "__main__":
    schema = Schema.model_json_schema()  # (1)!
    print(json.dumps(schema, indent=2))  # (2)!

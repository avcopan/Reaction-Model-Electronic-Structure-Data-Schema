# RMESS: Reaction Model Electronic Structure Schema

A repository for drafting a schema for reaction model electronic structure data.

## Installing dependencies

If you have a preferred method of creating python environments, you can use the
`pyproject.toml` file to do so.
Otherwise, an easy way to create and activate a virtual environment is through
[Pixi](https://pixi.sh/latest/):
1. Install Pixi: `curl -fsSL https://pixi.sh/install.sh | bash`
2. Create virtual environment: `pixi install` (in this directory)
3. Activate virtual environment: `pixi shell` (in this directory)

## Running the example

To test that your environment is working, you can run the example script:
```
python example.py
```

## Editing the schema

You can edit the schema in `src/rmess/schema.py`. If you wish to sketch out an
alternative idea rather than editing, you can simply create another file in this
directory.

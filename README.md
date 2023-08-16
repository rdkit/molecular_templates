# Molecular templates for RDKit

This repository manages the templates for ring systems used for 2D coordinate generation in RDKit.

## How to contribute

**PLEASE DO NOT MODIFY template_smiles.h DIRECTLY**, it will be automatically updated once your PR is merged.

To contribute (one or more) ring system templates, you should do the following:

1. Fork and clone this repository.
2. Export your template(s) as CXSMILES.
3. Add your templates to the `templates.smi` file in this repository. Add one CXSMILES per line, and please do not insert any blank lines.
4. Commit and push your changes to your forked repository.
5. Open a Pull Request against rdkit/molecular_templates in GitHub.

Once you have done this, some automated tests will run on your templates. We will review them, and eventually merge them into the repository, and they will eventually be merged into RDKit.

## Requisites for new templates

Please make sure that the templates you contribute follow these guidelines:

- Make sure that the CXSMILES for the template can be parsed by RDKit.
- Make sure that the "CX" extension of your template only includes the atom coordinates.
- Please include a single set of 2D coordinates.
- Your templates should represent a single molecule.
- Each template should must consist of exactly one ring system.
- Please do not submit duplicates for existing templates.

## Current templates Gallery

You can check how the current templates look like in the [Gallery](gallery.md).

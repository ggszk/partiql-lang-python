# PartiQL Lang Python

## Overview

* (Partial) Python implementation of the PariQL specification.
* AST spec: https://github.com/partiql/partiql-lang-kotlin/blob/master/docs/dev/README-AST-V0.md
* We partly use this specification.
* Sorry for using deprecated specification for simple implementation (current version is V1)

## Implemented

* Parse PartiQL Query and produce AST

## Restriction

* Query keyword (SELECT, FROM, ...) must be capitalized.
* Numbers in condition must be integer (don't support float).
* and many...

## Usage

* Please check example.py
* Passed samples of PartiQL, AST are in test_pariql.py
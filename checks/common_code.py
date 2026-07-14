def load_templates():
    with open("templates.smi") as f:
        for i, line in enumerate(f, 1):
            cxsmiles = line.strip()
            if not cxsmiles:
                raise ValueError(f"Empty line at line {i} in templates.smi; "
                                 "empty/blank lines are not allowed.")
            smiles = cxsmiles.split('|', 1)[0]
            yield i, smiles, cxsmiles

# Parser for `cubex` files

## `cubex` file format

- `anchor.xml`
    - contains
        - `cnodes`
        - `metrics`
        - `regions`
        - `system_tree_nodes`
            - `locationgroups`
                - `locations`
- `index.0`
    - the `0` stands for the metric ID
    - contains
        - a header
            - "1"
                - a "1" encoded as a 
            - endianness
            - the number of `cnodes` in the `data.0` file
        - a list of `cnode` indices
            - `cnode_indices = [c1, c2, ...]`
- `data.0` 
    - contains
        - a header
        - data for each `cnode_id` in `cnode_indices`
            - contains metric values for all `locations`
            - to retrieve the value of a particular `cnode` with `cnode_id`, and a specific `location_id`
                - get index of `cnode_index` in `cnode_indices`
                    - = the position of the `cnode_id` in `cnode_indices`
                - offset in `data.0`: `cnode_index * num_locations + location_id`
                    - the `locations` all have incrementing `location_ids`
            - Important: the list is sorted!
                - not in the order of the XML 

## Notes

- Requires at least Python version 3.5
    - Contains `typings` as defined in [PEP 484](https://www.python.org/dev/peps/pep-0484/)
- The `cubex` files are `tar` archives
    - :warning:  ... when extracting them and parsing the extracted `0.data` files using the low-level `IndexParser`/`DataParser` directly,
    they will create strange behaviour
        - in the most cases, parsing succeeds but some edge-cases (related to endianness?) create problems

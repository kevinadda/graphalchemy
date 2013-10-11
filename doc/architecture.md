Here are a few words on the way this project is built. We aim to make each component decoupled from the others.

# Client

The client folder contains all the code that is responsible for the basic interaction with the database :
- connection configuration
- session
- transactions
- basic querying

The use of this module alone will allow you to perform raw gremlin queries against the database.

# Model

On top of that, we add a set of components that intend to ensure various tasks related to the mapping of the database to Python objects :
- model definition (Model, Node, Relationship, Property)
- model validation (Validator)
- model creation from a query and Python-to-DB mapping (Mapper, Metadata)

The use of this module will allow you to validate and persist Python objects directly in the database.


# OGM

Eventually, we add the final OGM layer that ensures :
- lazy-loading
- identity-map

The use of this module will allow you to perform relation lazy-loading, object caching, etc...
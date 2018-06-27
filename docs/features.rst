Django Graph API features
=========================

This is a rough guide and not an exhaustive list.

We will update this list as features are added to django-graph-api.

Supported 👍
------------

Operations
^^^^^^^^^^
- queries (reading data: GET)

Types
^^^^^^^^
- objects (nodes)
- relationships (edges)
- scalar fields: bool, int, float, str, id
- enums
- inputs (for arguments)
- lists
- non-null

Querying
^^^^^^^^
- introspection
- arguments
- fragments
- variables
- operation name

Validation
^^^^^^^^^^
- required arguments
- operation uniqueness


Unsupported 🚫
--------------

Operations
^^^^^^^^^^
- mutations (writing data: POST, DELETE, PUT)
- subscriptions (push notifications, websockets)
- directives

Types
^^^^^
- interfaces
- unions
- inputs (for mutations)
- scalar fields: datetime

Querying
^^^^^^^^
- aliases
- pagination

Validation
^^^^^^^^^^
- fragment usage, uniqueness, type, non-cyclical
- argument type
- variable uniqueness, usage, type

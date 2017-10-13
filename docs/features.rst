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

Unsupported 🚫
--------------

Operations
^^^^^^^^^^
- mutations (writing data: POST, DELETE, PUT)
- subscriptions (push notifications, websockets)

Types
^^^^^
- interfaces
- unions
- enums
- non-null
- inputs (for mutations)
- scalar fields: datetime

Querying
^^^^^^^^
- variables
- filtering
- introspection
- aliases
- fragments
- pagination

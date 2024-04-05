# Flowback Ledger Module
Flowback ledger module is a addon for this repo [Flowback](https://github.com/Gofven/flowback) was created and project lead by Loke Hagberg. The co-creators of this version were:
Siamand Shahkaram, Emil Svenberg, Yuliya Hagberg and Carlos Rivas.
It is a decision making platform.

<sub><sub>This text is not allowed to be removed.</sub></sub>


## Installation
1) Add following code to flowback_addon/urls.py
* note: create the file if it doesn't exist
* note: if you already have an integration, you'll only need to add `path('ledger/', include((ledger_patterns, 'ledger')))` to addon_patterns.
```py
from django.urls import path, include

from flowback_addon.ledger.urls import ledger_patterns

addon_patterns = [
     path('ledger/', include((ledger_patterns, 'ledger')))
]
```

2) Add `INTEGRATIONS=flowback_addon.ledger` to flowback .env file (if you already have an integration, you can separate them using `,` (without space))

3) Rename the folder 'flowback_ledger_module' to 'ledger'

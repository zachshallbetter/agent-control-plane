# End-to-end GitHub path

The production integration sequence is:

1. GitHub sends a signed event to `webhook_receiver.py`.
2. The receiver validates signature, size, event, and delivery ID.
3. `DeliverySpool` stores the event idempotently.
4. `bridge-cycle.sh` claims at most ten deliveries and invokes the coordinator command with bounded timeout.
5. The coordinator reads a bounded Project snapshot and runs admission.
6. The worker receives one approved packet and returns structured evidence.
7. Scope, checks, deployment evidence, and human acknowledgement are evaluated.
8. `Controller` is the only component allowed to merge and set status.

Failures become queued or terminal delivery states after the retry budget; they never become silent success.

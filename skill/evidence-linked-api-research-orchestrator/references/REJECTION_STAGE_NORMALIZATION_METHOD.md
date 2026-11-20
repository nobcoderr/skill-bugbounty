# Rejection-Stage Normalization Method

## Why

Large API platforms often apply a sequence of routing, protocol, credential,
visibility, authorization, and application checks. Raw status codes rarely
identify which gate rejected a request. Normalize only after controlled
experiments establish target-specific semantics.

## Calibration matrix

For one harmless known method, vary one factor at a time:

- nonexistent method versus existing method;
- accepted versus wrong content type;
- missing versus invalid versus authorized test credential;
- permitted versus deliberately mismatched owned auth configuration;
- owned allowed versus owned denied object;
- valid versus invalid typed parameter.

Do not test bypasses, stolen credentials, or third-party objects. Stop when the
next stage is identified well enough to choose a safe probe.

## Stage record

```text
STAGE_ID=
OBSERVED_RESPONSE_CLASS=
CONTROL_OPERATION_IDS=
SINGLE_CHANGED_FACTOR=
EARLIEST_PROVEN_STAGE=
ALTERNATE_EXPLANATIONS=
CONFIDENCE=<HIGH|MEDIUM|LOW>
FALSIFIER=
```

Suggested neutral stage labels:

- `ROUTING_OR_METHOD_RESOLUTION`
- `TRANSCODING_OR_CONTENT_TYPE`
- `CALLER_REGISTRATION_OR_API_ENABLEMENT`
- `CREDENTIAL_RESTRICTION`
- `AUTHENTICATION`
- `ORIGIN_OR_CLIENT_POLICY`
- `VISIBILITY_OR_FEATURE_GATE`
- `RESOURCE_AUTHORIZATION`
- `APPLICATION_VALIDATION`
- `APPLICATION_PROCESSING`
- `STAGE_AMBIGUOUS`

These labels are not a universal provider pipeline. Reorder, merge, or omit
them based on measured evidence.

## Use

The stage guides the next minimal test and prevents wasting calls on a gate not
yet passed. It is not vulnerability evidence. A method reaching application
processing still needs an unauthorized protected effect, capability delta,
control, and replay.

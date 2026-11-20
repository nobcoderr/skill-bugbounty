# GTM evidence schema

Gunakan satu record untuk setiap item hasil ekstraksi.

```text
SOURCE_ASSET=
SCOPE_SNAPSHOT=
HTML_CAPTURED_AT=
GTM_ID=
GTM_JS_URL=
GTM_JS_SHA256=
ITEM_TYPE=HOST|URL|API_ROUTE|AUTH_URL|WEBHOOK|CONFIG|DATALAYER|SENSITIVE_STRING
VALUE=
LOCAL_CONTEXT=
SCOPE_STATUS=IN_SCOPE|OUT_OF_SCOPE|UNKNOWN
OBSERVATION_STATUS=REFERENCE_ONLY|OBSERVED_IN_APP|LIVE_CONFIRMED
AUTH_CONTEXT=
THIRD_PARTY=YES|NO|UNKNOWN
CANDIDATE_STATE=HYPOTHESIS_QUARANTINED|KILLED
FALSIFIABLE_QUESTION=
KILL_OBSERVATION=
NEXT_SAFE_ACTION=
```

`LIVE_CONFIRMED` hanya boleh dipakai setelah parent campaign memverifikasi
scope dan melakukan observasi yang diizinkan. Jangan menyalin token atau nilai
sensitif penuh ke ringkasan; simpan hash atau bentuk teredaksi dan pertahankan
raw evidence pada penyimpanan kampanye yang dibatasi.

{{ config(materialized='table') }}

WITH members AS (
    SELECT * FROM {{ ref('stg_members') }}
),
claims AS (
    SELECT * FROM {{ ref('stg_claims') }}
)
SELECT 
    m.member_id,
    m.first_name || ' ' || m.last_name AS member_name,
    'BPD' AS measure_code,
    'UNCLOSED_GAP_NEEDS_CLINICAL_EXT' AS gap_status
FROM members m
JOIN claims c ON m.member_id = c.member_id
WHERE c.code = 'E11.9'
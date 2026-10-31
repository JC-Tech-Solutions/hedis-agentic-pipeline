SELECT 
    member_id,
    claim_id,
    CAST(service_date AS DATE) AS service_date,
    code_type,
    code,
    description
FROM {{ ref('raw_claims') }}
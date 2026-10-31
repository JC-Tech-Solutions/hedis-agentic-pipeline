SELECT 
    member_id,
    first_name,
    last_name,
    CAST(dob AS DATE) AS dob,
    gender
FROM {{ ref('raw_members') }}
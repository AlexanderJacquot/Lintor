WITH EMPLOYEE_ANNUAL AS (
    SELECT *
    FROM {{ ref('dm_helpers_employee_by_month') }}
    QUALIFY
        ROW_NUMBER() OVER (
            PARTITION BY employee_id, EXTRACT(YEAR FROM effective_date)
            ORDER BY effective_date DESC
        ) = 1
),

GEOGRAPHIC AS (
    SELECT *
    FROM {{ source('datalake', 'talent_connect_career_aspiration_geographic_availability_v2') }}
    QUALIFY
        RANK() OVER (
            PARTITION BY user_id, mobilityArea_code, mobilityArea_name, region_code, region_name, number
            ORDER BY export_datetime DESC
        ) = 1
)

SELECT
    EMPLOYEE_ANNUAL.effective_date,
    GEOGRAPHIC.user_id AS employee_id,
    GEOGRAPHIC.mobilityArea_code,
    GEOGRAPHIC.mobilityArea_name,
    CASE
        WHEN
            GEOGRAPHIC.region_code = ''
            THEN GEOGRAPHIC.mobilityArea_code
        ELSE GEOGRAPHIC.region_code
    END AS region_code,
    CASE
        WHEN
            GEOGRAPHIC.region_code = ''
            THEN GEOGRAPHIC.mobilityArea_name
        ELSE GEOGRAPHIC.region_name
    END AS region_name,
    GEOGRAPHIC.description,
    GEOGRAPHIC.number,
    GEOGRAPHIC.last_modified_date,
    EMPLOYEE_ANNUAL.age,
    EMPLOYEE_ANNUAL.employee_status,
    EMPLOYEE_ANNUAL.business_category_surrogate_key,
    EMPLOYEE_ANNUAL.contract_type_surrogate_key,
    EMPLOYEE_ANNUAL.function_surrogate_key,
    EMPLOYEE_ANNUAL.gender_surrogate_key,
    EMPLOYEE_ANNUAL.geography_surrogate_key,
    EMPLOYEE_ANNUAL.organization_surrogate_key,
    EMPLOYEE_ANNUAL.professional_category_surrogate_key,
    EMPLOYEE_ANNUAL.career_key AS fact_key,
    EMPLOYEE_ANNUAL.encrypted_employee_id_key
FROM EMPLOYEE_ANNUAL
INNER JOIN GEOGRAPHIC
    ON
        GEOGRAPHIC.user_id = EMPLOYEE_ANNUAL.employee_id
        AND EMPLOYEE_ANNUAL.effective_date >= CAST(GEOGRAPHIC.export_datetime AS DATE)
WHERE
    professional_category_surrogate_key IN
    (
        SELECT surrogate_key FROM {{ ref('dm_ref_professional_category') }}
        WHERE
            professional_category_name IN
            ('Production Workers', 'Executives & Managers', 'Administrative & Sales Employees', 'Technicians & Supervisors')
            AND contract_type_name IN ('Permanent', 'Fixed_term', 'Fixed contract', 'Fixed-term')
    )

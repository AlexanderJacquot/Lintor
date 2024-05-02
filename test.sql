SELECT
    dim_users.lb_country,
    dim_users.lb_function,
    dim_template_master.lb_template_master,
    fpe_courses_stats.lb_id_course
    MAX(fpe_courses_stats.ts_completed_at) AS ts_completed_at,
    SUM(
        CASE
            WHEN
                    flag_first_assessment IS true
                AND nb_progress_user >= 76
                AND nb_progress_user <= 100
                THEN fpe_courses_stats.nb_attempts_score
        END
    ) AS first_assess_score,
    COUNT(
        CASE
            WHEN
                flag_first_assessment IS true
                AND nb_progress_user >= 76
                AND nb_progress_user <= 100
                THEN fpe_courses_stats.lb_id_user
        END
    ) AS nb_first_assess_score,
    SUM(
        CASE
            WHEN
                flag_final_assessment IS true
                AND nb_progress_user >= 76
                AND nb_progress_user <= 100
                THEN fpe_courses_stats.nb_attempts_score
        END
    ) AS final_assess_score,
    COUNT(
        CASE
            WHEN
                flag_final_assessment IS true
                AND nb_progress_user >= 76
                AND nb_progress_user <= 100
                THEN fpe_courses_stats.lb_id_user
        END
    ) AS nb_final_assess_score,
    AVG(fpe_courses_stats.nb_attempts_progress) AS module_progression,
    AVG(
        CASE
            WHEN
                fpe_courses_stats.nb_attempts_progress >= 76
                THEN fpe_courses_stats.nb_attempts_global_time
        END
    ) AS module_average_time,
    AVG(fpe_courses_stats.nb_attempts_score) AS module_average_score
FROM TABLE AS fpe_courses_stats
LEFT JOIN TABLE AS dim_courses
    ON fpe_courses_stats.lb_id_course = dim_courses.lb_id_course
WHERE fpe_courses_stats.lb_id_course IS NOT NULL
GROUP BY
    dim_users.lb_country,
    dim_users.lb_function,
    dim_template_master.lb_template_master,
    fpe_courses_stats.lb_id_course
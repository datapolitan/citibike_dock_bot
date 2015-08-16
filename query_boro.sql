WITH boro AS (
SELECT id, boroname AS boro
FROM public.dock_location d
LEFT OUTER JOIN public.nyc_boro b
    ON ST_CONTAINS(b.geom,d.geom)
)
-- , prep AS (
SELECT id,
    CASE WHEN boro IS NULL THEN
        'New Jersey'
    ELSE boro
    END
FROM boro
ORDER BY id
-- )
-- SELECT boro, COUNT(boro) FROM prep GROUP BY boro
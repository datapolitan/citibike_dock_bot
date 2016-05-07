--A query to join the ids on the boros and return the result

WITH boro AS (
SELECT id, boroname AS boro
FROM citibikedock.dock_location d
LEFT OUTER JOIN citibikedock.nyc_boro b
    ON ST_CONTAINS(b.geom,d.geom)
)

SELECT id,
    CASE WHEN boro IS NULL THEN
        'New Jersey'
    ELSE boro
    END
FROM boro
ORDER BY id

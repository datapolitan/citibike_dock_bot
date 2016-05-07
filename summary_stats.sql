--A script to calculate summary statistics for the past 12 hours

WITH hour_ex AS (
    SELECT 
        extract(hour from execution_time) as hour_ex, 
        nyc_avail_bikes,
        mhtn_avail_bikes,
        brklyn_avail_bikes,
        qns_avail_bikes
    FROM citibikedock.cb_boro_stats
    --account for the 4 hours for UTC
    WHERE execution_time >= now() - interval '28 hours' 
    )

SELECT 
    hour_ex,
    ROUND(AVG(nyc_avail_bikes),0) AS nyc,
    ROUND(AVG(mhtn_avail_bikes),0) AS manhattan,
    ROUND(AVG(brklyn_avail_bikes),0) AS brooklyn,
    ROUND(AVG(qns_avail_bikes),0) AS queens
FROM hour_ex
GROUP BY hour_ex
ORDER BY hour_ex 

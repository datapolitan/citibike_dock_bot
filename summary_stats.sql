with hour_ex AS (
    SELECT 
        extract(hour from execution_time) as hour_ex, 
        nyc_avail_bikes,
        mhtn_avail_bikes,
        brklyn_avail_bikes,
        qns_avail_bikes
    FROM public.cb_boro_stats
    WHERE execution_time >= NOW()::date - '1 day'::INTERVAL
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

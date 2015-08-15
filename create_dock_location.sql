DROP TABLE IF EXISTS public.dock_location;

CREATE TABLE public.dock_location (
    id int,
    latitude numeric,
    longitude numeric,
    geom geometry
    );
DROP TABLE IF EXISTS citibikedock.dock_location;

CREATE TABLE citibikedock.dock_location (
    id int,
    latitude numeric,
    longitude numeric,
    geom geometry
    );
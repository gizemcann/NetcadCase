WITH ankara_cankaya AS (
    SELECT
        39.9334 AS center_lat, 32.8597 AS center_lon -- Çankaya'nın merkez koordinatları
)
SELECT
    *,
    -- Merkeze olan uzaklığı haversine formülü ile hesapla
    6371 * acos(
        cos(radians(ankara_cankaya.center_lat)) *
        cos(radians(split_part(loc, ',', 1)::numeric)) *
        cos(radians(split_part(loc, ',', 2)::numeric) - radians(ankara_cankaya.center_lon)) +
        sin(radians(ankara_cankaya.center_lat)) * sin(radians(split_part(loc, ',', 1)::numeric))
    ) AS distance_to_center_km
FROM
    pharmaciess,
    ankara_cankaya
ORDER BY
    distance_to_center_km;



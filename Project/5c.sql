--39.895529890677054, 32.85406123627972
--39.891974665659134, 32.841726726197855
--39.96048921855266, 32.81581416852985
--39.902884397819015, 32.86023896852803
--39.91897491338078, 32.85624068202247

--Başvuran Kişi verilerinin Nöbetçi Eczanelere olan uzaklıkları hesaplanmalıdır

ALTER TABLE basvuru_noktaları
ADD COLUMN location text;

	
UPDATE basvuru_noktaları
SET location = CASE
    WHEN basvuru_numarasi = 1 THEN '39.895529890677054, 32.85406123627972'
    WHEN basvuru_numarasi = 2 THEN '39.891974665659134, 32.841726726197855'
    WHEN basvuru_numarasi = 3 THEN '39.96048921855266, 32.81581416852985'
    WHEN basvuru_numarasi = 4 THEN '39.902884397819015, 32.86023896852803'
    WHEN basvuru_numarasi = 5 THEN '39.91897491338078, 32.85624068202247'
    ELSE location
END;




SELECT
    basvuru_noktaları.adresi AS person_address,
    pharmaciess.address AS eczane_address,
    6371 * acos(
        cos(radians(CAST(SUBSTRING(basvuru_noktaları.location FROM '^(.*),') AS numeric))) *
        cos(radians(CAST(SUBSTRING(pharmaciess.loc FROM '^(.*),') AS numeric))) *
        cos(radians(CAST(SUBSTRING(pharmaciess.loc FROM ',(.*)$') AS numeric)) - radians(CAST(SUBSTRING(basvuru_noktaları.location FROM ',(.*)$') AS numeric))) +
        sin(radians(CAST(SUBSTRING(basvuru_noktaları.location FROM '^(.*),') AS numeric))) * sin(radians(CAST(SUBSTRING(pharmaciess.loc FROM '^(.*),') AS numeric)))
    ) AS distance_km
FROM
    basvuru_noktaları
CROSS JOIN
    pharmaciess;




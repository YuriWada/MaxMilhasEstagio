SELECT
  bi.from_iata AS aeroporto_origem,
  bi.to_iata AS aeroporto_destino,
  SUM(bi.valor_passagem) AS valor_total_gasto,
  AVG(CASE WHEN bi.milhas_usadas > 0 THEN bi.milhas_usadas ELSE NULL END) AS media_milhas_utilizadas
FROM
  BaseItens AS bi
INNER JOIN
  BaseAeroporto AS ba ON bi.from_iata = ba.from_iata AND bi.to_iata = ba.to_iata
WHERE
  ba.is_mercosul = 1
  AND bi.status_id <> 2
  AND bi.data_compra BETWEEN "2019-11-01" AND "2020-01-31"
GROUP BY
  bi.from_iata
  bi.to_iata
ORDER BY
  valor_total_gasto DESC;

  

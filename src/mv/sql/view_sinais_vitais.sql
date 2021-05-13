WITH 
    V_LEITURAS_SINAIS_VITAIS AS (
        select coleta.cd_coleta_sinal_vital,
            to_char(coleta.data_coleta, 'DD/MM/YYYY HH24:MI') hora,
            to_char(coleta.data_coleta, 'DD/MM/YYYY') DT,
            to_char(coleta.data_coleta, 'YYYY') ANO,
            to_char(coleta.data_coleta, 'DD') DIA,
            to_char(coleta.data_coleta, 'MM') MES,
            TO_CHAR(COLETA.DATA_COLETA, 'HH24:MI') HR,
            coleta.cd_atendimento,
            coleta.cd_prestador,
            prestador.nm_prestador,
            it.cd_sinal_vital,
            sinal_vital.ds_sinal_vital,
            it.valor,
            CONCAT(CONCAT(REGEXP_SUBSTR(prestador.nm_prestador,'[^ ]+', 1, 1),' '),REGEXP_SUBSTR(prestador.nm_prestador, '[^ ]+', 1, 2)) NOME
        from DBAMV.COLETA_SINAL_VITAL coleta,
            dbamv.itcoleta_sinal_vital it,
            dbamv.sinal_vital,
            dbamv.prestador
        where 
                coleta.cd_coleta_sinal_vital = it.cd_coleta_sinal_vital
            and sinal_vital.cd_sinal_vital = it.cd_sinal_vital
            and prestador.cd_prestador(+) = coleta.cd_prestador
            AND coleta.CD_MULTI_EMPRESA = {cd_multi_empresa}
    ),
  ULTIMAS_LEITURAS AS
  (
    SELECT
      V_LEITURAS_SINAIS_VITAIS.CD_ATENDIMENTO,
      MAX(V_LEITURAS_SINAIS_VITAIS.CD_COLETA_SINAL_VITAL) CD_ULTIMA_LEITURA
    FROM V_LEITURAS_SINAIS_VITAIS
    INNER JOIN ATENDIME ON  ATENDIME.CD_ATENDIMENTO = V_LEITURAS_SINAIS_VITAIS.CD_ATENDIMENTO
                            AND ATENDIME.TP_ATENDIMENTO = 'I'
                            AND ATENDIME.DT_ALTA IS NULL
                            AND ATENDIME.CD_MULTI_EMPRESA = {cd_multi_empresa}
    GROUP BY V_LEITURAS_SINAIS_VITAIS.CD_ATENDIMENTO
  )
  , LEITURAS AS 
  (
      SELECT 
        VDIC_REGISTRO_SINAL_VITAL.CD_ATENDIMENTO
        , UNID_INT.CD_UNID_INT
        , UNID_INT.DS_UNID_INT
        , ATENDIME.CD_LEITO
        , LEITO.DS_RESUMO AS DS_LEITO
        , VDIC_REGISTRO_SINAL_VITAL.CD_COLETA_SINAL_VITAL
        , VDIC_REGISTRO_SINAL_VITAL.HORA DT_COLETA
        , VDIC_REGISTRO_SINAL_VITAL.CD_SINAL_VITAL
        , VDIC_REGISTRO_SINAL_VITAL.DS_SINAL_VITAL
        , VDIC_REGISTRO_SINAL_VITAL.VALOR
        , TO_CHAR(ATENDIME.DT_ATENDIMENTO, 'DD/MM/YYYY') || ' ' || TO_CHAR(ATENDIME.HR_ATENDIMENTO, 'HH24:MI:SS') DT_ATENDIMENTO
        , ATENDIME.TP_ATENDIMENTO
        , ATENDIME.CD_CID
      FROM ULTIMAS_LEITURAS
      INNER JOIN VDIC_REGISTRO_SINAL_VITAL ON 
            VDIC_REGISTRO_SINAL_VITAL.CD_ATENDIMENTO = ULTIMAS_LEITURAS.CD_ATENDIMENTO
        AND VDIC_REGISTRO_SINAL_VITAL.CD_COLETA_SINAL_VITAL = ULTIMAS_LEITURAS.CD_ULTIMA_LEITURA
      INNER JOIN ATENDIME ON  
            ATENDIME.CD_ATENDIMENTO = VDIC_REGISTRO_SINAL_VITAL.CD_ATENDIMENTO
        AND ATENDIME.TP_ATENDIMENTO = 'I'
        AND ATENDIME.DT_ALTA IS NULL
      INNER JOIN LEITO ON 
            LEITO.CD_LEITO = ATENDIME.CD_LEITO 
        AND LEITO.DT_DESATIVACAO IS NULL
      INNER JOIN UNID_INT ON 
            UNID_INT.CD_UNID_INT = LEITO.CD_UNID_INT
      ORDER BY  
          UNID_INT.CD_UNID_INT, 
          ATENDIME.CD_LEITO
  )
  SELECT
    *
  FROM LEITURAS
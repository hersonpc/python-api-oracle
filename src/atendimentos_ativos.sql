select 
    cd_atendimento
    , dt_atendimento
    , hr_atendimento
    , cd_paciente
    , cd_leito
    , cd_cid
from atendime
where 
    dt_alta is null 
    and dt_atendimento >= '01/01/2020' 
    and tp_atendimento = 'I'
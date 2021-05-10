select * from unid_int
inner join setor on setor.cd_setor = unid_int.cd_setor
where
  setor.cd_multi_empresa = {cd_multi_empresa}
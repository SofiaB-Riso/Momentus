# Backend Momentus

API e servidor de arquivos do frontend em Flask/SQLAlchemy. Para instalação e configuração do banco, consulte o [README principal](../README.md).

## Fluxo

`Controller → Service → Model/Repository`. O controller obtém a identidade e o caso de uso por `controllers/contexto.py`. `controllers/respostas.py` converte resultados/exceções em HTTP. Serviços não importam Flask: recebem a transação e as dependências escolhidas em `application/composicao.py`.

`CasoUso.exigir_acesso_evento()` valida existência e permissão antes das operações. A consulta de acesso sem exceção continua disponível para encerrar SSE quando a permissão é revogada. A transação agrupa dados, histórico e notificações; arquivos usam limpeza após confirmação ou rollback.

`Evento.total_despesas_decimal` centraliza o total exato de itens e despesas. A serialização e o resumo financeiro usam esse mesmo cálculo; as estratégias de rateio distribuem centavos no servidor.

## Persistência

O SQLite relativo usa `backend/instance`, definido explicitamente na fábrica da aplicação. O banco incluído está vazio, com 16 tabelas. `DATABASE_URL` pode escolher outro arquivo ou MySQL/MariaDB; o SQL de instalação está em `database/create_database.sql`. Não há carga automática de usuários de demonstração.

Uploads usam `UPLOAD_FOLDER`, com padrão em `backend/uploads`. O modelo é criado por `create_all()` na inicialização; alterações de esquema em uma instalação existente exigem migração própria.

## Contratos da API

- Sessões: login/cadastro vinculam o cookie ao cadastro persistido. Cookies antigos ou de outra identidade são recusados com HTTP 401.
- `tipo_evento`: até 100 caracteres, incluindo o texto personalizado de Outro.
- `hora_evento`: opcional; formato HH:MM entre 00:00 e 23:59. Vazio/null remove o horário; omitir o campo na alteração preserva o valor.
- Orçamento: de zero a R$ 99.999.999,99, com centavos.
- `GET /catalogo/perto?paginado=1`: recebe categoria, q, cidade ou lat/lng e, nas páginas seguintes, pagina. Responde `{"fornecedores": [...], "proxima_pagina": "token ou null"}`. Sem paginado=1, mantém a resposta em lista usada pelo Início.
- `categoria=melhores`: exige nota > 4 e mais de 200 avaliações. As demais categorias ordenam por proximidade quando há coordenadas.
- `GET /catalogo/foto`: proxy legado mantido por compatibilidade; a interface atual não o chama.
- Convites de convidados usam `/rsvp/<token>`; convites de colaboração usam `/colaboracoes/<token>`. O aceite de colaboração exige login na conta correspondente.
- O dono define permissões por evento; convidados públicos não recebem acesso administrativo. Atualizações ao vivo usam SSE.

Os caminhos e métodos das 63 regras HTTP existentes foram preservados. [IMPLEMENTACAO.md](../IMPLEMENTACAO.md) indica os recursos e seus arquivos.

## Verificação

Na pasta backend, execute `py -m unittest discover -s tests -v` no Windows, ou use python3 no Linux/macOS. As chamadas do Google e os bancos de testes são isolados. Resultados e limites estão em [RESULTADO_TESTES.md](../RESULTADO_TESTES.md).

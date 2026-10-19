# Validação da limpeza do código

Revisão de 19/10/2026, usando como base a entrega com bancos zerados.

## Alterações

- Construção dos casos de uso centralizada em `controllers/contexto.py`, mantendo autenticação e rotas.
- Validação comum de acesso em `CasoUso.exigir_acesso_evento`, sem aliases ou retornos de erro inalcançáveis. O streaming continua encerrando ao perder permissão.
- Total de itens e despesas centralizado em `Evento.total_despesas_decimal`, reutilizado pela serialização e pelo resumo/rateio financeiro.
- Escape de HTML/atributos, estrelas e datas compartilhados por `frontend/js/utils.js`.
- GPS, cidade digitada, cache e descarte de localização atrasada compartilhados em `localizacao-momentus.js`.
- Dezesseis arquivos de ícones laterais substituídos por oito variantes únicas, preservando exatamente os bytes usados em cada página. Funções sem consumidores e estilos da tela de fornecedor descontinuada foram removidos.
- CSS expandido para leitura; as 650 regras restantes são equivalentes às da versão limpa antes da formatação, comparadas pelo parser do Chromium, desconsiderando apenas espaços de indentação.
- SQLite padrão fixado em `backend/instance`, sem pasta instance duplicada na raiz. Banco entregue vazio e esquema preservado.
- READMEs e documentos consolidados; retiradas instruções históricas que contradiziam a versão atual.

## Verificações executadas

| Verificação | Resultado |
|---|---|
| Suíte backend | **69 testes aprovados** com SQLite temporário e integrações simuladas |
| Regressões acrescentadas | Caminho SQLite relativo, configuração absoluta e totais financeiros exatos antes/depois de remover itens |
| Ruff E4/E7/E9/F/I e formatação Python | Aprovados |
| Consistência das dependências | `pip check` aprovado |
| Sintaxe | 131 arquivos Python e 14 JavaScripts válidos |
| Compatibilidade HTTP | As 63 regras de rota e seus métodos permanecem iguais à base |
| Referências HTML | Arquivos locais existem; imagens preservam os bytes da base após a unificação de caminhos |
| Arquivos do frontend por HTTP | 36 arquivos servidos com conteúdo correto |
| Banco de entrega | Um SQLite, 16 tabelas, zero registros, integrity_check e foreign_key_check aprovados |
| ZIP | Sem venv, caches, .env, chave Google real ou cópias dos bancos anteriores |

A suíte cobre autenticação, identidade da sessão, permissões, CRUD, colaboração, RSVP, concorrência de reserva, rateio com centavos, tarefas, lembretes, notificações, uploads e sua limpeza, rollback, relatórios, contratos, arquitetura e catálogo paginado.

## Interface em Chromium

- Comparação de 38 capturas entre antes/depois, nas larguras 1366 e 390 px: login, cadastro, Início, planejamento, catálogo claro/escuro, eventos, configurações, convite, RSVP e nove abas do evento. As diferenças observadas ficaram em horários, contadores e estados transitórios de animação; componentes e ícones foram preservados. Sem erros de JavaScript ou arquivos faltando nesses percursos.
- Fluxos nas duas larguras: GPS preciso, cidade pelo Enter, permissão negada, cache, resposta atrasada descartada, tipo Outro, orçamento de R$ 25.000,37, relógio 19:37, rascunho fora dos ativos, finalização do mesmo evento e ingresso com prévia/rasgo.
- Texto com sinais de HTML, aspas e & continua aparecendo como texto, sem gerar elementos na renderização do evento.
- Catálogo: 20 → 40 → 60 → restante final, filtros estritos, deduplicação, candidatos reservados, fim da fonte, cursor repetido, falha/nova tentativa e reinício por busca. Mantidas capas coloridas e links de Street View.
- Cookie antigo pede novo login; entrada explícita e recarga conservam a conta correta.

## Limites

Google, GPS e dados de usuários foram simulados. Não houve chamada com chave real nem acesso a banco externo. MySQL/MariaDB e cobertura real de Street View não foram revalidados nesta limpeza; o SQL de instalação foi preservado. Os testes verificam os cenários descritos, sem cobrir todas as combinações possíveis de navegador e entrada.

Para repetir a suíte, na pasta backend execute `py -m unittest discover -s tests -v` no Windows ou use python3 no Linux/macOS. Os bancos de teste são temporários; o banco incluído no ZIP continua sem cadastros.

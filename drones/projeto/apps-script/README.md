# Drones — master do projeto e preparação para Google Apps Script

## Responsabilidades

| Componente | Local | Acesso |
|---|---|---|
| Código mestre, páginas públicas, documentação e catálogo das aulas | GitHub do professor | Público, sem segredos ou dados de participantes |
| Vídeos publicados e playlist | Canal YouTube do professor | Preservar os identificadores existentes |
| Aplicação de cadastro, prova e coordenação | Google Apps Script | Acesso por identidade e função; ainda em adaptação |
| Registros, documentos ANAC, certificados individuais e backups | Google Drive e planilhas do professor | Privado, acesso controlado |
| Banco real de questões, gabaritos e configurações de autorização | Área privada no Google | Somente o servidor e instrutores autorizados |

Os MP4 guardados no Drive são cópias de preservação. O YouTube permanece como serviço de publicação dos vídeos. As estatísticas do canal medem audiência; a conclusão individual de aulas precisa de registros da aplicação. Eventos do player não demonstram atenção humana e não constituem prova inviolável de presença.

## Estado desta entrega

`Code.gs` prepara uma estrutura privada de dados e uma página de diagnóstico restrita ao proprietário. Não implementa ainda a autenticação dos participantes, o acompanhamento pelo player, a prova, o upload documental ou a emissão. Esses recursos continuam no ambiente anterior até que a migração funcional seja desenvolvida, testada e validada. Não apontar os links de produção para este projeto de preparação.

Não foi migrado nenhum cadastro ou resultado real. A autorização OAuth foi concluída e a inicialização foi executada com sucesso. As oito tabelas foram criadas na planilha privada do curso, na pasta do professor. A privacidade e as regras iniciais foram conferidas. Nenhuma inscrição, resultado, documento pessoal ou certificado individual foi migrado nesta etapa.

## Preparação

1. Criar um projeto Apps Script privado e copiar `Code.gs`.
2. Nas propriedades do script, configurar `OWNER_EMAIL` com a identidade Google do proprietário e `COURSE_FOLDER_ID` com a pasta privada do curso. Não gravar esses valores no repositório.
3. Revisar a tela de permissões do Google antes de executar `setupProject`.
4. Executar `setupProject` no editor. A função é idempotente e preserva linhas existentes; uma estrutura incompatível interrompe a operação.
5. Não compartilhar a planilha de registros nem os documentos pessoais com o público.

## Segurança da migração funcional

- A autenticação docente não pode confiar em e-mail informado pelo visitante. `Session.getActiveUser()` pode não identificar visitantes externos em uma aplicação executada como proprietário. A escolha da autenticação precisa ser validada antes da publicação.
- Validar a identidade, a função e a titularidade no servidor em todas as operações.
- Gabaritos e regras de correção permanecem no servidor. O sorteio e a nota final não são determinados pelo navegador.
- Preservar 17 conclusões, 20 questões por prova, mínimo de 70%, no máximo três tentativas na mesma janela de duas horas e bloqueio de novas tentativas após aprovação.
- Usar o relógio do servidor para prazos e intervalos de reprodução; tratar concorrência e repetição de solicitações.
- A conclusão no YouTube isoladamente não libera a prova da aplicação.
- Documentos e certificados individuais ficam privados. Usar acesso autenticado para os downloads.
- Configurações de emissão, carga horária e autorização institucional são independentes da publicação do código.
- Não versionar senhas, tokens, arquivos de credenciais do clasp, documentos pessoais, resultados, IDs de arquivos privados ou backups da base. Um repositório privado também não é lugar para credenciais.
- Avaliar cotas de execução e concorrência da conta Google antes da migração; não há garantia de capacidade ilimitada.

## Código mestre

A cópia do GitHub é a referência para alterações de código. Valores de produção ficam nas propriedades do script. Mudanças feitas no editor devem ser reconciliadas com o master antes da próxima publicação. Uma automação com `clasp` poderá ser acrescentada separadamente, após revisar suas credenciais e permissões; nenhuma automação de escrita foi criada nesta etapa.

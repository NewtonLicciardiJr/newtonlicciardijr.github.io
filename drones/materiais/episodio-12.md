# 12. Autonomia, IA e o próximo voo

Simular, validar e aprender com falhas antes de ampliar a missão.

Série: **Drones Muito Além do Voo**. Consulta: 09/10/2026. Vídeo em preparação.

Duração: 6–9 min, incluindo demonstração. Papéis: Prof. Newton e professor instrutor.

## Conexão com a apostila

Encontros 10–12 • contingências, operação integrada e debrief

## Objetivos

- Distinguir automação de autonomia.
- Planejar um ensaio seguro em simulação.
- Usar debrief e análise de falhas para produzir aprendizado.

## Leitura de apoio

Uma missão por pontos programados automatiza uma sequência; autonomia inclui adaptar decisões dentro de limites. Em ambos os casos, a confiabilidade precisa ser avaliada. IA pode auxiliar detecção, mas resultados variam com contexto e dados.

O Ingenuity oferece um caso de processamento embarcado e investigação de falha. PX4 e QGroundControl permitem estudar missões em ambiente simulado. A prova de conceito deve explicitar hipótese, condições de teste, resultados e limite do que foi demonstrado.

## Roteiro de gravação

**Prof. Newton:** O próximo passo dos drones envolve autonomia e inteligência embarcada. Mas antes de aumentar a complexidade, precisamos perguntar: como vamos verificar que o sistema responde bem ao que não esperávamos?

**Professor instrutor:** Começamos pela simulação. Com ferramentas compatíveis, podemos observar missões, telemetria e respostas a condições de teste sem colocar uma aeronave real no espaço aéreo.

**Prof. Newton:** Automatizar uma sequência não é o mesmo que adaptar decisões. Se a percepção falhar, o sistema precisa reconhecer sua limitação e responder dentro de condições previstas.

**Professor instrutor:** No exercício, vamos registrar o que esperávamos, o que ocorreu e o que pode ser concluído. Um teste que funciona uma vez não valida todos os cenários.

**Prof. Newton:** O caso do Ingenuity mostra o valor de investigar falhas. A narrativa inicial de um acidente não substitui a análise posterior dos dados. É preciso revisar hipóteses conforme a evidência.

**Professor instrutor:** Também faremos um debrief. Qual etapa consumiu mais tempo? Qual informação faltou? O que seria necessário antes de uma próxima missão? Essas respostas viram melhoria de procedimento.

**Prof. Newton:** Para os engenheirandos, a série pode abrir projetos em sensores, telemetria, controle, visão e sistemas embarcados. O projeto ganha força quando a pergunta é mensurável e a validação é honesta.

**Professor instrutor:** Drones Muito Além do Voo termina aqui como série inicial, mas o material continua disponível para consulta. A ideia é voar com propósito, entregar evidência e aprender com cada missão.

## Demonstração

1. Mostrar a documentação oficial de SITL e QGroundControl.
2. Executar apenas em simulador uma missão simples de referência; registrar a versão usada.
3. Preencher debrief: hipótese, resultado, limitações e próxima verificação.

Prática real: conferir aptidão, local, equipamento e condições autorizadas. Use simulação se não houver condições.

## Atividade

Uma detecção por IA funcionou em dez imagens de um ambiente. Isso comprova desempenho em qualquer local?

## Resposta comentada

Não. É necessário avaliar representatividade, condições de captura, erros e critérios de decisão. Um ensaio restrito sustenta uma conclusão restrita.

## Modelos

- NASA Ingenuity
- DJI Matrice 4T
- Parrot ANAFI Ai

## Fontes

- [NASA • encerramento da missão Ingenuity](https://www.nasa.gov/news-release/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/) — Agência de pesquisa.
- [NASA • investigação do último voo do Ingenuity](https://www.nasa.gov/missions/mars-2020-perseverance/ingenuity-helicopter/nasa-performs-first-aircraft-accident-investigation-on-another-world/) — Agência de pesquisa.
- [PX4 • documentação de simulação](https://docs.px4.io/main/en/simulation/) — Documentação técnica.
- [QGroundControl • guia de uso](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/) — Documentação técnica.
- [Baguer et al. • BVLOS, Open RAN e network slicing](https://arxiv.org/abs/2608.09481) — Preprint.

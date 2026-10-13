# 06. Da câmera ao dado confiável

RGB, térmica, multispectral e LiDAR: cada sensor responde a uma pergunta.

Série: **Drones Muito Além do Voo**. Consulta: 09/10/2026. Vídeo em preparação.

Duração: 6–9 min, incluindo demonstração. Papéis: Prof. Newton e professor instrutor.

## Conexão com a apostila

Encontro 11 • objetivo, coleta e evidência

## Objetivos

- Escolher sensor pela variável observada.
- Distinguir resolução, amostragem e exatidão.
- Conservar metadados e validar resultados.

## Leitura de apoio

RGB registra aparência em bandas visíveis; imagem térmica permite examinar padrões de temperatura aparente; multispectral observa bandas específicas; LiDAR mede distâncias para representar geometria. Essas informações podem se complementar, mas não são intercambiáveis.

Uma medida exige referência, unidade, método e incerteza. GSD é a amostragem no solo em um modelo geométrico; não é o erro final de posição. Preservar data, parâmetros e contexto permite avaliar se uma comparação é válida.

## Roteiro de gravação

**Prof. Newton:** Uma imagem bonita pode ser um dado ruim para uma medida. Hoje vamos trocar a pergunta “qual câmera tem mais pixels?” por “qual variável precisa ser observada?”.

**Professor instrutor:** Eu começo com uma imagem RGB e uma imagem térmica. A primeira mostra aparência; a segunda traz outro tipo de informação. A interpretação muda, e o contexto da captura precisa acompanhar os arquivos.

**Prof. Newton:** LiDAR entra pela geometria. Multispectral entra por bandas específicas. Nenhum sensor transforma sozinho uma observação em diagnóstico. É preciso método e uma verificação adequada.

**Professor instrutor:** Na coleta, também registramos configurações, horário e posição. Se duas campanhas forem feitas em condições incompatíveis, o resultado pode parecer mudança no objeto quando é mudança na aquisição.

**Prof. Newton:** Vamos calcular um GSD com números sintéticos. A fórmula relaciona altura, tamanho do pixel e distância focal. O resultado descreve amostragem e não garante a exatidão do mapa.

**Professor instrutor:** Para validar, precisamos de referências independentes e de critérios. Não basta que o software tenha concluído o processamento e produzido uma imagem convincente.

**Prof. Newton:** Essa é a diferença entre produzir dados e produzir evidência: outra pessoa deve conseguir compreender o método e os limites da conclusão.

**Professor instrutor:** Ao final, cada arquivo será acompanhado de uma pequena ficha. Parece detalhe, mas é o que permite usar a informação depois que o voo terminou.

## Demonstração

1. Mostrar os tipos de sensor com as fichas verificadas do catálogo.
2. Resolver o exemplo de GSD do caso Mapeamento.
3. Organizar três arquivos fictícios com nome, data, contexto e critério de validação.

Prática real: conferir aptidão, local, equipamento e condições autorizadas. Use simulação se não houver condições.

## Atividade

Se o GSD for 2 cm/pixel, posso declarar que todas as coordenadas têm erro de 2 cm?

## Resposta comentada

Não. GSD e exatidão descrevem aspectos distintos. A estimativa do erro exige validação do produto e de seu referencial.

## Modelos

- DJI Mavic 3E
- DJI Mavic 3T
- Flyability Elios 3
- DJI Matrice 400

## Fontes

- [DJI • Mavic 3 Enterprise Series](https://enterprise.dji.com/mavic-3-enterprise) — Fabricante.
- [Flyability • Elios 3](https://www.flyability.com/elios-3) — Fabricante.
- [DJI • Matrice 400](https://enterprise.dji.com/matrice-400) — Fabricante.

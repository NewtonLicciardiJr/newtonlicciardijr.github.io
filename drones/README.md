# Drones Muito Além do Voo

[Abrir o site](https://newtonlicciardijr.github.io/drones/) · [Episódios](https://newtonlicciardijr.github.io/drones/serie.html) · [Materiais](https://newtonlicciardijr.github.io/drones/materiais.html)

Acervo de apoio à série de extensão planejada pelo Prof. Newton Licciardi Jr. e professor instrutor. Base: apostila do curso PI Drones. Autoria original preservada nos PDFs. Consulta das fontes: **09/10/2026**. Vídeos em preparação; esta entrega reúne os materiais e roteiros.

## O que está disponível

- 12 roteiros-base com leitura, demonstração, atividade e resposta.
- 37 slides de apoio aos 12 episódios, em PowerPoint editável com notas e em PDF para consulta e projeção. [Guia e mapa dos slides](materiais/guia-slides.md).
- 17 modelos civis, militares, brasileiros e de pesquisa, com fonte e limite de aplicação.
- 4 casos documentados e 4 cenários didáticos; 8 notícias comentadas de 2024–2026.
- Apostila ampliada, caderno complementar, roteiros em PDF e arquivos editáveis.
- Checklist, ficha de missão, plano de integração, guia de produção, glossário e fontes.

## Estrutura

- `episodios/`: páginas individuais dos episódios.
- `casos/`: estudos individuais e atividades.
- `materiais/`: arquivos Markdown e CSV editáveis.
- `downloads/`: PDFs e pacote ZIP.
- `assets/`: estilo, interação, favicon e imagens com créditos.
- `conteudo.py` / `conteudo.json`: conteúdo editorial estruturado.
- `build.py`: geração reproduzível do site, materiais e PDFs.

## Atualização

1. Editar `conteudo.py` e conferir novamente as fontes.
2. Executar `python conteudo.py` e `python build.py` a partir desta pasta. Requer Python 3, reportlab, pypdf e fontes DejaVu; a regeneração utiliza `downloads/apostila-base.pdf` quando o arquivo original externo não está disponível.
3. Conferir páginas, links, legibilidade dos PDFs e estado dos vídeos antes do commit.
4. Publicar alterações na branch `main`: o GitHub Pages já atende este repositório.

O conteúdo de gravações e seus URLs deve ser acrescentado quando houver vídeos publicados. Não existe atualização automática de notícias nesta edição.

Os slides estão em `downloads/slides-apoio-serie.pptx` e `downloads/slides-apoio-serie.pdf`. O arquivo `materiais/plano-slides.json` conserva o conteúdo estruturado e as notas. O PDF contém as telas exibidas ao público; as notas de apresentação, respostas e referências completas ficam no PowerPoint. A geração do site não recria estes dois arquivos.

## Critérios

Notícias conservam data e fonte. Máximos de fabricante não são autonomia útil nem autorização de voo. Preprints são identificados. A norma aplicável, as condições da autorização e o manual prevalecem. Os exemplos militares são estudos públicos de engenharia e responsabilidade. Este acervo não representa uma autorização de operação, certificação ou publicação institucional formal do Mackenzie.

Foto Ingenuity: NASA/JPL-Caltech/ASU/MSSS, imagem de 02/08/2023 publicada pela NASA em janeiro de 2024. Não há endosso dos fabricantes ou da NASA. Marcas e material de terceiros conservam seus direitos; o acervo usa referências e não republica manuais ou vídeos completos.

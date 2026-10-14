"""Gera site estático, Markdown, PDFs e pacote. Sem dependências de front-end."""
from pathlib import Path
import html, json, shutil, zipfile, re, csv
from conteudo import DATA, ROOT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

E=html.escape
S={s['id']:s for s in DATA['sources']}
M={m['slug']:m for m in DATA['models']}
C={c['slug']:c for c in DATA['cases']}
EP={e['n']:e for e in DATA['episodes']}
NAV=[('index.html','Início'),('serie.html','Episódios'),('modelos.html','Modelos'),('casos.html','Casos'),('noticias.html','Notícias'),('materiais.html','Materiais'),('normas.html','Normas'),('fontes.html','Fontes')]

def write(path,text):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def refs(ids,prefix=''):
    return '<ul>'+''.join(f'<li><a href="{E(S[i]["url"])}" target="_blank" rel="noopener noreferrer">{E(S[i]["title"])}</a> <span class="meta">· {E(S[i]["kind"])}</span></li>' for i in ids)+'</ul>'
def paras(ps):return ''.join('<p>'+E(p)+'</p>' for p in ps)
def items(xs):return '<ul>'+''.join('<li>'+E(x)+'</li>' for x in xs)+'</ul>'
def epfile(e):return f'episodios/{e["n"]:02d}-{e["slug"]}.html'
def casefile(c):return f'casos/{c["slug"]}.html'
def page(path,title,body,active='index.html',deep=False,desc=None):
    pre='../' if deep else ''
    url='https://newtonlicciardijr.github.io/drones/'+('' if path=='index.html' else path)
    nav=''.join(f'<a href="{pre}{p}"'+(' aria-current="page"' if p==active else '')+f'>{n}</a>' for p,n in NAV)
    description=desc or 'Série de vídeos e materiais de extensão: operação, engenharia, aplicações civis e militares, casos e fontes verificadas.'
    published=sum(bool(e.get('video_url')) for e in DATA['episodes'])
    video_status='Série em preparação: roteiros disponíveis; vídeos ainda não publicados.' if not published else f'Série em produção: {published} de 12 episódios com vídeo vinculado.'
    body=f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(title)} | Drones Muito Além do Voo</title><meta name="description" content="{E(description)}"><meta name="author" content="Prof. Newton Licciardi Jr."><meta name="theme-color" content="#111d32"><link rel="canonical" href="{url}"><link rel="icon" type="image/svg+xml" href="{pre}assets/favicon.svg"><link rel="stylesheet" href="{pre}assets/style.css"><script src="{pre}assets/site.js" defer></script></head><body><a class="skip" href="#conteudo">Pular para o conteúdo</a><header class="top"><div class="wrap top-inner"><a class="brand" href="{pre}index.html">DRONES<span>Muito Além do Voo</span></a><a class="home-link" href="/">Prof. Newton Licciardi Jr.</a></div></header><nav class="nav" aria-label="Navegação principal"><div class="wrap nav-inner">{nav}</div></nav><main id="conteudo">{body}</main><footer class="foot"><div class="wrap"><p><strong>Drones Muito Além do Voo</strong> · Material para extensão, parceiros e comunidade.</p><p>Prof. Newton Licciardi Jr. · {E(video_status)}</p><p>Edição 1.0 · Fontes consultadas em 09/10/2026 · <a href="{pre}fontes.html">Fontes e critérios editoriais</a> · <a href="https://github.com/NewtonLicciardiJr/newtonlicciardijr.github.io/tree/main/drones">Arquivos no GitHub</a></p></div></footer></body></html>'''
    write(path,body)
def intro(label,title,desc):return f'<div class="intro wrap"><div class="eyebrow">{E(label)}</div><h1>{E(title)}</h1><p class="lead">{E(desc)}</p></div>'
def epcard(e):return f'<article class="card"><span class="number">EPISÓDIO {e["n"]:02d}</span><h3><a href="{epfile(e)}">{E(e["title"])}</a></h3><p>{E(e["subtitle"])}</p><span class="meta">{E(e["minutes"])}</span><a class="link" href="{epfile(e)}">Ler roteiro e explorar materiais</a></article>'
def casecard(c):return f'<article class="card"><span class="tag {"real" if c["label"]=="Caso documentado" else ""}">{E(c["label"])} · {E(c["area"])}</span><h3><a href="{casefile(c)}">{E(c["title"])}</a></h3><p>{E(c["fact"])}</p><a class="link" href="{casefile(c)}">Explorar o caso</a></article>'

def build_site():
    write('assets/favicon.svg','<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#111d32"/><path d="M9 24V8h6c9 0 9 16 0 16z" fill="none" stroke="#f2c85c" stroke-width="3"/><circle cx="24" cy="8" r="3" fill="#be2c38"/></svg>')
    hero='''<section class="hero"><div class="wrap hero-grid"><div><div class="eyebrow">Tecnologia • engenharia • sociedade</div><h1>Drones<br><em>Muito Além<br>do Voo.</em></h1><p class="lead">Do primeiro comando à informação que transforma uma decisão. Conheça as aplicações, os sistemas e as pessoas por trás de cada missão.</p><div class="actions"><a class="button primary" href="serie.html">Explorar os 12 episódios</a><a class="button secondary" href="materiais.html">Apostilas e materiais</a></div></div><aside class="hero-card"><span class="num">01 / 12</span><h2>O drone é só uma parte do sistema</h2><p>A aeronave voa. O sistema coleta. A missão precisa entregar evidência.</p><a href="episodios/01-muito-alem-do-voo.html">Começar pelo episódio 01</a><p class="meta" style="margin-top:20px;margin-bottom:0">Roteiro disponível · vídeo em preparação</p></aside></div></section>'''
    stats='<div class="wrap stats">'+''.join(f'<div><strong>{n}</strong><span>{s}</span></div>' for n,s in [(12,'episódios'),(17,'modelos reais'),(8,'casos e exercícios'),(8,'notícias comentadas')])+'</div>'
    if EP[1].get('video_url'):hero=hero.replace('Roteiro disponível · vídeo em preparação','Vídeo e roteiro disponíveis')
    home=hero+stats+'<section class="section"><div class="wrap"><div class="section-head"><h2>Comece pela missão.</h2><a href="serie.html">Ver a série completa</a></div><div class="grid">'+''.join(epcard(e) for e in DATA['episodes'][:3])+'</div></div></section>'
    home+='<section class="section soft"><div class="wrap"><div class="section-head"><h2>Na indústria. No campo. Na defesa.</h2><a href="modelos.html">Explorar o catálogo</a></div><div class="grid">'+''.join(f'<article class="card"><span class="tag">{E(m["sector"])}</span><h3>{E(m["name"])}</h3><p>{E(m["mission"])}</p><p>{E(m["lesson"])}</p><a class="link" href="modelos.html#{m["slug"]}">Ler a ficha e consultar a fonte</a></article>' for m in [M['phantom-4'],M['elios-3'],M['nauru-500c']])+'</div></div></section>'
    home+='''<section class="section"><div class="wrap feature"><figure class="figure"><img src="assets/ingenuity.jpg" alt="Helicóptero Ingenuity fotografado na superfície de Marte"><figcaption>Ingenuity, em Marte. NASA/JPL-Caltech/ASU/MSSS. Registro de 02/08/2023, publicado pela NASA em janeiro de 2024.</figcaption></figure><div><div class="eyebrow">Da bancada a Marte</div><h2>Quando voar depende de decidir a bordo.</h2><p>O Ingenuity fez 72 voos. Sua missão ajuda a discutir navegação, energia e aprendizado com falhas — temas que também aparecem em sistemas embarcados aqui na Terra.</p><a class="button" href="casos/ingenuity.html">Estudar o caso Ingenuity</a></div></div></section>'''
    home+='<section class="section soft"><div class="wrap"><div class="section-head"><h2>Casos para pensar a aplicação.</h2><a href="casos.html">Ver os oito casos</a></div><div class="grid">'+''.join(casecard(c) for c in DATA['cases'][:3])+'</div></div></section>'
    page('index.html','Início',home)
    published=sum(bool(e.get('video_url')) for e in DATA['episodes'])
    series_notice='<strong>Vídeos em preparação.</strong> Os conteúdos e roteiros já podem ser consultados. As gravações serão vinculadas às respectivas páginas quando estiverem disponíveis.' if not published else f'<strong>{published} de 12 episódios com vídeo vinculado.</strong> Consulte as páginas dos episódios para acessar os vídeos e os respectivos materiais.'
    page('serie.html','Os 12 episódios',intro('Série de vídeos','Conhecimento com propósito.','Roteiros-base para dois apresentadores, demonstrações, modelos e atividades. Cada episódio se conecta à apostila do curso.')+'<section class="section wrap"><div class="callout">'+series_notice+'</div><div class="grid">'+''.join(epcard(e) for e in DATA['episodes'])+'</div></section>','serie.html')
    for e in DATA['episodes']:
        article='<h2>O que você vai compreender</h2>'+items(e['goals'])+'<h2>Leitura de apoio</h2>'+paras(e['reading'])
        if e.get('video_url'):
            article='<div class="callout"><h2>Vídeo do episódio</h2><a class="button" href="'+E(e['video_url'],quote=True)+'" target="_blank" rel="noopener noreferrer">Assistir ao vídeo</a></div>'+article
        article+='<div class="callout"><strong>Conexão com a apostila</strong><p>'+E(e['base'])+'</p></div>'
        article+='<h2>Roteiro para dois apresentadores</h2><p class="meta">Papéis: Newton e professor instrutor. Ajustar as falas ao estilo dos apresentadores. O tempo estimado inclui demonstrações e comentários.</p>'
        article+=''.join('<div class="talk"><strong>'+('Professor instrutor' if who=='Instrutor' else 'Prof. Newton')+'</strong><p>'+E(line)+'</p></div>' for who,line in e['dialogue'])
        article+='<h2>Demonstração sugerida</h2>'+items(e['demo'])+'<div class="callout"><p>Práticas reais dependem da aptidão da equipe, do equipamento, do local e das condições autorizadas. Use a simulação quando essas condições não estiverem atendidas.</p></div>'
        article+='<h2>Atividade</h2><p>'+E(e['exercise'])+'</p><details><summary>Ver resposta comentada</summary><p>'+E(e['answer'])+'</p></details><h2>Fontes do episódio</h2>'+refs(e['refs'])
        aside=f'<h2>Material deste episódio</h2><a class="button" href="../materiais/episodio-{e["n"]:02d}.md" download>Baixar roteiro editável</a><a class="button" href="../downloads/roteiros-da-serie.pdf">Roteiros em PDF</a><h2>Modelos relacionados</h2><ul>'+''.join(f'<li><a href="../modelos.html#{slug}">{E(M[slug]["name"])}</a></li>' for slug in e['models'])+'</ul>'
        slide_start=2+3*(e['n']-1)
        aside+=f'<h2>Slides para gravação</h2><p>Telas {slide_start}–{slide_start+2} da apresentação. O PowerPoint inclui notas para os dois apresentadores.</p><a class="button" href="../downloads/slides-apoio-serie.pptx" download>Baixar PowerPoint</a><a class="button" href="../downloads/slides-apoio-serie.pdf#page={slide_start}">Abrir slides em PDF</a>'
        if e['cases']:aside+='<h2>Casos relacionados</h2><ul>'+''.join(f'<li><a href="../{casefile(C[slug])}">{E(C[slug]["title"])}</a></li>' for slug in e['cases'])+'</ul>'
        prevnext='<div class="prev-next">'+(f'<a href="{Path(epfile(EP[e["n"]-1])).name}">Episódio anterior</a>' if e['n']>1 else '<span></span>')+(f'<a href="{Path(epfile(EP[e["n"]+1])).name}">Próximo episódio</a>' if e['n']<12 else '<a href="../materiais.html">Consultar materiais</a>')+'</div>'
        body=f'<div class="wrap crumb"><a href="../serie.html">Episódios</a> / {e["n"]:02d}</div>'+intro(f'Episódio {e["n"]:02d} · {e["minutes"]}',e['title'],e['subtitle'])+'<section class="section wrap layout"><article class="article">'+article+prevnext+'</article><aside class="aside">'+aside+'</aside></section>'
        page(epfile(e),e['title'],body,'serie.html',True,desc=e['subtitle'])
    modelcards=''
    for m in DATA['models']:
        modelcards+=f'<article class="card" id="{m["slug"]}" data-model data-sector="{E(m["sector"])}"><span class="tag {"military" if m["sector"]=="Militar" else ""}">{E(m["sector"])} · {E(m["architecture"])}</span><h2 style="font-size:1.45rem">{E(m["name"])}</h2><p><strong>Missão:</strong> {E(m["mission"])}</p><p>{E(m["fact"])}</p><p><strong>Na aula:</strong> {E(m["lesson"])}</p><div class="callout"><p>{E(m["limit"])}</p></div>{refs(m["refs"])}</article>'
    search='<div class="searchbar"><div class="field"><label for="busca-modelos">Buscar por modelo, sensor ou aplicação</label><input id="busca-modelos" type="search" placeholder="Ex.: térmica, brasileiro, mapeamento"></div><div class="filter-buttons" role="group" aria-label="Tipo de aplicação">'+''.join(f'<button class="filter" data-filter="{s}" aria-pressed="{str(s=="Todos").lower()}">{s}</button>' for s in ['Todos','Civil','Militar','Pesquisa'])+'</div></div><p id="resultados" class="meta" aria-live="polite">17 modelos</p><p id="sem-resultados" class="empty" hidden>Nenhum modelo encontrado. Tente outra aplicação ou remova o filtro.</p>'
    page('modelos.html','Catálogo de drones',intro('17 plataformas • fontes oficiais','A missão escolhe o sistema.','Drones civis, brasileiros, militares e de pesquisa. As fichas são exemplos didáticos; máximos declarados não equivalem a limites autorizados de operação.')+'<section class="section wrap">'+search+'<div class="grid two">'+modelcards+'</div><p class="meta" style="margin-top:24px">Consulta em 09/10/2026. Não são cotações nem recomendações de compra. Variantes, acessórios e manuais devem ser conferidos.</p></section>','modelos.html')
    page('casos.html','Casos e aplicações',intro('Da observação à decisão','Casos reais. Perguntas de engenharia.','Quatro casos documentados e quatro cenários didáticos. A distinção entre evidência, hipótese e interpretação acompanha cada estudo.')+'<section class="section wrap"><div class="grid two">'+''.join(casecard(c) for c in DATA['cases'])+'</div></section>','casos.html')
    for c in DATA['cases']:
        body='<div class="wrap crumb"><a href="../casos.html">Casos</a> / '+E(c['area'])+'</div>'+intro(c['label']+' · '+c['area'],c['title'],c['fact'])+'<section class="section wrap layout"><article class="article"><h2>Análise para a aula</h2>'+paras(c['analysis'])+'<h2>Atividade proposta</h2><p>'+E(c['activity'])+'</p><h2>Entrega esperada</h2><p>'+E(c['deliverable'])+'</p><details><summary>Ver orientação ao professor</summary><p>'+E(c['answer'])+'</p></details><h2>Fontes e contexto</h2>'+refs(c['refs'])+'</article><aside class="aside"><h2>Continuar estudando</h2><a class="button" href="../materiais/caso-'+c['slug']+'.md" download>Baixar estudo editável</a><a class="button" href="../casos.html">Todos os casos</a><h2>Episódios relacionados</h2><ul>'+''.join(f'<li><a href="../{epfile(e)}">{e["n"]:02d} · {E(e["title"])}</a></li>' for e in DATA['episodes'] if c['slug'] in e['cases'])+'</ul></aside></section>'
        page(casefile(c),c['title'],body,'casos.html',True,desc=c['fact'])
    timeline=''
    for n in DATA['news']:
        timeline+='<article class="news-item"><span class="meta">'+n['date'][8:10]+'/'+n['date'][5:7]+'/'+n['date'][:4]+' · '+E(n['tag'])+'</span><h2>'+E(n['title'])+'</h2><p>'+E(n['summary'])+'</p><div class="callout"><strong>Pergunta para discussão</strong><p>'+E(n['question'])+'</p></div>'+refs(n['refs'])+f'<a href="{epfile(EP[n["ep"]])}">Conectar ao episódio {n["ep"]:02d}</a></article>'
    page('noticias.html','Notícias comentadas',intro('Recorte editorial • consulta em 09/10/2026','A notícia vira pergunta.','Seleção de fatos de 2024 a 2026, com data e fonte. Marcos históricos aparecem como históricos; anúncios comerciais são identificados por sua origem.')+'<section class="section wrap"><div class="timeline">'+timeline+'</div><div class="callout"><p>Esta é uma seleção estática, não um feed automático. Cada atualização deve conferir novamente fonte, data, contexto e possíveis retificações.</p></div></section>','noticias.html')
    downloads=[('Apostila ampliada','Apostila original de 84 páginas acompanhada do novo caderno de casos, modelos e roteiros.','downloads/apostila-ampliada.pdf','Abrir PDF'),('Caderno complementar','Leitura de apoio, roteiros, casos comentados, catálogo, notícias, normas e glossário.','downloads/caderno-complementar.pdf','Abrir PDF'),('Roteiros dos 12 episódios','Um arquivo para os dois apresentadores prepararem gravações e demonstrações.','downloads/roteiros-da-serie.pdf','Abrir PDF'),('Apostila original','Base do curso enviada pelo professor; autoria e conteúdo preservados.','downloads/apostila-base.pdf','Abrir PDF'),('Pacote de materiais editáveis','Markdown, dados estruturados, checklists e guias, em um arquivo ZIP.','downloads/materiais-editaveis.zip','Baixar ZIP'),('Guia de produção','Planejamento de gravação, materiais de apoio, captação e publicação.','materiais/guia-producao.md','Baixar guia'),('Ficha de missão','Modelo para objetivo, responsabilidades, decisão e debrief.','materiais/ficha-missao.md','Baixar ficha'),('Plano de integração na apostila','Onde inserir cada episódio, caso e ficha no curso de 12 encontros.','materiais/plano-integracao.md','Baixar plano')]
    downloads[3:3]=[('Slides de apoio aos 12 episódios','PowerPoint editável com 37 slides, notas para os apresentadores, demonstrações, respostas comentadas e fontes.','downloads/slides-apoio-serie.pptx','Baixar PowerPoint'),('Slides para consulta e projeção','As 37 telas em PDF. As notas de apresentação e as respostas permanecem no PowerPoint e nos roteiros.','downloads/slides-apoio-serie.pdf','Abrir PDF'),('Guia dos slides','Mapa das telas por episódio e orientações de uso no modo Apresentador.','materiais/guia-slides.md','Baixar guia')]
    resources='<div class="resources">'+''.join(f'<article class="resource"><div><h2>{E(t)}</h2><p>{E(d)}</p></div><a class="button" href="{url}"'+(' download' if not url.endswith('.pdf') else '')+f'>{cta}</a></article>' for t,d,url,cta in downloads)+'</div>'
    checklist='<ul class="checklist">'+''.join(f'<li><input type="checkbox" id="check-{i}"><label for="check-{i}">{E(s)}</label></li>' for i,s in enumerate(DATA['checklist']))+'</ul>'
    glossary='<dl class="glossary">'+''.join('<div><dt>'+E(t)+'</dt><dd>'+E(d)+'</dd></div>' for t,d in DATA['glossary'])+'</dl>'
    page('materiais.html','Apostilas e materiais',intro('Biblioteca da série','Leia. Prepare. Aplique.','Materiais para os apresentadores, parceiros e engenheirandos, com versões em PDF e arquivos editáveis.')+'<section class="section wrap">'+resources+'</section><section class="section soft"><div class="wrap feature"><figure class="figure cover"><img src="assets/apostila-base.png" alt="Capa da apostila original PI Drones — operação segura e projeto de engenharia"></figure><div><h2>Da apostila para uma série de extensão.</h2><p>A base do curso continua disponível. O caderno acrescenta aplicações, estudos, modelos e perguntas, e o plano de integração mostra onde usar cada material.</p><p class="meta">Base didática: Prof. Newton, Prof. Jucá e Instrutor Vitor, com os créditos originais preservados no PDF.</p></div></div></section><section class="section wrap"><h2>Checklist para discussão e preparação</h2><p>Marcação local nesta página; não é autorização nem registro formal. A ficha editável permite documentar a decisão.</p>'+checklist+'</section><section class="section soft"><div class="wrap"><h2>Glossário de consulta</h2>'+glossary+'</div></section>','materiais.html')
    norms=intro('Fontes oficiais • responsabilidades','Antes do voo, o enquadramento.','Use os textos oficiais e as condições emitidas para a missão. As páginas do curso ajudam a organizar a consulta.')+'<section class="section wrap article"><h2>Três camadas na mesma operação</h2><div class="table-wrap"><table><thead><tr><th>Responsável</th><th>O que conferir</th><th>Entrada oficial</th></tr></thead><tbody><tr><td>ANAC</td><td>Aplicabilidade, categoria, requisitos e transições.</td><td><a href="'+S['805']['url']+'">Resolução 805</a><br><a href="'+S['806']['url']+'">Resolução 806</a></td></tr><tr><td>DECEA</td><td>Acesso ao espaço aéreo e condições da autorização.</td><td><a href="'+S['decea']['url']+'">Portal Drone UAS</a></td></tr><tr><td>ANATEL</td><td>Conformidade e homologação dos produtos aplicáveis.</td><td><a href="'+S['anatel']['url']+'">Certificação de produtos</a></td></tr></tbody></table></div><h2>Referências de 2026</h2><p>A Resolução 805 aprovou o RBAC 100 em substituição ao RBAC-E 94. A Resolução 806 trata de UA até 250 g e aeromodelos em VLOS/EVLOS nas condições de aplicabilidade de seu texto. A ICA 100-40/2026 entrou em vigor em 1º de julho de 2026.</p><div class="callout"><strong>Conferir novamente antes da gravação</strong><p>A Resolução 805 contém dispensa temporária do parágrafo 100.13(b) até 31/12/2026. Não apresentar uma disposição de transição como regra permanente. Verificar emendas e atos posteriores nos portais oficiais.</p></div><h2>Princípios para ler um exemplo</h2>'+items(['Limite de catálogo é capacidade declarada; autorização é condição jurídica e operacional.','Sub-250 g não significa ausência de responsabilidades.','Uma autorização de espaço aéreo não resolve todas as demais exigências.','Exemplos militares, estrangeiros e científicos não estabelecem permissões para uma turma civil.','Uma missão deve ser reformulada quando a equipe ou o enquadramento não comportam seus requisitos.'])+'<h2>Fontes</h2>'+refs(['805','806','ica','decea','anatel'])+'</section>'
    page('normas.html','Normas e operação',norms,'normas.html')
    sourcebody=intro('Transparência editorial','A origem de cada afirmação.','Fontes oficiais de órgãos, fabricantes, pesquisa e comunicados. Consulta em 09/10/2026.')+'<section class="section wrap"><div class="callout"><h2>Como usar este acervo</h2><p>Fatos documentados são separados de cenários fictícios e da análise pedagógica. Números de fabricante são declarações sob condições próprias; notícias empresariais não são avaliação independente. Um preprint é identificado como tal.</p><p>Imagens, vídeos, nomes e marcas de terceiros conservam seus direitos. Os links levam às fontes; o acervo não republica manuais ou vídeos completos de terceiros. A foto do Ingenuity tem crédito NASA/JPL-Caltech/ASU/MSSS.</p></div><div class="source-list">'
    sourcebody+=''.join('<article class="source-item" id="'+s['id']+'"><span class="tag">'+E(s['kind'])+'</span><h2>'+E(s['title'])+'</h2><p>'+E(s['note'])+'</p><a class="url" href="'+E(s['url'])+'" target="_blank" rel="noopener noreferrer">'+E(s['url'])+'</a></article>' for s in DATA['sources'])+'</div></section>'
    page('fontes.html','Fontes e créditos',sourcebody,'fontes.html')

def md_refs(ids):return '\n'.join(f'- [{S[i]["title"]}]({S[i]["url"]}) — {S[i]["kind"]}.' for i in ids)
def md_episode(e):
    t=f'# {e["n"]:02d}. {e["title"]}\n\n{e["subtitle"]}\n\nSérie: **Drones Muito Além do Voo**. Consulta: 09/10/2026. Vídeo em preparação.\n\nDuração: {e["minutes"]}. Papéis: Prof. Newton e professor instrutor.\n\n## Conexão com a apostila\n\n{e["base"]}\n\n## Objetivos\n\n'+''.join('- '+x+'\n' for x in e['goals'])+'\n## Leitura de apoio\n\n'+'\n\n'.join(e['reading'])+'\n\n## Roteiro de gravação\n\n'
    t+='\n\n'.join('**'+('Professor instrutor' if who=='Instrutor' else 'Prof. Newton')+':** '+line for who,line in e['dialogue'])+'\n\n## Demonstração\n\n'+''.join(f'{i+1}. {x}\n' for i,x in enumerate(e['demo']))+'\nPrática real: conferir aptidão, local, equipamento e condições autorizadas. Use simulação se não houver condições.\n\n## Atividade\n\n'+e['exercise']+'\n\n## Resposta comentada\n\n'+e['answer']+'\n\n## Modelos\n\n'+''.join('- '+M[s]['name']+'\n' for s in e['models'])+'\n## Fontes\n\n'+md_refs(e['refs'])+'\n'
    return t
def md_case(c):return '# '+c['title']+'\n\n**'+c['label']+' — '+c['area']+'**\n\n'+c['fact']+'\n\n## Análise pedagógica\n\n'+'\n\n'.join(c['analysis'])+'\n\n## Atividade\n\n'+c['activity']+'\n\n## Entrega\n\n'+c['deliverable']+'\n\n## Orientação ao professor\n\n'+c['answer']+'\n\n## Fontes\n\n'+md_refs(c['refs'])+'\n'

def build_markdown():
    for e in DATA['episodes']:write(f'materiais/episodio-{e["n"]:02d}.md',md_episode(e))
    for c in DATA['cases']:write(f'materiais/caso-{c["slug"]}.md',md_case(c))
    write('materiais/catalogo-drones.md','# Catálogo de drones\n\nConsulta: 09/10/2026. Exemplos didáticos; não são recomendações de compra.\n\n'+'\n'.join(f'## {m["name"]}\n\n- Setor: {m["sector"]}\n- Arquitetura: {m["architecture"]}\n- Missão: {m["mission"]}\n- Característica: {m["fact"]}\n- Uso didático: {m["lesson"]}\n- Limitação: {m["limit"]}\n\n{md_refs(m["refs"])}\n' for m in DATA['models']))
    write('materiais/noticias-comentadas.md','# Notícias comentadas\n\nRecorte de 2024–2026. Consulta: 09/10/2026. Seleção estática.\n\n'+'\n'.join(f'## {n["date"]} — {n["title"]}\n\n{n["summary"]}\n\n**Pergunta:** {n["question"]}\n\n{md_refs(n["refs"])}\n' for n in DATA['news']))
    write('materiais/fontes.md','# Fontes e critérios editoriais\n\nConsulta: 09/10/2026. Fonte comercial não é validação independente. Números de fabricante dependem da configuração. Cenários didáticos são marcados.\n\n'+'\n'.join(f'- [{s["title"]}]({s["url"]}) — {s["kind"]}. {s["note"]}' for s in DATA['sources'])+'\n')
    write('materiais/ficha-missao.md','''# Ficha de missão e debrief

Série: Drones Muito Além do Voo. Modelo didático; não é autorização.

## 1. Missão

- ID, data, hora e versão do plano:
- Solicitante e responsável técnico:
- Pergunta a responder:
- Evidência esperada e critério de aceitação:
- Local, limites, referência e condições de uso:
- Plataforma, configuração, sensores e armazenamento:

## 2. Equipe e condições

- Piloto remoto em comando e observador:
- Comunicação e palavras de parada:
- Enquadramento, documentos, autorizações e homologação aplicáveis:
- Condições de clima, vento, visibilidade e interferência:
- Pessoas, acessos e isolamento:
- Energia e margens; não usar máximo de catálogo como duração de missão:
- Ponto de referência, retorno, pouso alternativo e contingências:

## 3. Decisão

- GO / NO-GO:
- Justificativa:
- Pendências e quem pode encerrá-las:
- Critério de interrupção e responsável pela decisão:

## 4. Registro e debrief

- Resultado e evidências obtidas:
- Nomes dos arquivos, horário, parâmetros e contexto:
- Ocorrências, desvios e limites:
- O que funcionou e o que exige nova verificação:
- Ações antes da próxima missão, responsável e prazo:
''')
    write('materiais/checklist.md','# Checklist de preparação\n\nModelo didático. Conferir aplicabilidade, manual e condições reais.\n\n'+''.join('- [ ] '+s+'\n' for s in DATA['checklist']))
    write('materiais/glossario.md','# Glossário de consulta\n\n'+''.join('## '+t+'\n\n'+d+'\n\n' for t,d in DATA['glossary']))
    write('materiais/guia-producao.md','''# Guia de produção da série

## Identidade e público

Título: **Drones Muito Além do Voo**. Público: comunidade, parceiros da extensão e engenheirandos interessados em tecnologia e aplicações. Dois apresentadores: Prof. Newton e professor instrutor. Confirmar nome e crédito do segundo apresentador antes das gravações. A base didática original preserva os créditos do Prof. Newton, Prof. Jucá e Instrutor Vitor.

## Formato de cada vídeo

Roteiros-base de 6–9 minutos, contando demonstração e comentários. As falas fornecidas servem à preparação e podem ser adaptadas; não são uma transcrição de gravação existente.

| Bloco | Tempo indicativo | Função |
|---|---|---|
| Pergunta inicial | 0:00–0:40 | Mostrar o problema concreto |
| Conceito e conversa | 0:40–2:30 | Explicar a relação entre sistema e missão |
| Caso e modelo | 2:30–4:00 | Aplicar o conceito com fonte visível |
| Demonstração | 4:00–6:00 | Bancada, tela, imagem ou simulador |
| Atividade e fechamento | 6:00–7:30 | Propor uma entrega e conectar ao próximo vídeo |

## Preparação

1. Conferir fontes, norma, versão de software e configuração de equipamentos. Registrar a data da checagem.
2. Separar aeronave apta e desligada para bancada, controle, bateria e cartões; usar gravação de tela nos exemplos de simulação.
3. Ensaiar falas e termos técnicos. Explicar cada sigla na primeira ocorrência.
4. Mostrar no vídeo: nome do modelo, variante, fonte e data. Em cenas fictícias, escrever “cenário didático”.
5. Preferir imagens próprias. Para materiais de terceiros, conferir permissão de reprodução; disponibilizar links quando não houver autorização.
6. Conferir créditos e uso da identidade institucional com a equipe de extensão antes de aplicar logos ou anunciar certificação institucional.

## Captação

- Duas vozes claras; priorizar microfone e ambiente sem ruído.
- Plano geral dos apresentadores, detalhes de equipamento e captura de tela em resolução legível.
- Bancada com aeronave desligada para identificação. Energização e prática somente em condições apropriadas.
- Não produzir uma operação de risco apenas para obter a cena. Simulação e imagem previamente coletada podem ensinar o mesmo conceito.
- Militares: usar fichas públicas para comparar missão, arquitetura e sensores; manter a discussão tecnológica e de responsabilidade.

## Edição e publicação

- Legendas revisadas em português, contraste e texto legível em celular.
- Cartela curta: título da série, número do episódio e pergunta central.
- Descrição: resumo, modelos, links do episódio, fontes e data de consulta.
- Não usar “mais recente”, “único” ou “garantido” sem verificação do contexto.
- Publicar o vídeo na plataforma escolhida e informar o URL no campo video_url de conteudo.py. Ao gerar o site, a página do episódio passa a mostrar o link para assistir.
- Atualizar o site com o processo documentado no README. Gravações não estão incluídas nesta edição.

## Modelo de descrição de vídeo

Drones Muito Além do Voo — Episódio [NN]: [título].

Neste episódio: [pergunta, conceito e aplicação].

Apresentação: Prof. Newton Licciardi Jr. e [nome do professor instrutor].

Materiais e fontes: https://newtonlicciardijr.github.io/drones/

Fontes verificadas em [data]. Casos e cenários didáticos identificados no material. As condições da norma, da autorização e do manual aplicáveis prevalecem sobre exemplos simplificados.
''')
    integration='# Plano de integração na apostila\n\nApostila base: 84 páginas do PDF enviado. Os encontros são a referência didática; a edição ampliada preserva o PDF original e acrescenta o caderno ao final. Para revisão do arquivo-fonte de slides, usar o mapeamento abaixo para inserções junto aos respectivos temas.\n\n| Episódio | Conexão na base | Material para inserir |\n|---|---|---|\n'
    for e in DATA['episodes']:
        cs=', '.join(C[s]['title'] for s in e['cases']) or 'Demonstração e atividade do episódio'
        integration+=f'| {e["n"]:02d}. {e["title"]} | {e["base"]} | {cs} |\n'
    integration+='\n## Uso em cada encontro\n\n1. Abrir com a pergunta central e um modelo real (3–5 min).\n2. Mostrar um caso ou uma notícia com data e fonte (5–8 min).\n3. Retomar o conceito da apostila e o briefing da prática.\n4. Executar a atividade dentro do escopo e das condições autorizadas.\n5. Registrar a evidência e fazer debrief.\n\nA série de extensão tem sequência temática própria, não substitui a formação operacional. As demonstrações avançadas, aeroagrícolas e militares são estudos de tecnologia; não são práticas propostas para o encontro introdutório.\n'
    write('materiais/plano-integracao.md',integration)
    write('materiais/atualizacao-editorial.md','''# Atualização editorial

## Antes de publicar uma nova edição

- Normas: consultar órgãos oficiais, aplicabilidade, vigência, emendas e transições. Conferir novamente a dispensa temporária até 31/12/2026 citada na Resolução 805.
- Modelos: identificar a variante, configuração e condições dos máximos. Diferenciar linha atual, suporte legado e missão encerrada.
- Notícias: registrar data do evento e da publicação; identificar fonte comercial, órgão ou pesquisa. Não transformar um marco histórico em novidade.
- Casos: distinguir fato documentado, interpretação pedagógica e cenário sintético. Corrigir o material quando novas evidências mudarem a conclusão.
- Fontes: verificar links, direitos de reprodução e créditos. Não copiar matérias ou manuais completos.
- Vídeos: informar URL real após publicação e manter o estado “em preparação” enquanto não houver gravação disponível.

## Registro de uma atualização

Data / responsável / item / mudança / fonte / efeito no roteiro e na atividade.

O acervo é estático. Esta entrega não configura monitoramento recorrente nem atualização automática.
''')
    with (ROOT/'materiais/catalogo-drones.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['modelo','setor','arquitetura','missao','caracteristica','uso_didatico','limite','fontes'])
        for m in DATA['models']:w.writerow([m[k] for k in ['name','sector','architecture','mission','fact','lesson','limit']]+['; '.join(S[i]['url'] for i in m['refs'])])

def make_pdf(path,with_all=True):
    for name,file in [('DVS','DejaVuSans.ttf'),('DVS-Bold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
    styles=getSampleStyleSheet()
    for k in ['Normal','BodyText','Heading1','Heading2','Heading3','Title']:styles[k].fontName='DVS'
    styles['Normal'].fontSize=9.7;styles['Normal'].leading=14;styles['Normal'].spaceAfter=7
    styles['Title'].fontName='DVS-Bold';styles['Title'].fontSize=28;styles['Title'].leading=33;styles['Title'].textColor=colors.HexColor('#111d32')
    styles['Heading1'].fontName='DVS-Bold';styles['Heading1'].fontSize=20;styles['Heading1'].leading=25;styles['Heading1'].textColor=colors.HexColor('#111d32');styles['Heading1'].spaceAfter=16
    styles['Heading2'].fontName='DVS-Bold';styles['Heading2'].fontSize=13;styles['Heading2'].leading=18;styles['Heading2'].spaceBefore=14;styles['Heading2'].spaceAfter=7
    styles['Heading3'].fontName='DVS-Bold';styles['Heading3'].fontSize=11;styles['Heading3'].leading=15
    styles.add(ParagraphStyle('Small',parent=styles['Normal'],fontSize=8,leading=12,textColor=colors.HexColor('#526177')))
    styles.add(ParagraphStyle('Accent',parent=styles['Normal'],fontName='DVS-Bold',textColor=colors.HexColor('#be2c38'),fontSize=10,leading=15))
    styles.add(ParagraphStyle('BibliographyHeading',parent=styles['Heading2'],fontSize=10.5,leading=14,spaceBefore=9,spaceAfter=4))
    styles.add(ParagraphStyle('BibliographyText',parent=styles['Normal'],fontSize=8.7,leading=12,spaceAfter=4))
    story=[]
    def p(text,style='Normal'):story.append(Paragraph(E(text).replace('\n','<br/>'),styles[style]))
    def h(text):p(text,'Heading2')
    def bullets(xs):
        for x in xs:p('• '+x)
    def reference(ids,keep=True):
        block=[Paragraph('Fontes',styles['Heading2'])]
        for i in ids:
            s=S[i];block.append(Paragraph(f'<link href="{E(s["url"],quote=True)}" color="#245a91">{E(s["title"])}</link> · {E(s["kind"])}',styles['Small']))
        if keep:story.append(KeepTogether(block))
        else:story.extend(block)
    def newchapter(title,label):story.append(PageBreak());p(label,'Accent');p(title,'Heading1')
    p('DRONES','Accent');p('Muito Além do Voo','Title');story.append(Spacer(1,20));p('Caderno complementar' if with_all else 'Roteiros da série','Heading1');p('Tecnologia, operação, engenharia e aplicações para a sociedade.');p('Prof. Newton Licciardi Jr. • Roteiros para dois apresentadores.');p('Edição 1.0 • Fontes consultadas em 09/10/2026.');p('12 episódios • 17 modelos • 8 casos • 8 notícias.');story.append(Spacer(1,24));p('Uso deste material','Heading2');p('O caderno amplia a base do curso com leitura, casos e propostas de gravação. A apostila original preserva seus autores e permanece disponível. Os vídeos ainda não foram gravados ou publicados nesta edição.');p('Casos documentados são identificados; os demais exemplos são cenários didáticos com valores sintéticos. Capacidades de fabricante não são autorizações de operação.');p('https://newtonlicciardijr.github.io/drones/','Accent')
    if with_all:
        story.append(Spacer(1,18));story.append(Image(str(ROOT/'assets/ingenuity.jpg'),width=430,height=156,kind='proportional'));p('Ingenuity em Marte. NASA/JPL-Caltech/ASU/MSSS. Registro de 02/08/2023.','Small')
    newchapter('Mapa da série','CONTEÚDO')
    for e in DATA['episodes']:p(f'{e["n"]:02d}  {e["title"]}');p(e['base'],'Small')
    for e in DATA['episodes']:
        newchapter(e['title'],f'EPISÓDIO {e["n"]:02d}');p(e['subtitle']);p(e['minutes'],'Small');p(e['base'],'Small');h('Objetivos');bullets(e['goals']);h('Leitura de apoio')
        for q in e['reading']:p(q)
        h('Roteiro para dois apresentadores')
        for who,line in e['dialogue']:
            story.append(KeepTogether([Paragraph('Professor instrutor' if who=='Instrutor' else 'Prof. Newton',styles['Accent']),Paragraph(E(line),styles['Normal'])]))
        h('Demonstração sugerida');bullets(e['demo']);h('Atividade');p(e['exercise']);h('Resposta comentada');p(e['answer']);h('Modelos de referência');bullets([M[s]['name'] for s in e['models']]);reference(e['refs'])
    if with_all:
        for c in DATA['cases']:
            newchapter(c['title'],c['label'].upper()+' • '+c['area'].upper());p(c['fact']);h('Análise pedagógica')
            for q in c['analysis']:p(q)
            h('Atividade');p(c['activity']);h('Entrega');p(c['deliverable']);h('Orientação ao professor');p(c['answer']);reference(c['refs'])
        newchapter('Catálogo de plataformas','17 MODELOS')
        for m in DATA['models']:
            start=len(story)
            h(m['name']);p(m['sector']+' • '+m['architecture'],'Accent');p('Missão: '+m['mission']);p(m['fact']);p('Uso didático: '+m['lesson']);p('Limitação: '+m['limit']);reference(m['refs'],keep=False)
            block=story[start:];del story[start:];story.append(KeepTogether(block))
        newchapter('Notícias comentadas','RECORTE 2024–2026')
        for n in DATA['news']:
            start=len(story)
            h(n['date']+' • '+n['title']);p(n['summary']);p('Pergunta: '+n['question']);reference(n['refs'],keep=False)
            block=story[start:];del story[start:];story.append(KeepTogether(block))
        newchapter('Normas e responsabilidades','CONSULTA EM 09/10/2026');p('ANAC: aplicabilidade, requisitos e transições. DECEA: acesso ao espaço aéreo. ANATEL: conformidade dos equipamentos. Conferir as fontes oficiais, o manual e as condições autorizadas da missão.');p('A Resolução 805 contém dispensa temporária do parágrafo 100.13(b) até 31/12/2026. Não ensinar uma condição transitória como permanente. Este caderno não é revisão jurídica exaustiva da apostila base.');reference(['805','806','ica','decea','anatel'])
        newchapter('Ficha de missão e checklist','PREPARAÇÃO E DEBRIEF');p('Registrar objetivo, evidência, equipe, local, configuração, condições, contingências, decisão e pendências. Após a missão: resultado, arquivos, ocorrências e ações para a próxima atividade.');bullets(DATA['checklist'])
        newchapter('Glossário de consulta','TERMOS')
        for t,d in DATA['glossary']:
            story.append(KeepTogether([Paragraph(E(t),styles['Heading2']),Paragraph(E(d),styles['Normal'])]))
        newchapter('Produção e atualização','ORIENTAÇÃO EDITORIAL');p('Dois apresentadores: uma pergunta concreta, explicação, caso com data e fonte, demonstração e atividade. Estimativa de 6–9 minutos inclui pausas e demonstração; ajustar ao ensaio. Os roteiros são editáveis.');p('Antes da gravação, conferir normas, versões e créditos. Preferir imagens próprias e links a materiais de terceiros. Não encenar operações de risco para obter imagens.');p('O acervo é estático. Registrar data, responsável, mudança e fonte em cada atualização. Marcos históricos devem permanecer datados. Vídeos só devem ser vinculados após publicação real.');p('A versão ampliada mantém as 84 páginas originais e acrescenta este caderno. O plano editável de integração mapeia os episódios aos encontros do curso.');
        newchapter('Fontes e créditos','BIBLIOGRAFIA')
        for s in DATA['sources']:
            story.append(KeepTogether([Paragraph(E(s['title']),styles['BibliographyHeading']),Paragraph(E(s['kind']+' • Consulta: 09/10/2026'),styles['Small']),Paragraph(E(s['note']),styles['BibliographyText']),Paragraph(f'<link href="{E(s["url"],quote=True)}" color="#245a91">{E(s["url"])}</link>',styles['Small'])]))
    def footer(canvas,doc):
        w,ht=A4;canvas.saveState();canvas.setStrokeColor(colors.HexColor('#dce2e9'));canvas.line(42,38,w-42,38);canvas.setFont('DVS',8);canvas.setFillColor(colors.HexColor('#526177'));canvas.drawString(42,24,'Drones Muito Além do Voo • edição 1.0 • 09/10/2026');canvas.drawRightString(w-42,24,str(doc.page));canvas.restoreState()
    SimpleDocTemplate(str(path),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=48,bottomMargin=54,title='Drones Muito Além do Voo',author='Prof. Newton Licciardi Jr.').build(story,onFirstPage=footer,onLaterPages=footer)

def build_downloads():
    original=ROOT.parent.parent/'upload/Apostila-PI-Drones-Normas-2026-Categoria-Aberta-v4 - Copia.pdf'
    if original.exists():shutil.copyfile(original,ROOT/'downloads/apostila-base.pdf')
    elif not (ROOT/'downloads/apostila-base.pdf').exists():raise FileNotFoundError('Disponibilize downloads/apostila-base.pdf para gerar a edição ampliada.')
    make_pdf(ROOT/'downloads/caderno-complementar.pdf')
    make_pdf(ROOT/'downloads/roteiros-da-serie.pdf',False)
    writer=PdfWriter();writer.append(str(ROOT/'downloads/apostila-base.pdf'),import_outline=False);writer.append(str(ROOT/'downloads/caderno-complementar.pdf'),import_outline=False);writer.add_outline_item('Parte 1 • Apostila original do curso',0);writer.add_outline_item('Parte 2 • Drones Muito Além do Voo',84);writer.add_metadata({'/Title':'Drones Muito Além do Voo — apostila ampliada','/Author':'Prof. Newton Licciardi Jr.; créditos originais preservados na Parte 1'})
    with (ROOT/'downloads/apostila-ampliada.pdf').open('wb') as f:writer.write(f)
    with zipfile.ZipFile(ROOT/'downloads/materiais-editaveis.zip','w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted((ROOT/'materiais').glob('*')):z.write(f,'materiais/'+f.name)
        z.write(ROOT/'conteudo.json','conteudo.json');z.write(ROOT/'README.md','README.md')

def readme():
    write('README.md','''# Drones Muito Além do Voo

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
''')

if __name__=='__main__':
    write('conteudo.json',json.dumps(DATA,ensure_ascii=False,indent=2)+'\n')
    readme();build_markdown();build_site();build_downloads()
    pages=list(ROOT.rglob('*.html'))
    print(f'{len(pages)} páginas HTML; {len(list((ROOT/"materiais").glob("*.md")))} arquivos Markdown')
    for f in sorted((ROOT/'downloads').glob('*.pdf')):print(f.name,len(PdfReader(f).pages),'páginas',f.stat().st_size,'bytes')

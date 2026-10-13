(() => {
  const search = document.querySelector('#busca-modelos');
  if (!search) return;
  const cards = [...document.querySelectorAll('[data-model]')];
  const buttons = [...document.querySelectorAll('[data-filter]')];
  let sector = 'Todos';
  const normalize = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  function update() {
    const term = normalize(search.value.trim());
    let count = 0;
    cards.forEach(card => {
      const visible = normalize(card.textContent).includes(term) && (sector === 'Todos' || card.dataset.sector.includes(sector));
      card.hidden = !visible;
      count += Number(visible);
    });
    document.querySelector('#resultados').textContent = `${count} de ${cards.length} modelos`;
    document.querySelector('#sem-resultados').hidden = count > 0;
  }
  search.addEventListener('input', update);
  buttons.forEach(button => button.addEventListener('click', () => {
    sector = button.dataset.filter;
    buttons.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    update();
  }));
  update();
})();

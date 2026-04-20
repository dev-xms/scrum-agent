// backlog_id: BKI-001, BKI-002
const STORAGE_KEY = 'smart_plate_recipes';
const DARK_MODE_KEY = 'smart_plate_dark_mode';

function loadRecipes() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; }
  catch { return []; }
}

function saveRecipes(recipes) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(recipes));
}

function addRecipe(title, ingredients, instructions) {
  if (!title.trim() || !ingredients.trim() || !instructions.trim()) {
    throw new Error('All fields required');
  }
  const recipes = loadRecipes();
  recipes.push({ id: Date.now(), title, ingredients, instructions });
  saveRecipes(recipes);
}

function deleteRecipe(id) {
  const recipes = loadRecipes().filter(r => r.id !== id);
  saveRecipes(recipes);
}

function filterRecipes(recipes, query) {
  const q = query.trim().toLowerCase();
  if (!q) return recipes;
  return recipes.filter(r => r.title.toLowerCase().includes(q));
}

function renderList(query = '') {
  const list = document.getElementById('recipe-list');
  const recipes = filterRecipes(loadRecipes(), query);

  list.innerHTML = '';

  if (recipes.length === 0) {
    const li = document.createElement('li');
    li.dataset.testid = 'empty-state';
    li.className = 'empty';
    li.textContent = query.trim() ? 'No recipes match your search' : 'No recipes yet';
    list.appendChild(li);
    return;
  }

  recipes.forEach(r => {
    const li = document.createElement('li');
    li.dataset.testid = 'recipe-item';

    const content = document.createElement('div');
    content.className = 'recipe-content';
    content.innerHTML = `<h3>${escapeHtml(r.title)}</h3>
      <p><strong>Ingredients:</strong> ${escapeHtml(r.ingredients)}</p>
      <p><strong>Instructions:</strong> ${escapeHtml(r.instructions)}</p>`;

    const btn = document.createElement('button');
    btn.dataset.testid = 'btn-delete';
    btn.textContent = 'Delete';
    btn.addEventListener('click', () => {
      deleteRecipe(r.id);
      renderList(document.querySelector('[data-testid="input-search"]').value);
    });

    li.appendChild(content);
    li.appendChild(btn);
    list.appendChild(li);
  });
}

function escapeHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function initDarkMode() {
  if (localStorage.getItem(DARK_MODE_KEY) === '1') {
    document.body.classList.add('dark');
  }
  document.querySelector('[data-testid="btn-dark-mode"]').addEventListener('click', () => {
    document.body.classList.toggle('dark');
    localStorage.setItem(DARK_MODE_KEY, document.body.classList.contains('dark') ? '1' : '');
  });
}

function init() {
  const form = document.getElementById('recipe-form');
  const errorEl = document.querySelector('[data-testid="error-message"]');
  const searchEl = document.querySelector('[data-testid="input-search"]');

  form.addEventListener('submit', e => {
    e.preventDefault();
    const title = form.querySelector('[data-testid="input-title"]').value;
    const ingredients = form.querySelector('[data-testid="input-ingredients"]').value;
    const instructions = form.querySelector('[data-testid="input-instructions"]').value;

    try {
      addRecipe(title, ingredients, instructions);
      errorEl.textContent = '';
      errorEl.classList.add('hidden');
      form.reset();
      renderList(searchEl.value);
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove('hidden');
    }
  });

  searchEl.addEventListener('input', () => renderList(searchEl.value));

  initDarkMode();
  renderList();
}

document.addEventListener('DOMContentLoaded', init);

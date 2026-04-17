const STORAGE_KEY = 'smartplate_recipes';
const DARK_KEY = 'smartplate_dark';

function loadRecipes() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

function saveRecipes(recipes) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(recipes));
}

function validateForm(title) {
  const error = document.getElementById('title-error');
  if (!title.trim()) {
    error.classList.remove('hidden');
    return false;
  }
  error.classList.add('hidden');
  return true;
}

function saveRecipe(title, ingredients, instructions) {
  const recipes = loadRecipes();
  recipes.push({
    id: Date.now().toString(),
    title: title.trim(),
    ingredients: ingredients.trim(),
    instructions: instructions.trim(),
  });
  saveRecipes(recipes);
}

function deleteRecipe(id) {
  if (!window.confirm('Delete this recipe?')) return;
  const recipes = loadRecipes().filter(r => r.id !== id);
  saveRecipes(recipes);
  renderList(document.getElementById('search').value);
}

function filterRecipes(recipes, term) {
  if (!term.trim()) return recipes;
  const lower = term.toLowerCase();
  return recipes.filter(r => r.title.toLowerCase().includes(lower));
}

function toggleDark() {
  const isDark = document.body.classList.toggle('dark');
  localStorage.setItem(DARK_KEY, isDark ? 'true' : 'false');
  document.getElementById('dark-toggle').textContent = isDark ? 'Light Mode' : 'Dark Mode';
}

function loadDarkPref() {
  if (localStorage.getItem(DARK_KEY) === 'true') {
    document.body.classList.add('dark');
    document.getElementById('dark-toggle').textContent = 'Light Mode';
  }
}

function createRecipeCard(recipe) {
  const card = document.createElement('div');
  card.className = 'bg-white rounded-xl shadow p-4 mb-4';

  const title = document.createElement('h3');
  title.className = 'font-semibold text-gray-800 mb-2';
  title.textContent = recipe.title;

  const card_body = document.createElement('div');
  card_body.className = 'text-sm text-gray-600 space-y-1';

  if (recipe.ingredients) {
    const ing = document.createElement('p');
    ing.textContent = 'Ingredients: ' + recipe.ingredients;
    card_body.appendChild(ing);
  }

  if (recipe.instructions) {
    const ins = document.createElement('p');
    ins.textContent = 'Instructions: ' + recipe.instructions;
    card_body.appendChild(ins);
  }

  const deleteBtn = document.createElement('button');
  deleteBtn.className = 'mt-3 text-xs text-red-500 hover:text-red-700 font-medium';
  deleteBtn.textContent = 'Delete';
  deleteBtn.addEventListener('click', () => deleteRecipe(recipe.id));

  card.appendChild(title);
  card.appendChild(card_body);
  card.appendChild(deleteBtn);
  return card;
}

function renderList(searchTerm = '') {
  const container = document.getElementById('recipe-list');
  container.innerHTML = '';

  const recipes = filterRecipes(loadRecipes(), searchTerm);

  if (loadRecipes().length === 0) {
    const empty = document.createElement('p');
    empty.className = 'text-gray-400 text-sm';
    empty.textContent = 'No recipes yet. Add one above!';
    container.appendChild(empty);
    return;
  }

  if (recipes.length === 0) {
    const empty = document.createElement('p');
    empty.className = 'text-gray-400 text-sm';
    empty.textContent = 'No recipes match your search.';
    container.appendChild(empty);
    return;
  }

  recipes.forEach(recipe => container.appendChild(createRecipeCard(recipe)));
}

document.getElementById('recipe-form').addEventListener('submit', function (e) {
  e.preventDefault();
  const title = document.getElementById('title').value;
  const ingredients = document.getElementById('ingredients').value;
  const instructions = document.getElementById('instructions').value;

  if (!validateForm(title)) return;

  saveRecipe(title, ingredients, instructions);
  this.reset();
  document.getElementById('search').value = '';
  renderList();
});

document.getElementById('search').addEventListener('input', function () {
  renderList(this.value);
});

document.getElementById('dark-toggle').addEventListener('click', toggleDark);

loadDarkPref();
renderList();

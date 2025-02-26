// Helper function for suggestion items with keyboard navigation
function createSuggestionItem(text) {
  const item = document.createElement('div');
  item.textContent = text;
  item.setAttribute('role', 'option');
  item.tabIndex = 0;
  item.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      clientNameInput.value = text;
      suggestionsDiv.innerHTML = '';
      clientNameInput.focus();
    } else if (e.key === 'ArrowDown') {
      if (item.nextElementSibling) {
        item.nextElementSibling.focus();
      }
      e.preventDefault();
    } else if (e.key === 'ArrowUp') {
      if (item.previousElementSibling) {
        item.previousElementSibling.focus();
      } else {
        clientNameInput.focus();
      }
      e.preventDefault();
    }
  });
  item.addEventListener('click', () => {
    clientNameInput.value = text;
    suggestionsDiv.innerHTML = '';
    clientNameInput.focus();
  });
  return item;
}

let citiesData = [];
let regionsData = [];
let departmentData = [];

// DOM Elements for suggestions and messages
const suggestionsDiv = document.getElementById('suggestions');
const messageDiv = document.getElementById('message');
const clientNameInput = document.getElementById('clientName');

// Fonction de normalisation pour enlever accents et tirets
function normalizeString(str) {
  return str
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "") // Supprime les accents
    .replace(/-/g, ' ')              // Remplace les tirets par des espaces
    .trim();
}

// Afficher un spinner pendant le chargement du CSV
suggestionsDiv.innerHTML = "<div class='spinner'></div>";

fetch('data/v_commune_2024.csv')
  .then(response => {
    if (!response.ok) throw new Error('Erreur lors du chargement du fichier CSV.');
    return response.text();
  })
  .then(csvData => {
    // Nettoyage et traitement du CSV
    const rows = csvData
      .split('\n')
      .slice(1) // Ignorer l'en-tête
      .filter(row => row.trim() !== '');
    
    rows.forEach(row => {
      const columns = row
        .split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/)
        .map(col => col.replace(/^"|"$/g, '').trim());
      const type = columns[0];
      if (type === "COM" && columns.length > 9) {
        citiesData.push({
          code: columns[1],
          cityName: columns[9],
          departmentCode: columns[1]
        });
      } else if (type === "DEP" && columns.length > 9) {
        departmentData.push({
          code: columns[1],
          departmentName: columns[8]
        });
      } else if (type === "REG" && columns.length > 9) {
        regionsData.push({
          code: columns[3],
          regionName: columns[8]
        });
      }
    });
    setupSearch();
  })
  .catch(error => {
    console.error("Erreur CSV:", error);
    suggestionsDiv.innerHTML = "Erreur de chargement des données";
  });

function setupSearch() {
  let debounceTimer;
  clientNameInput.addEventListener('input', () => {
    // Effacer le message d'erreur dès que l'utilisateur tape
    if (clientNameInput.value.trim() !== '') {
      messageDiv.textContent = '';
      messageDiv.className = 'message';
    }
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const searchTerm = clientNameInput.value.trim();
      const searchTermNormalized = normalizeString(searchTerm);
      suggestionsDiv.innerHTML = '';
      if (searchTermNormalized.length < 2) {
        suggestionsDiv.classList.remove('show');
        return;
      }
      const regionResults = regionsData.filter(d => 
        normalizeString(d.regionName).startsWith(searchTermNormalized) ||
        normalizeString(d.code).startsWith(searchTermNormalized)
      );
      const departmentResults = departmentData.filter(d => 
        normalizeString(d.departmentName).startsWith(searchTermNormalized) ||
        normalizeString(d.code).startsWith(searchTermNormalized)
      );
      const cityResults = citiesData.filter(c => 
        normalizeString(c.cityName).startsWith(searchTermNormalized) ||
        normalizeString(c.departmentCode).startsWith(searchTermNormalized)
      );
      
      function appendHeader(text) {
        const header = document.createElement('div');
        header.textContent = text;
        header.className = 'suggestions-header';
        suggestionsDiv.appendChild(header);
      }
      
      let resultsFound = false;
      if (regionResults.length > 0) {
        appendHeader('Régions');
        regionResults.forEach(item => {
          suggestionsDiv.appendChild(createSuggestionItem(`${item.regionName} (${item.code})`));
        });
        resultsFound = true;
      }
      if (departmentResults.length > 0) {
        appendHeader('Départements');
        departmentResults.forEach(item => {
          suggestionsDiv.appendChild(createSuggestionItem(`${item.departmentName} (${item.code})`));
        });
        resultsFound = true;
      }
      if (cityResults.length > 0) {
        appendHeader('Communes');
        cityResults.forEach(item => {
          suggestionsDiv.appendChild(createSuggestionItem(`${item.cityName} (${item.departmentCode})`));
        });
        resultsFound = true;
      }
      if (resultsFound) {
        suggestionsDiv.classList.add('show');
      } else {
        suggestionsDiv.textContent = 'Aucun résultat trouvé';
        suggestionsDiv.classList.add('show');
      }
    }, 300);
  });
}

clientNameInput.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowDown') {
    const firstSuggestion = suggestionsDiv.querySelector('div');
    if (firstSuggestion) {
      firstSuggestion.focus();
      e.preventDefault();
    }
  }
});

// Bouton Générer
document.getElementById('generateFileBtn').addEventListener('click', () => {
  const clientName = clientNameInput.value.trim();
  if (!clientName) {
    messageDiv.textContent = 'Veuillez entrer un nom de ville ou de département.';
    messageDiv.className = 'message error';
    return;
  }
  messageDiv.textContent = 'Traitement en cours...';
  messageDiv.className = 'message';
  fetch('src/main.py', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ clientName })
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Erreur HTTP ' + response.status);
      }
      return response.json();
    })
    .then(data => {
      messageDiv.textContent = data.message || 'Fichier généré avec succès.';
      messageDiv.className = 'message success';
      document.getElementById('generatedSheet').innerHTML = `<p>${data.message || 'Fiche client générée.'}</p>`;
    })
    .catch(error => {
      console.error("Erreur lors de la génération du fichier:", error);
      messageDiv.textContent = 'Erreur lors de la génération du fichier.';
      messageDiv.className = 'message error';
    });
});

// Bouton Importer
const importFileBtn = document.getElementById('importFileBtn');
const fileInput = document.getElementById('fileInput');

if (importFileBtn && fileInput) {
  importFileBtn.addEventListener('click', () => {
    fileInput.click();
  });
}
  fileInput.setAttribute('multiple', true); // Permettre les fichiers multiples
  fileInput.addEventListener('change', function(e) {
    const files = Array.from(e.target.files);
    const filesContainer = document.getElementById('uploadedFiles');
    filesContainer.innerHTML = ''; // Clear existing files
    
    files.forEach((file, index) => {
      const fileItem = document.createElement('div');
      fileItem.className = 'file-item';
      fileItem.innerHTML = `
        <span>${file.name}</span>
        <span class="remove-file" data-index="${index}">&times;</span>
      `;
      filesContainer.appendChild(fileItem);
  });

  // Gestion de la suppression
  filesContainer.querySelectorAll('.remove-file').forEach(btn => {
    btn.addEventListener('click', () => {
      const index = parseInt(btn.dataset.index);
      const dt = new DataTransfer();
      const filesArray = Array.from(fileInput.files);
      
      filesArray.splice(index, 1);
      filesArray.forEach(file => dt.items.add(file));
      fileInput.files = dt.files;
      
      btn.parentElement.remove();
    });
  });
});



// Back-to-top Button
document.addEventListener('DOMContentLoaded', () => {
  const backToTopButton = document.getElementById('back-to-top');
  if (backToTopButton) {
    const handleScroll = () => {
      backToTopButton.style.display = window.scrollY > 200 ? 'block' : 'none';
    };
    window.addEventListener('scroll', handleScroll);
    handleScroll();
    backToTopButton.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
});
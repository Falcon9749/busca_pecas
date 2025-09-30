async function performSearch() {
    const resultsDiv = document.getElementById('results');
    const loader = document.getElementById('loader');
    const searchInput = document.getElementById('partName');
    const modelInput = document.getElementById('carModel');
    
    const query = searchInput.value;
    const model = modelInput.value;

    if (!query) {
        alert('Por favor, digite pelo menos o nome de uma peça para buscar.');
        return;
    }

    resultsDiv.innerHTML = '';
    loader.style.display = 'block';

    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}&model=${encodeURIComponent(model)}`);
        const data = await response.json();
        loader.style.display = 'none';

        if (data.length === 0) {
            resultsDiv.innerHTML = '<p class="text-center">Nenhum resultado encontrado para esta combinação.</p>';
            return;
        }

        data.forEach(part => {
            const col = document.createElement('div');
            col.className = 'col-md-4 mb-4';

            // Define uma imagem placeholder caso a URL da imagem não exista
            const imageUrl = part.image_url ? part.image_url : 'https://via.placeholder.com/250x250.png?text=Sem+Imagem';

            // --- AQUI ESTÁ A MUDANÇA PARA MOSTRAR A IMAGEM ---
            col.innerHTML = `
                <div class="card h-100">
                    <img src="${imageUrl}" class="card-img-top p-3" alt="${part.name}" style="max-height: 250px; object-fit: contain;">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title" style="font-size: 1rem;">${part.name}</h5>
                        <h6 class="card-subtitle my-2 text-success fw-bold fs-4">${part.price}</h6>
                        <p class="card-text"><small class="text-muted">Vendedor: ${part.seller}</small></p>
                        <a href="${part.link}" class="btn btn-primary mt-auto" target="_blank">Ver Oferta</a>
                    </div>
                </div>
            `;
            resultsDiv.appendChild(col);
        });
    } catch (error) {
        console.error('Erro ao buscar:', error);
        loader.style.display = 'none';
        resultsDiv.innerHTML = '<p class="text-center text-danger">Ocorreu um erro ao buscar as peças. Tente novamente.</p>';
    }
}
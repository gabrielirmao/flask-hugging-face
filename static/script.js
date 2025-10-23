let typeInterval = null;

document.addEventListener('DOMContentLoaded', () => {
    
    const generateBtn = document.getElementById('generate-btn');
    const promptInput = document.getElementById('prompt-input');
    const responseCard = document.getElementById('response-card');
    const responseText = document.getElementById('response-text');
    const responseBox = document.getElementById('response-box');
    const loadingSpinner = document.getElementById('loading-spinner');
    
    const modelNameDisplay = document.getElementById('model-name-display');
    const modelIconContainer = document.getElementById('model-icon-container');

    async function fetchModelStatus() {
        let iconClass = 'bi-question-circle-fill';
        try {
            const response = await fetch('/api/model');
            if (!response.ok) throw new Error('Falha ao buscar status');
            
            const data = await response.json();
            modelNameDisplay.textContent = data.model_name || 'Indisponível';

            if (data.model_name.includes('GPU')) {
                iconClass = 'bi-gpu-card';
            } else if (data.model_name.includes('CPU')) {
                iconClass = 'bi-cpu-fill';
            }
            
        } catch (error) {
            console.error('Erro ao buscar modelo:', error);
            modelNameDisplay.textContent = 'Erro ao carregar';
            modelNameDisplay.classList.add('text-danger');
        } finally {
            modelIconContainer.innerHTML = `<i class="bi ${iconClass}"></i>`;
        }
    }

    function typeEffect(element, text, speed = 15) {
        if (typeInterval) {
            clearInterval(typeInterval);
        }
        
        let i = 0;
        element.innerHTML = "";
        responseCard.style.display = 'block'; 

        typeInterval = setInterval(() => {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                responseBox.scrollTop = responseBox.scrollHeight;
            } else {
                clearInterval(typeInterval);
                typeInterval = null;
            }
        }, speed);
    }

    generateBtn.addEventListener('click', async () => {
        const prompt = promptInput.value;

        if (!prompt.trim()) {
            Swal.fire({
                icon: 'warning',
                title: 'Oops...',
                text: 'Por favor, digite um prompt antes de enviar.',
                background: '#343a40',
                color: '#f8f9fa'
            });
            return;
        }

        setLoading(true);

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt: prompt })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Erro ${response.status}`);
            }

            const data = await response.json();
            
            typeEffect(responseText, data.response);

        } catch (error) {
            console.error('Erro ao gerar resposta:', error);
            Swal.fire({
                icon: 'error',
                title: 'Erro na Geração',
                text: error.message,
                background: '#343a40',
                color: '#f8f9fa'
            });
            responseCard.style.display = 'none';
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        if (isLoading) {
            generateBtn.disabled = true;
            loadingSpinner.classList.remove('d-none');
            if (typeInterval) {
                clearInterval(typeInterval);
                typeInterval = null;
            }
        } else {
            generateBtn.disabled = false;
            loadingSpinner.classList.add('d-none');
        }
    }

    fetchModelStatus();
});
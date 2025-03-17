// Script para manejar el formulario de solicitud de cliente
document.getElementById("getClientForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const nif = document.getElementById("nif").value;
    try {
        const response = await fetch(`/get_client?nif=${nif}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            const clientData = await response.json();
            // Mostrar los datos del cliente
            document.getElementById("username").textContent = clientData.username;
            document.getElementById("email").textContent = clientData.email;
            document.getElementById("nif-info").textContent = clientData.nif;
            document.getElementById("capital").textContent = clientData.capital;

            // Mostrar el contenedor de detalles
            document.getElementById("client-details").style.display = 'block';
            document.getElementById("error-message").style.display = 'none';
            document.getElementById("clearButton").style.display = 'block';
        } else {
            document.getElementById("client-details").style.display = 'none';
            document.getElementById("error-message").style.display = 'block';
            document.getElementById("clearButton").style.display = 'block';
        }
    } catch (error) {
        console.error("Error fetching client data:", error);
        document.getElementById("client-details").style.display = 'none';
        document.getElementById("error-message").style.display = 'block';
    }
});

// Script para manejar el formulario de simulación de hipoteca
document.getElementById("simulateMortgageForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const formData = {
        nif: document.getElementById("nif").value,
        tae: parseFloat(document.getElementById("tae").value),
        years: parseInt(document.getElementById("years").value)
    };

    try {
        const response = await fetch("/simulate_mortgage", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        if (response.ok) {
            // Mostrar los resultados
            document.getElementById("monthly-payment").textContent = ((data.monthly_pay).toFixed(2)) + "€";
            document.getElementById("total-payment").textContent = ((data.total).toFixed(2)) + "€";
            document.getElementById("total-interest").textContent = ((data.total - data.capital).toFixed(2)) + "€";

            // Mostrar los detalles de la hipoteca y ocultar el mensaje de error
            document.getElementById("mortgage-details").style.display = 'block';
            document.getElementById("error-message").style.display = 'none';
            document.getElementById("clearButton").style.display = 'block';
        } else {
            document.getElementById("mortgage-details").style.display = 'none';
            document.getElementById("error-message").style.display = 'block';
            document.getElementById("clearButton").style.display = 'block';
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("mortgage-details").style.display = 'none';
        document.getElementById("error-message").style.display = 'block';
    }
});

// Función para limpiar los resultados
document.getElementById("clearButton").addEventListener("click", function() {
    // Limpiar los campos y ocultar los detalles
    document.getElementById("nif").value = '';
    document.getElementById("tae").value = '';
    document.getElementById("years").value = '';
    document.getElementById("client-details").style.display = 'none';
    document.getElementById("mortgage-details").style.display = 'none';
    document.getElementById("error-message").style.display = 'none';
    document.getElementById("clearButton").style.display = 'none';
});

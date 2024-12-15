$(document).ready(function () {
    const converter = new showdown.Converter(); // Initialize showdown converter
    const sessionId = $('body').data('session-id'); // Read session_id from data attribute

    // Load chat history from history.json
    $.getJSON(`/chat/${sessionId}/history`, function (data) {
        const chatHistory = $('#chat-history');
        let totalTokens = 0;
        let totalCost = 0;

        data.forEach(message => {
            const messageClass = message.role === 'user' ? 'user' : 'bot';
            const messageContent = message.role === 'user' ? message.content : converter.makeHtml(message.content); // Convert markdown to HTML for bot messages
            chatHistory.append(`<div class="chat-message ${messageClass}">${messageContent}</div>`);
            totalTokens += message.content.split(' ').length;
        });

        // Calculate total cost based on tokens
        $.ajax({
            url: '/calculate_cost',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ messages: data, model: $('#model-select').val() }),
            success: function (response) {
                totalCost = response.total_cost;
                $('#total-tokens').text(totalTokens);
                if (totalCost === "FREE") {
                    $('#total-cost').html('<b>FREE</b>');
                } else {
                    $('#total-cost').text(totalCost.toFixed(2));
                }
            },
            error: function () {
                console.error('Failed to calculate cost.');
            }
        });
    });

    // Load previous chats
    $.getJSON('/previous_chats', function (data) {
        const previousChatsContainer = $('#previous-chats');
        previousChatsContainer.empty(); // Clear previous content
        data.forEach(chat => {
            previousChatsContainer.append(`<a href="/chat/${chat.session_id}">${chat.first_message}...</a>`);
        });
    });

    // Add dynamic model fetching logic
    $('#modeToggle').change(function () {
        const mode = $(this).is(':checked') ? 'API' : 'Local'; // Determine mode based on toggle state

        // Fetch models dynamically
        $.ajax({
            url: '/get_models', 
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ mode: mode }),
            success: function (data) {
                const dropdown = $('#model-select');
                dropdown.empty(); // Clear previous options
                dropdown.append('<option value="">--Select a Model--</option>'); // Default option

                // Populate with new models
                data.forEach(model => {
                    dropdown.append(`<option value="${model.id}">${model.name}</option>`);
                });
            },
            error: function () {
                console.error('Failed to fetch models.');
            }
        });
    });

    // Trigger an initial update for default mode
    $('#modeToggle').trigger('change');

    // Handle chat message submission
    $('#submit-button').click(function () {
        const message = $('#chat-input').val();
        const model = $('#model-select').val();

        if (!message || !model) {
            alert('Please enter a message and select a model.');
            return;
        }

        const chatHistory = $('#chat-history');
        chatHistory.append(`<div class="chat-message user">${message}</div>`); // Display user message immediately

        $.ajax({
            url: '/chat',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ message: message, model: model }),
            success: function (data) {
                const botMessageHtml = converter.makeHtml(data.response); // Convert markdown to HTML
                chatHistory.append(`<div class="chat-message bot">${botMessageHtml}</div>`);
                $('#chat-input').val(''); // Clear input field
                $('#total-tokens').text(data.total_tokens);
                if (data.total_cost === "FREE") {
                    $('#total-cost').html('<b>FREE</b>');
                } else {
                    $('#total-cost').text(data.total_cost.toFixed(2));
                }
            },
            error: function () {
                console.error('Failed to send message.');
            }
        });
    });

    // Handle file upload
    $('#file-upload').change(function () {
        const file = this.files[0];
        if (!file) {
            alert('Please select a file.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        $.ajax({
            url: '/upload_file',
            method: 'POST',
            processData: false,
            contentType: false,
            data: formData,
            success: function (data) {
                alert('File uploaded successfully.');
                $('#chat-input').val(data.text); // Set extracted text in input bar
            },
            error: function () {
                console.error('Failed to upload file.');
            }
        });
    });

    // Trigger file input click on label click
    $('.file-upload-label').click(function () {
        $('#file-upload').click();
    });
});
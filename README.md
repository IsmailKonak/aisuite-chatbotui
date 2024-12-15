# AI Chatbot UI for AI Suite Library

This project is created as part of a workshop titled **"Chatbot Workshop: Design Your Own AI Assistant"** conducted by the **Sakarya University AI Society**.

### What is this Project?
This project enables users to easily interact with multiple AI models through a single interface. Equipped with advanced features, it offers capabilities like saving chat histories, estimating costs, and processing PDF files. It also supports both local and API-based models, providing exceptional flexibility.

Türkçe README için, [buraya tıklayın](https://github.com/IsmailKonak/aisuite-chatbotui/blob/main/README_tr.md)

---

## **Key Features**

1. **Model Flexibility:**
   - Switch between different AI models within the same chat session, enabling diverse conversational experiences and comparisons.

2. **Chat History Management:**
   - Save and revisit previous chats, allowing users to continue past conversations seamlessly.

3. **Markdown Support:**
   - Display responses with Markdown formatting for enhanced readability, including features like links, code snippets, and lists.

4. **Cost Estimation:**
   - Calculate the estimated cost of a conversation based on the pricing models of various AI APIs, helping users manage and predict expenses effectively.

5. **Integration with Ollama:**
   - Utilize both local models and API-based models within the same chat session, offering flexibility in performance, privacy, and cost.

6. **Crop Conversation for Infinite Chat:**
   - Automatically crops old conversations to ensure the context length remains within model limits, allowing for continuous, uninterrupted chatting.

7. **PDF Upload Support (Text Only):**
   - Upload text-based PDF files to interact with their content directly in the chat interface. Ideal for extracting insights, summarizing, or asking questions about the document.

---

## **Setup Instructions (Windows)**

### **Step 1: Install Required Libraries**

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

---

### **Step 2: Configure the Models**

1. Navigate to the `model_config.json` file in the project directory.

2. Update the model configuration with your API keys and model details. Below is an example structure:
   ```json
   {
       "models": [
           {
               "name": "OpenAI GPT-4o",
               "api_key": "Your API Key Here",
               "id": "openai:gpt-4o",
               "local": false
           },
           {
               "name": "Ollama Llama3.2 3B",
               "api_key": "None",
               "id": "ollama:llama3.2:3b",
               "local": true
           }
       ]
   }
   ```

3. Key points:
   - Replace `"Your API Key Here"` with the appropriate API keys for each model.
   - Local models (`"local": true`) do not require API keys.

---

### **Step 3: Configure Pricing (Optional)**

1. Open the `pricing_config.json` file to update the cost for each model:
   ```json
   {
       "openai:gpt-4o": {
           "prompt_tokens": 2.50,
           "completion_tokens": 10.00
       }
   }
   ```

2. Notes:
   - Pricing is given in **USD** per 1,000 tokens.
   - Local models (`local: true`) do not have pricing, as they operate on your hardware without additional costs.

---

### **Step 4: Setup for Local Models**

1. Download and install **Ollama** from their [official website](https://ollama.com).

2. After installation, use the following command to download the required local models:
   ```bash
   ollama pull <model_id>
   ```
   - Replace `<model_id>` with the specific ID of the model you want to use (e.g., `ollama:llama3.2:3b`).

3. Once the model is installed, update the `model_config.json` with:
   - **Provider:** Use `ollama` as the provider.
   - **Model ID:** The ID of the downloaded model.

---

### **Step 5: Run the Application**

1. Start the chatbot UI by running the following command:
   ```bash
   python app.py
   ```

2. Open your browser and go to the URL displayed in the terminal (default: `http://127.0.0.1:5000/`) to start using the chatbot.

---

### **Step 6: Additional Feature - Uploading PDFs**

1. To use the PDF upload feature, ensure the files are:
   - **Text-based PDFs** (scanned or image-based PDFs are not supported).

2. Upload the PDF file through the chatbot UI by clicking the **Upload** button. Once uploaded, the file's text content will be available for interaction.

---

## **Features to Be Added Later**

1. **Retrieval-Augmented Generation (RAG):**
   - Integrate retrieval-based techniques to enhance chatbot responses by incorporating relevant data from external sources or uploaded documents.

2. **Image Support:**
   - Enable the chatbot to handle image inputs, such as analyzing, describing, or extracting data from images.

3. **Adding Models via Interface:**
   - Provide an intuitive interface for adding new models directly to the system without needing to modify the configuration file manually.

4. **Setting API Prices via Web Scraping:**
   - Automate the updating of API pricing configurations by scraping pricing information from official provider websites.

5. **Setting Conversation Max Token Size via Interface:**
   - Allow users to configure the maximum token size for conversations directly through the interface, providing better control over context length and performance.

---

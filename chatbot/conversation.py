import tiktoken

def crop_conversation(max_tokens, messages, next_message):
    tokenizer = tiktoken.encoding_for_model(model_name="gpt-4o")
    messages.append(next_message)
    tokenized_messages = [(msg, tokenizer.encode(msg["content"])) for msg in messages]
    total_tokens = sum(len(tokens) for _, tokens in tokenized_messages)

    while total_tokens > max_tokens and tokenized_messages:
        for i, (msg, tokens) in enumerate(tokenized_messages):
            if msg["role"] != "system":
                total_tokens -= len(tokens)
                tokenized_messages.pop(i)
                break

    return [msg for msg, _ in tokenized_messages]

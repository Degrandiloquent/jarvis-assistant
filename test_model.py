#!/usr/bin/env python3
"""
Simple test script to verify if the DialoGPT model is working.
"""

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    print("Testing DialoGPT model...")

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small", force_download=False, resume_download=True)
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small", force_download=False, resume_download=True)

    # Set pad token
    tokenizer.pad_token = tokenizer.eos_token

    # Test inputs
    test_inputs = [
        "Hello, how are you?",
        "What is your name?",
        "Tell me a joke",
        "What can you do?"
    ]

    print("\nModel loaded successfully!")
    print("Generating responses to test inputs:\n")

    for test_input in test_inputs:
        print(f"Input: {test_input}")

        # Encode input
        input_ids = tokenizer.encode(test_input + tokenizer.eos_token, return_tensors='pt')

        # Generate response
        output = model.generate(
            input_ids,
            max_length=50,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            top_p=0.95,
            top_k=50,
            temperature=0.7,
            num_return_sequences=1
        )

        # Decode response
        response = tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        print(f"Response: {response.strip()}")
        print("-" * 40)

    print("\n✅ Model is working correctly!")

except Exception as e:
    print(f"❌ Error testing model: {e}")
    print("The model may not be working properly.")

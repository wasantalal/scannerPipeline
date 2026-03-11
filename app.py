from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

print("Loading model...")

# try phi-2 instead (older but more stable)
model = AutoModelForCausalLM.from_pretrained(
        "microsoft/phi-2", 
        device_map="auto", 
        torch_dtype="auto", 
        trust_remote_code=True 
        )
    
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")

generator = pipeline(
        "text-generation", #Specifies the task type
        model=model,
        tokenizer=tokenizer,
        return_full_text=False, #returns only the newly generated text
        max_new_tokens=500,
        do_sample=False
        )
    
print("Model loaded successfully!")
print("What do you want?")
user_input = input()

# Phi-2 uses a different format
prompt = f"Instruct: {user_input}\nOutput:"
response = generator(prompt)
print(response[0]["generated_text"])
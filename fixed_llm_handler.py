import os
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model configurations
model_names = {
    "GPT-Neo 1.3B": "EleutherAI/gpt-neo-1.3B",
    "Bloom-560M": "bigscience/bloom-560m", 
    "OPT-1.3B": "facebook/opt-1.3b"
}

# Global variables for lazy loading
loaded_models = {}
tokenizers = {}

def load_model(llm_name):
    """Lazy load model and tokenizer when needed."""
    if llm_name in loaded_models:
        return loaded_models[llm_name], tokenizers[llm_name]
    
    if llm_name not in model_names:
        raise ValueError(f"Model {llm_name} not supported")
    
    model_path = model_names[llm_name]
    
    try:
        logger.info(f"Loading {llm_name}...")
        
        # Load tokenizer first
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        # Set or add a padding token
        if tokenizer.pad_token is None:
            if tokenizer.eos_token:
                tokenizer.pad_token = tokenizer.eos_token
            else:
                tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        
        # Load model with appropriate settings
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            low_cpu_mem_usage=True
        )
        
        # Resize embeddings if we added new tokens
        if tokenizer.pad_token == '[PAD]':
            model.resize_token_embeddings(len(tokenizer))
        
        # Cache the loaded model and tokenizer
        loaded_models[llm_name] = model
        tokenizers[llm_name] = tokenizer
        
        logger.info(f"Successfully loaded {llm_name}")
        return model, tokenizer
        
    except Exception as e:
        logger.error(f"Error loading {llm_name}: {str(e)}")
        raise

def get_llm_response(llm_name, prompt, max_length=200):
    """Generate a response using the selected LLM."""
    try:
        model, tokenizer = load_model(llm_name)
        
        # Tokenize the input
        inputs = tokenizer(
            prompt, 
            return_tensors="pt", 
            truncation=True, 
            max_length=512, 
            padding=True
        )
        
        # Move to appropriate device
        device = next(model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate text with better parameters
        with torch.no_grad():
            outputs = model.generate(
                inputs['input_ids'],
                attention_mask=inputs['attention_mask'],
                max_length=len(inputs['input_ids'][0]) + max_length,
                num_beams=2,
                early_stopping=True,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
                do_sample=True,
                temperature=0.7,
                repetition_penalty=1.2
            )
        
        # Decode the generated text
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the original prompt from response
        if response.startswith(prompt):
            response = response[len(prompt):].strip()
        
        return response if response else "I apologize, but I couldn't generate a meaningful response."
        
    except Exception as e:
        logger.error(f"Error generating response with {llm_name}: {str(e)}")
        return f"Error: Could not generate response with {llm_name}. Please try again."

def get_model_info():
    """Get information about available models."""
    return {
        name: {
            "path": path,
            "loaded": name in loaded_models,
            "parameters": "1.3B" if "1.3B" in name else "560M" if "560M" in name else "1.3B"
        }
        for name, path in model_names.items()
    }

def clear_model_cache():
    """Clear loaded models to free memory."""
    global loaded_models, tokenizers
    loaded_models.clear()
    tokenizers.clear()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    logger.info("Model cache cleared")
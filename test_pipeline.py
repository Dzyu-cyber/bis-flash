import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))
from src.pipeline import RAGPipeline

print("Initializing pipeline...")
pipeline = RAGPipeline(use_llm_expansion=False)
print("Pipeline initialized.")

query = "Water purifiers"
print(f"Running query: {query}")
results = pipeline.run(query)
print(f"Results: {results}")

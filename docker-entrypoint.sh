#!/bin/bash

if [ ! -d "/app/chroma_db" ] || [ -z "$(ls -A /app/chroma_db)" ]; then
    echo "building vector store..."
    cd /app/src && python vectorstore.py
fi

echo "starting streamlit app..."
streamlit run src/app.py --server.port=8501 --server.address=0.0.0.0


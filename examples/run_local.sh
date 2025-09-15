#!/bin/bash
# Local execution script for XBOW Autonomous Web Bug Hunter

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PATH="$PROJECT_ROOT/venv"

# Default model path (user should modify this)
DEFAULT_MODEL_PATH="$PROJECT_ROOT/models/codellama-7b-instruct.Q4_K_M.gguf"

echo "🎯 XBOW Autonomous Web Bug Hunter - Local Runner"
echo "================================================"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Virtual environment not found at $VENV_PATH"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Check if model path is set
if [ -z "$LLM_MODEL_PATH" ]; then
    if [ -f "$DEFAULT_MODEL_PATH" ]; then
        export LLM_MODEL_PATH="$DEFAULT_MODEL_PATH"
        echo "📁 Using default model: $LLM_MODEL_PATH"
    else
        echo "❌ LLM_MODEL_PATH not set and default model not found"
        echo "Please download a GGUF model and set LLM_MODEL_PATH environment variable"
        echo ""
        echo "Example:"
        echo "  export LLM_MODEL_PATH=\"$DEFAULT_MODEL_PATH\""
        echo ""
        echo "Download models from:"
        echo "  https://huggingface.co/TheBloke"
        exit 1
    fi
else
    echo "📁 Using model: $LLM_MODEL_PATH"
fi

# Check if model file exists
if [ ! -f "$LLM_MODEL_PATH" ]; then
    echo "❌ Model file not found: $LLM_MODEL_PATH"
    exit 1
fi

# Check required tools
echo "🔍 Checking security tools..."
REQUIRED_TOOLS=("subfinder" "nuclei" "httpx")
MISSING_TOOLS=()

for tool in "${REQUIRED_TOOLS[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        MISSING_TOOLS+=("$tool")
    fi
done

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo "⚠️  Missing tools: ${MISSING_TOOLS[*]}"
    echo "Install with: sudo apt install ${MISSING_TOOLS[*]}"
    echo "Or download from project websites"
fi

# Set up output directory
mkdir -p "$PROJECT_ROOT/out"

# Change to project directory
cd "$PROJECT_ROOT"

# Run the agent with provided arguments
echo "🚀 Launching agent..."
echo "Arguments: $*"
echo ""

python agent/agent.py "$@"

echo ""
echo "✅ Execution complete!"
echo "📊 Check results in: $PROJECT_ROOT/out/"
#!/bin/bash
# Quick test sequence for directory dependency fix (Issue #3)

set -e

echo "======================================================================"
echo "Test Sequence for Issue #3: Directory Dependencies in Elyra Pipelines"
echo "======================================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Navigate to elyra root
cd "$(dirname "$0")/.."

echo "${BLUE}Test 1: Running unit test for directory validation${NC}"
echo "----------------------------------------------------------------------"
python -m pytest elyra/tests/pipeline/test_validation.py::test_validate_filepath_with_directory -v
echo ""
echo "${GREEN}✓ Unit test passed${NC}"
echo ""

echo "${BLUE}Test 2: Running standalone validation test${NC}"
echo "----------------------------------------------------------------------"
python test_directory_deps/test_validation.py
echo ""
echo "${GREEN}✓ Standalone validation test passed${NC}"
echo ""

echo "${BLUE}Test 3: Verifying test files exist${NC}"
echo "----------------------------------------------------------------------"
ls -la test_directory_deps/sample_data/
echo ""
echo "${GREEN}✓ Test data directory exists with sample files${NC}"
echo ""

echo "======================================================================"
echo "${GREEN}✅ All tests completed successfully!${NC}"
echo "======================================================================"
echo ""
echo "Next steps:"
echo "1. Open test_directory_deps/test_notebook.ipynb in JupyterLab"
echo "2. Create a pipeline and add the notebook as a node"
echo "3. In node properties, add 'test_directory_deps/sample_data' as a dependency"
echo "4. Verify no validation errors appear"
echo ""

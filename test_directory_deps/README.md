# Directory Dependency Test Suite

This test suite validates the fix for issue #3: allowing directories as dependencies in Elyra pipelines.

## Test Structure

```
test_directory_deps/
├── README.md (this file)
├── test_notebook.ipynb (sample notebook that will use the dependency)
├── sample_data/ (directory to use as dependency)
│   ├── config.json
│   ├── data.csv
│   └── utils.py
└── test_validation.py (validation test script)
```

## Quick Test Sequence

### 1. Run Unit Tests
```bash
# Run the new test that validates directory support
pytest elyra/tests/pipeline/test_validation.py::test_validate_filepath_with_directory -v
```

### 2. Manual Validation Test
```bash
# Run the standalone validation test
python test_directory_deps/test_validation.py
```

### 3. Visual Verification
- Open `test_notebook.ipynb` in JupyterLab
- Right-click → "Open With" → "Pipeline Editor"
- Check the node properties
- Verify `sample_data/` directory is listed in dependencies without validation errors

## Expected Results

✅ **Pass**: Directory dependencies are accepted without validation errors
✅ **Pass**: Binary file check only applies to files, not directories
✅ **Pass**: Backward compatibility - file dependencies still work
❌ **Fail**: Directory rejected with "invalidFilePath" error (pre-fix behavior)

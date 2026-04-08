# Quick Test Guide for Issue #3 Fix

## Summary
This branch fixes the bug where Elyra pipelines couldn't include directories as dependencies - only individual files were accepted. The validation now properly accepts directories when marked as dependencies.

## Quick Test Sequence

### Option 1: Run Existing Unit Tests (Recommended)
```bash
# Test the new directory validation functionality
pytest elyra/tests/pipeline/test_validation.py::test_validate_filepath_with_directory -v

# Run all validation tests to ensure no regression
pytest elyra/tests/pipeline/test_validation.py -v
```

### Option 2: Manual Integration Test

1. **Start JupyterLab with Elyra**
   ```bash
   jupyter lab
   ```

2. **Open the test notebook**
   - Navigate to `test_directory_deps/test_notebook.ipynb`

3. **Create a simple pipeline**
   - Create a new pipeline (File → New → Pipeline)
   - Drag the test notebook onto the canvas
   - Double-click the node to open properties

4. **Add directory dependency**
   - In the "File Dependencies" section
   - Click "Add" and enter: `sample_data`
   - **IMPORTANT**: Use `sample_data` (relative to notebook), NOT `test_directory_deps/sample_data`
   - **Expected**: No validation error (✅ this is the fix!)
   - **Before fix**: Would show "invalidFilePath" error (❌)

5. **Save and validate**
   - The pipeline should save without errors
   - The directory should appear in the dependencies list

### Option 3: Test with Real Pipeline Execution

```bash
# Create a runtime configuration (if not already done)
# Then run the pipeline with the directory dependency

# The pipeline should successfully package and send the entire
# sample_data directory to the execution environment
```

## What the Fix Changes

### Before (❌ Broken)
- User adds `my_folder/` as a dependency
- Validation fails: "Property has an invalid path to a file/dir"
- Workaround: List every file individually OR download at runtime

### After (✅ Fixed)  
- User adds `my_folder/` as a dependency
- Validation passes ✓
- Entire directory is included in the pipeline execution

## Test Files Included

```
test_directory_deps/
├── README.md              # Full documentation
├── QUICK_TEST.md          # This file - quick test guide
├── test_notebook.ipynb    # Sample notebook for testing
├── sample_data/           # Test directory dependency
│   ├── config.json       # Sample config file
│   ├── data.csv          # Sample data file
│   └── utils.py          # Sample Python module
├── test_validation.py    # Standalone test (requires full env)
└── run_tests.sh          # Automated test runner
```

## Verification Checklist

- [ ] Unit test `test_validate_filepath_with_directory` passes
- [ ] No regression in other validation tests  
- [ ] Directory can be added as dependency in UI without error
- [ ] Files still work as dependencies (backward compatibility)
- [ ] Binary files are handled correctly
- [ ] Relative and absolute paths both work

## Expected Test Output

When running the unit test, you should see:
```
test_validate_filepath_with_directory PASSED
```

This confirms:
1. ✓ Directories are rejected by default (allow_directory=False)
2. ✓ Directories are accepted when allow_directory=True  
3. ✓ Binary file check only applies to files, not directories
4. ✓ Backward compatibility maintained

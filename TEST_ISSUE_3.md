# Testing Issue #3: Directory Dependencies Fix

## What This Branch Fixes

**Issue**: [opendatahub-io/odh-ide-extensions#3](https://github.com/opendatahub-io/odh-ide-extensions/issues/3)  
**Problem**: Users couldn't include directories as dependencies in Elyra pipelines - validation would reject them even when the directories existed.

**Solution**: Modified `_validate_filepath()` to accept directories when `allow_directory=True`.

## Changes Made

1. **elyra/pipeline/validation.py**
   - Added `allow_directory` parameter to `_validate_filepath()` method
   - Updated validation logic to accept both files and directories
   - Fixed binary file check to only apply to files, not directories
   - Set `allow_directory=True` when validating node dependencies

2. **elyra/tests/pipeline/test_validation.py**  
   - Added comprehensive test: `test_validate_filepath_with_directory`
   - Tests directory rejection (default), acceptance (when enabled), and edge cases

3. **elyra/metadata/metadata_app.py**
   - Fixed `List` type import conflicts (List → ListType)

## Quick Test Commands

### Fastest: Run the New Unit Test
```bash
pytest elyra/tests/pipeline/test_validation.py::test_validate_filepath_with_directory -v
```

### Thorough: Run All Validation Tests
```bash
pytest elyra/tests/pipeline/test_validation.py -v
```

### Complete: Run Full Test Suite
```bash
make test-server
```

## Manual Testing (JupyterLab UI)

I've created a complete test setup in `test_directory_deps/`:

```
test_directory_deps/
├── QUICK_TEST.md          ← Start here for detailed instructions
├── test_notebook.ipynb    ← Use this in a pipeline
└── sample_data/           ← Add this directory as a dependency
    ├── config.json
    ├── data.csv  
    └── utils.py
```

**Steps**:
1. Open JupyterLab: `jupyter lab`
2. Create a new pipeline
3. Add `test_directory_deps/test_notebook.ipynb` as a node
4. In node properties → File Dependencies → Add: `test_directory_deps/sample_data`
5. ✅ Should save without validation errors

## Expected Behavior

### ✅ After Fix (Current Branch)
```python
# When validating dependencies
_validate_filepath(
    filename="my_data_folder/",
    allow_directory=True  # ← This is now set for dependencies
)
# Result: No validation error, directory accepted ✓
```

### ❌ Before Fix  
```python
# Same validation would fail
# Error: "Property has an invalid path to a file/dir or the file/dir does not exist"
```

## Test Coverage

The new test `test_validate_filepath_with_directory` validates:

1. **Scenario 1**: Directories are rejected by default (backward compatible)
2. **Scenario 2**: Directories are accepted when `allow_directory=True`  
3. **Scenario 3**: Binary file check only applies to files, not directories
4. **Scenario 4**: Files still work (backward compatibility)

## Verification Checklist

Before submitting PR, verify:

- [x] Unit tests pass
- [x] No regression in existing tests
- [x] Code follows project style (type hints, documentation)
- [x] Fix matches upstream Elyra solution
- [ ] Manual UI test confirms directories work as dependencies
- [ ] Pipeline execution test with directory dependency succeeds

## Related Files

- **Issue**: https://github.com/opendatahub-io/odh-ide-extensions/issues/3
- **Upstream**: https://github.com/elyra-ai/elyra/issues/3181  
- **Documentation**: https://elyra.readthedocs.io/en/stable/user_guide/best-practices-file-based-nodes.html#file-input

## Questions?

See `test_directory_deps/QUICK_TEST.md` for detailed testing instructions and examples.

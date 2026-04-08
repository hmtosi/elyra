# 🐛 Directory Dependency Archive Bug & Workaround

## The Issue

When you add a directory as a dependency, you're hitting a bug in the archiving code (`elyra/util/archive.py`):

1. **Validation**: ✅ Passes (your fix works!)
2. **Archiving**: ❌ Fails because directories aren't added to `matched_set`

## The Bug

In `archive.py` lines 75-76:
```python
elif not include_all and directory_in_list(tarinfo.name, filenames_set):
    return tarinfo  # ← Directory added to archive BUT NOT to matched_set!
```

But files (lines 91-95) DO get added to `matched_set`:
```python
if fnmatch.fnmatch(tarinfo.name, filename):
    matched_set.add(filename)  # ← Files are tracked
    return tarinfo
```

Later, line 128 checks:
```python
if len(filenames_set) > len(matched_set):
    raise FileNotFoundError(filenames_set - matched_set)
```

Result: `{'sample_data'}` is in `filenames_set` but NOT in `matched_set` → Error!

## Workaround #1: Enable "Include Subdirectories"

This is the **easiest fix**:

1. In JupyterLab, open your pipeline
2. Double-click the `test_notebook.ipynb` node
3. Find the **"Include Subdirectories"** checkbox
4. ✅ **Check it** (enable it)
5. Keep the dependency as `sample_data`
6. Save and run

When `recursive=True`, the archive code uses different logic that properly handles directories.

## Workaround #2: List Files Individually

Instead of `sample_data`, list each file:
```
sample_data/config.json
sample_data/data.csv  
sample_data/utils.py
```

This avoids the directory matching issue entirely.

## Workaround #3: Fix the Archive Code

Add this after line 76 in `elyra/util/archive.py`:

```python
elif not include_all and directory_in_list(tarinfo.name, filenames_set):
    # Add directory to matched_set if it matches exactly
    for filename in filenames_set:
        if fnmatch.fnmatch(tarinfo.name, filename):
            matched_set.add(filename)
            break
    return tarinfo
```

Then reinstall:
```bash
source .venv/bin/activate
pip install -e .
```

## Recommended Solution

**Use Workaround #1** (enable Include Subdirectories) for now. This is the intended way to include entire directories with their contents.

The validation fix you made IS working - it's just exposing a separate bug in the archiving code that was previously masked.

## Testing

After enabling "Include Subdirectories":

```bash
# Should work now!
# The directory and all its contents will be packaged
```

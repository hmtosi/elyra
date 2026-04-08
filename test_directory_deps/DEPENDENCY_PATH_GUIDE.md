# 📝 How to Specify Dependencies in Elyra Pipelines

## Important: Dependencies are Relative to the Notebook!

When you add a file or directory as a dependency in Elyra, the path is **resolved relative to the notebook's location**, not the pipeline root.

## Example

### Directory Structure
```
elyra/
├── my_pipeline.pipeline
└── notebooks/
    ├── my_notebook.ipynb
    └── data/
        ├── config.json
        └── input.csv
```

### ✅ Correct Dependency Path

If `my_notebook.ipynb` needs the `data/` directory:

**In the UI, specify:**
```
data
```

**NOT:**
```
notebooks/data  ❌ This will double the path!
```

### Why?

Because Elyra automatically:
1. Gets the notebook's directory: `notebooks/`
2. Joins it with your dependency: `notebooks/` + `data/` = `notebooks/data/` ✅

If you specify `notebooks/data`, it becomes:
- `notebooks/` + `notebooks/data/` = `notebooks/notebooks/data/` ❌ (doubled!)

## For Our Test Case

### Directory Structure
```
elyra/
└── test_directory_deps/
    ├── test_notebook.ipynb
    └── sample_data/
        ├── config.json
        ├── data.csv
        └── utils.py
```

### ✅ Correct Dependency

In the node properties for `test_notebook.ipynb`, specify:
```
sample_data
```

**Result**: Resolves to `/home/htosi/elyra/test_directory_deps/sample_data` ✅

### ❌ Wrong Dependency

Do NOT specify:
```
test_directory_deps/sample_data
```

**Result**: Would resolve to `/home/htosi/elyra/test_directory_deps/test_directory_deps/sample_data` ❌

## General Rules

1. **Same directory as notebook**: Just use the filename/dirname
   ```
   config.json
   data_folder
   ```

2. **Subdirectory of notebook**: Use relative path from notebook
   ```
   data/config.json
   models/trained_model.pkl
   ```

3. **Parent directory**: Use `../`
   ```
   ../shared_utils.py
   ../common_data/
   ```

4. **Sibling directory**: Use `../sibling_dir/`
   ```
   ../other_notebooks/helper.ipynb
   ```

## Pro Tip

Always think: "What's the path from my notebook to this file/directory?"
- **Not**: "What's the path from the pipeline root?"

# 🔧 Quick Fix for Your Error

## The Error You Saw

```
"value": "/home/htosi/elyra/test_directory_deps/test_directory_deps/sample_data"
                                              ↑ DUPLICATED ↑
```

## The Problem

You specified: `test_directory_deps/sample_data`

But dependencies are resolved **relative to the notebook's location**, so it got doubled!

## ✅ The Solution

Change the dependency from:
```
test_directory_deps/sample_data  ❌
```

To:
```
sample_data  ✅
```

## Why?

Your notebook is at: `test_directory_deps/test_notebook.ipynb`
- Elyra sees the notebook is in directory: `test_directory_deps/`
- You specify dependency: `sample_data`
- Result: `test_directory_deps/sample_data` ✅ Perfect!

## Try Again

1. Open your pipeline in JupyterLab
2. Double-click the `test_notebook.ipynb` node
3. In "File Dependencies", change `test_directory_deps/sample_data` to just `sample_data`
4. Save the pipeline
5. It should now validate successfully! 🎉

## Rule of Thumb

**Think**: "What's the path FROM my notebook TO the dependency?"
- Notebook is in: `test_directory_deps/`
- Dependency is in: `test_directory_deps/sample_data/`
- Relative path: Just `sample_data/` !

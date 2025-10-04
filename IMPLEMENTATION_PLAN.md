# cisTEM Modern Documentation System Implementation Plan

## Overview

This document outlines the implementation strategy for migrating cisTEM's documentation from Jupyter Book to a modern, LLM-friendly documentation system with automated C++ AST parsing, intelligent tagging, and bidirectional code-documentation linking.

**Timeline**: 4-6 weeks
**Approach**: Phased implementation with validation checkpoints
**Risk Level**: Low (feature branch, incremental rollout, comprehensive rollback strategies)

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Pre-Implementation Checklist](#pre-implementation-checklist)
3. [Phase 0: Pre-Setup & Validation](#phase-0-pre-setup--validation)
4. [Phase 1: Docker Environment Setup](#phase-1-docker-environment-setup)
5. [Phase 2: Documentation Repository Migration](#phase-2-documentation-repository-migration)
6. [Phase 3: Submodule Integration](#phase-3-submodule-integration)
7. [Phase 4: AST Parser Implementation](#phase-4-ast-parser-implementation)
8. [Phase 5: Metadata System & Auto-Documentation](#phase-5-metadata-system--auto-documentation)
9. [Phase 6: Tagging & Search System](#phase-6-tagging--search-system)
10. [Phase 7: LLM Optimization](#phase-7-llm-optimization)
11. [Phase 8: CI/CD Integration](#phase-8-cicd-integration)
12. [Rollback Procedures](#rollback-procedures)
13. [Success Criteria](#success-criteria)
14. [Monitoring & Maintenance](#monitoring--maintenance)
15. [Troubleshooting Guide](#troubleshooting-guide)

---

## Architecture Overview

### Core Components

- **AST-Based Code Analysis**: libclang/cppast for parsing C++ and CUDA code
- **Structured Documentation**: YAML frontmatter with rich metadata
- **Intelligent Tagging**: Hierarchical tags for scientific computing domains
- **LLM Optimization**: Token-aware chunking, embeddings, JSON schemas
- **Automated Pipeline**: GitHub Actions for continuous documentation updates

### Technology Stack

- **Static Site Generator**: MkDocs with Material theme
- **C++ Parsing**: libclang-14 / cppast
- **Container**: Ubuntu 22.04 Docker with Python 3.10+ venv at `/opt/venv`
- **Search**: JSON index with optional Elasticsearch upgrade path
- **CI/CD**: GitHub Actions with matrix builds

### Repository Structure

```
cisTEM/
├── src/                    # C++ source code
├── docs/                   # Documentation submodule
│   ├── initial_jupyter_book_impl/  # Preserved original docs
│   ├── api/               # Auto-generated API docs
│   ├── tutorials/         # Manual tutorials
│   ├── llm/              # LLM-optimized outputs
│   ├── scripts/          # Documentation tools
│   │   ├── parse_cpp_ast.py
│   │   ├── generate_docs.py
│   │   ├── build_index.py
│   │   └── update_tags.py
│   ├── index.json        # Code-to-doc mappings
│   └── mkdocs.yml        # Site configuration
└── .github/
    └── workflows/
        └── documentation.yml
```

---

## Pre-Implementation Checklist

Before starting, ensure you have:

- [ ] Git credentials configured
- [ ] Docker installed and running
- [ ] Access to documentation repository
- [ ] At least 20GB free disk space
- [ ] Python 3.10+ available locally
- [ ] Backup of current documentation

---

## Phase 0: Pre-Setup & Validation

**Duration**: 2-3 hours
**Risk Level**: Low

### Steps

1. **Create feature branch**
   ```bash
   git checkout -b feature/new-documentation-system
   git push -u origin feature/new-documentation-system
   ```

2. **Verify documentation repository access**
   ```bash
   git ls-remote https://github.com/[your-username]/[docs-repo].git
   ```

3. **Create full backup**
   ```bash
   tar -czf cistem_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
     --exclude=build --exclude=.git/objects .
   ```

### Validation Checkpoint

```bash
# Verify branch
git branch --show-current  # Should show: feature/new-documentation-system

# Verify clean state
git status  # Should show: nothing to commit

# Verify backup
ls -lh cistem_backup_*.tar.gz  # Should exist and be > 100MB
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Git credentials fail | Run `git config --global credential.helper store` |
| Insufficient disk space | Use `docker system prune -a` to free space |
| Can't create branch | Ensure you're on your fork, not upstream |

---

## Phase 1: Docker Environment Setup

**Duration**: 1-2 hours
**Risk Level**: Low

### Steps

1. **Create infrastructure directories**
   ```bash
   mkdir -p .claude/cache
   mkdir -p docs_build
   mkdir -p docs
   ```

2. **Create Docker configuration files**

   **install_documentation_deps.sh**:
   ```bash
   #!/bin/bash
   # Create virtual environment
   python3 -m venv /opt/venv
   source /opt/venv/bin/activate

   # Install documentation tools
   pip install --upgrade pip
   pip install mkdocs mkdocs-material mkdocstrings[python]
   pip install pyyaml jinja2 pygments

   # Install AST parsing tools
   apt-get update && apt-get install -y \
     libclang-14-dev \
     clang-14 \
     python3-clang-14

   pip install libclang pycparser cppast

   # Install LLM tools
   pip install tiktoken sentence-transformers
   ```

   **Dockerfile**:
   ```dockerfile
   FROM ubuntu:22.04

   # Set environment for venv
   ENV VIRTUAL_ENV=/opt/venv
   ENV PATH="$VIRTUAL_ENV/bin:$PATH"

   # Install base dependencies
   RUN apt-get update && apt-get install -y \
     python3.10 python3.10-venv python3-pip \
     git curl wget build-essential

   # Copy and run installation script
   COPY install_documentation_deps.sh /tmp/
   RUN chmod +x /tmp/install_documentation_deps.sh && \
       /tmp/install_documentation_deps.sh

   WORKDIR /workspace
   ```

3. **Build container**
   ```bash
   docker build -t cistem-docs .
   ```

### Validation Checkpoint

```bash
# Test 1: Container exists
docker images | grep cistem-docs

# Test 2: Python environment
docker run --rm cistem-docs python --version
# Expected: Python 3.10.x

# Test 3: Virtual environment
docker run --rm cistem-docs sh -c "echo \$VIRTUAL_ENV"
# Expected: /opt/venv

# Test 4: libclang available
docker run --rm cistem-docs python -c \
  "import clang.cindex; print('libclang loaded successfully')"

# Test 5: MkDocs installed
docker run --rm cistem-docs mkdocs --version
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| libclang not found | Install specific version: `libclang-14-dev` |
| Port conflict | Change port in docker-compose.yml |
| Build fails on ARM Mac | Add `--platform linux/amd64` to docker build |

---

## Phase 2: Documentation Repository Migration

**Duration**: 1 hour
**Risk Level**: Medium

### Steps

1. **Clone existing documentation repository**
   ```bash
   git clone https://github.com/[your-username]/[docs-repo] /tmp/docs-migration
   cd /tmp/docs-migration
   ```

2. **Run migration script**
   ```bash
   #!/bin/bash
   # migrate_docs_repo.sh

   # Preserve existing Jupyter Book implementation
   mkdir -p initial_jupyter_book_impl
   git mv !(initial_jupyter_book_impl) initial_jupyter_book_impl/ 2>/dev/null || true

   # Create new structure
   mkdir -p api tutorials llm scripts .ast_cache

   # Create MkDocs configuration
   cat > mkdocs.yml << 'EOF'
   site_name: cisTEM Documentation
   theme:
     name: material
     features:
       - navigation.tabs
       - navigation.sections
       - navigation.expand

   nav:
     - Home: index.md
     - API Reference: api/
     - Tutorials: tutorials/
     - LLM Interface: llm/

   plugins:
     - search
     - mkdocstrings:
         handlers:
           python:
             paths: [src]
   EOF

   # Commit changes
   git add -A
   git commit -m "Migrate to new documentation system, preserve Jupyter Book in initial_jupyter_book_impl/"
   ```

3. **Push to repository**
   ```bash
   git push origin main
   ```

### Validation Checkpoint

```bash
# Test directory structure
tree -L 2
# Should show new structure with initial_jupyter_book_impl/

# Test MkDocs configuration
mkdocs build --strict
# Should build (may have warnings initially)

# Test old content preserved
ls initial_jupyter_book_impl/_config.yml
# Should exist
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Git mv fails | Use `find . -maxdepth 1 ! -name initial_jupyter_book_impl -exec mv {} initial_jupyter_book_impl/ \;` |
| MkDocs strict mode fails | Remove `--strict` initially, fix warnings incrementally |
| Large repo size | Consider `git filter-branch` to reduce history |

---

## Phase 3: Submodule Integration

**Duration**: 30 minutes
**Risk Level**: Low

### Steps

1. **Add documentation as submodule**
   ```bash
   cd /workspaces/cisTEM
   git submodule add https://github.com/[your-username]/[docs-repo] docs
   git submodule update --init --recursive
   ```

2. **Configure submodule**
   ```bash
   cd docs
   git checkout main
   git pull origin main
   cd ..
   ```

3. **Create helper script**
   ```python
   # regenerate_submodule.py
   import subprocess
   import sys

   def setup_submodule(repo_url):
       # Check for existing submodule
       result = subprocess.run(['git', 'submodule', 'status'],
                             capture_output=True, text=True)
       if 'docs' in result.stdout:
           print("Submodule already exists, updating...")
           subprocess.run(['git', 'submodule', 'update', '--init', '--recursive'])
       else:
           print(f"Adding submodule from {repo_url}")
           subprocess.run(['git', 'submodule', 'add', repo_url, 'docs'])
           subprocess.run(['git', 'submodule', 'update', '--init'])

       print("Submodule setup complete!")

   if __name__ == "__main__":
       repo_url = sys.argv[1] if len(sys.argv) > 1 else input("Enter docs repo URL: ")
       setup_submodule(repo_url)
   ```

### Validation Checkpoint

```bash
# Test 1: Submodule registered
git submodule status
# Should show docs submodule

# Test 2: Can update submodule
cd docs && git fetch && cd ..
# Should complete without errors

# Test 3: Docker can access
docker run --rm -v $(pwd):/workspace cistem-docs ls -la /workspace/docs
# Should list docs contents
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Submodule dirty | `cd docs && git checkout . && cd ..` |
| Permission denied | Check SSH keys: `ssh -T git@github.com` |
| Detached HEAD | `cd docs && git checkout main && cd ..` |

---

## Phase 4: AST Parser Implementation

**Duration**: 2-3 days
**Risk Level**: High

### Core Features Required

- Parse C++ classes, functions, templates
- Handle CUDA kernels (`__global__`, `__device__`)
- Extract documentation comments
- Cache parsed results
- Support incremental updates

### Implementation Steps

1. **Create base parser**
   ```python
   # docs/scripts/parse_cpp_ast.py
   import clang.cindex
   import hashlib
   import json
   import os
   from pathlib import Path

   class CppASTParser:
       def __init__(self, cache_dir=".ast_cache"):
           self.cache_dir = Path(cache_dir)
           self.cache_dir.mkdir(exist_ok=True)

           # Initialize libclang
           clang.cindex.Config.set_library_file('/usr/lib/llvm-14/lib/libclang.so')
           self.index = clang.cindex.Index.create()

       def parse_file(self, filepath):
           # Check cache
           file_hash = self._get_file_hash(filepath)
           cache_file = self.cache_dir / f"{file_hash}.json"

           if cache_file.exists():
               with open(cache_file) as f:
                   return json.load(f)

           # Parse with libclang
           tu = self.index.parse(filepath, args=[
               '-std=c++17',
               '-I/usr/include',
               '-I./include',
               '-DHAVE_MKL',  # cisTEM specific
           ])

           # Extract information
           result = {
               'file': str(filepath),
               'hash': file_hash,
               'classes': [],
               'functions': [],
               'templates': [],
               'cuda_kernels': []
           }

           self._extract_ast_info(tu.cursor, result)

           # Save to cache
           with open(cache_file, 'w') as f:
               json.dump(result, f, indent=2)

           return result
   ```

2. **Add CUDA support**
   ```python
   def _extract_cuda_info(self, cursor, result):
       """Extract CUDA-specific information"""
       if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL:
           # Check for CUDA attributes
           for token in cursor.get_tokens():
               if token.spelling in ['__global__', '__device__', '__host__']:
                   kernel_info = {
                       'name': cursor.spelling,
                       'type': token.spelling,
                       'params': [p.spelling for p in cursor.get_arguments()],
                       'location': f"{cursor.location.file}:{cursor.location.line}"
                   }
                   result['cuda_kernels'].append(kernel_info)
                   break
   ```

3. **Handle templates**
   ```python
   def _extract_template_info(self, cursor, result):
       """Extract template specializations"""
       if cursor.kind == clang.cindex.CursorKind.CLASS_TEMPLATE:
           template_info = {
               'name': cursor.spelling,
               'parameters': [],
               'specializations': []
           }

           # Extract template parameters
           for child in cursor.get_children():
               if child.kind == clang.cindex.CursorKind.TEMPLATE_TYPE_PARAMETER:
                   template_info['parameters'].append(child.spelling)

           result['templates'].append(template_info)
   ```

### Validation Checkpoint

```python
# test_ast_parser.py
def test_basic_parsing():
    parser = CppASTParser()
    result = parser.parse_file("src/core/image.h")
    assert "Image" in [c['name'] for c in result['classes']]

def test_template_parsing():
    result = parser.parse_file("src/core/tensor.h")
    assert any(t['name'] == 'Tensor' for t in result['templates'])

def test_cuda_parsing():
    result = parser.parse_file("src/gpu/kernels.cu")
    assert len(result['cuda_kernels']) > 0
    assert any(k['type'] == '__global__' for k in result['cuda_kernels'])

def test_cache_performance():
    import time
    # First parse (no cache)
    start = time.time()
    parser.parse_file("large_file.cpp")
    first_time = time.time() - start

    # Second parse (cached)
    start = time.time()
    parser.parse_file("large_file.cpp")
    cached_time = time.time() - start

    assert cached_time < first_time * 0.1  # 10x speedup
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| libclang can't find headers | Set `CPLUS_INCLUDE_PATH` environment variable |
| Template recursion | Add `max_depth` parameter to limit recursion |
| Memory explosion | Process files in batches, clear cache between |
| CUDA files not recognized | Add `.cu` extension handling, use nvcc flags |

### Performance Optimization

- **Incremental parsing**: Only parse changed files
- **Parallel processing**: Use multiprocessing for large codebases
- **Smart caching**: Hash file contents, not timestamps
- **Memory management**: Process in chunks, use generators

---

## Phase 5: Metadata System & Auto-Documentation

**Duration**: 2 days
**Risk Level**: Medium

### Metadata Schema

```yaml
# Scientific computing specific metadata
---
title: FFT3D Class
source_file: src/core/fft3d.cpp
line_range: [45, 580]
scientific_metadata:
  algorithm_type: "Fast Fourier Transform"
  computational_complexity: "O(n log n)"
  memory_footprint: "2 * input_size"
  numerical_stability: "double precision recommended"
  parallelization: ["MKL", "CUDA"]
  typical_input_size: "512x512x512 voxels"
performance_metadata:
  benchmarks:
    - config: "512^3, single precision, RTX 3090"
      throughput: "245 transforms/sec"
    - config: "512^3, double precision, CPU"
      throughput: "12 transforms/sec"
dependencies:
  runtime: ["Intel MKL", "CUDA 11.8+"]
  compile_time: ["fftw3.h", "cufft.h"]
tags:
  - processing/fourier/fft
  - optimization/gpu/cuda
  - core/transforms
llm_metadata:
  summary: "GPU-accelerated 3D FFT implementation"
  token_count: 4500
  chunk_ids: ["fft3d_overview", "fft3d_implementation"]
---
```

### Implementation Steps

1. **Create metadata extractor**
   ```python
   # docs/scripts/extract_metadata.py
   class MetadataExtractor:
       def extract(self, ast_data, source_file):
           metadata = {
               'title': self._extract_title(ast_data),
               'source_file': source_file,
               'line_range': self._get_line_range(ast_data),
               'scientific_metadata': self._extract_scientific(ast_data),
               'performance_metadata': self._extract_performance(source_file),
               'dependencies': self._extract_dependencies(ast_data),
               'tags': self._generate_tags(ast_data, source_file)
           }
           return metadata

       def _extract_scientific(self, ast_data):
           # Parse comments for algorithm complexity
           # Analyze memory allocations
           # Detect parallelization patterns
           pass
   ```

2. **Generate documentation pages**
   ```python
   # docs/scripts/generate_docs.py
   def generate_documentation(ast_data, metadata):
       template = load_template('api_doc.md.jinja')

       doc_content = template.render(
           metadata=metadata,
           classes=ast_data['classes'],
           functions=ast_data['functions'],
           examples=find_examples(metadata['source_file'])
       )

       output_path = Path('docs/api') / metadata['source_file'].replace('.cpp', '.md')
       output_path.parent.mkdir(parents=True, exist_ok=True)
       output_path.write_text(doc_content)
   ```

### Validation Checkpoint

```bash
# Test metadata extraction
python docs/scripts/test_metadata.py
# Should extract complexity, memory, dependencies

# Check generated documentation
ls docs/api/**/*.md | wc -l
# Should match number of source files

# Verify cross-references
grep -r "line_range" docs/api/ | head -5
# Should show line number references
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Can't extract from macros | Use preprocessor: `cpp -E file.cpp` |
| Missing dependencies | Parse CMakeLists.txt and configure.ac |
| Performance data unavailable | Create benchmark suite first |

---

## Phase 6: Tagging & Search System

**Duration**: 1 day
**Risk Level**: Low

### Tag Hierarchy

```
cisTEM Tags:
├── processing/
│   ├── fourier/
│   │   ├── fft
│   │   └── ifft
│   ├── filtering/
│   │   ├── gaussian
│   │   ├── butterworth
│   │   └── median
│   └── reconstruction/
│       ├── backprojection
│       └── iterative
├── optimization/
│   ├── gpu/
│   │   ├── cuda
│   │   └── opencl
│   └── simd/
│       ├── avx2
│       └── avx512
└── data/
    ├── formats/
    │   ├── mrc
    │   └── tiff
    └── structures/
        ├── image
        └── volume
```

### Implementation

1. **Auto-tagging system**
   ```python
   # docs/scripts/update_tags.py
   class AutoTagger:
       def __init__(self):
           self.tag_rules = {
               'namespace': {
                   'gpu': ['optimization/gpu/cuda'],
                   'core': ['core/fundamental']
               },
               'filename': {
                   'cuda': ['optimization/gpu/cuda'],
                   'test': ['testing'],
                   'benchmark': ['performance']
               },
               'content': {
                   'FFT': ['processing/fourier/fft'],
                   'filter': ['processing/filtering']
               }
           }

       def generate_tags(self, ast_data, filepath):
           tags = set()

           # From namespace
           namespace = self._extract_namespace(ast_data)
           if namespace in self.tag_rules['namespace']:
               tags.update(self.tag_rules['namespace'][namespace])

           # From filename
           filename = Path(filepath).name.lower()
           for pattern, tag_list in self.tag_rules['filename'].items():
               if pattern in filename:
                   tags.update(tag_list)

           # From content
           content_str = str(ast_data).lower()
           for pattern, tag_list in self.tag_rules['content'].items():
               if pattern.lower() in content_str:
                   tags.update(tag_list)

           return sorted(list(tags))
   ```

2. **Build search index**
   ```python
   # docs/scripts/build_index.py
   def build_search_index():
       index = {
           'version': '1.0',
           'timestamp': datetime.now().isoformat(),
           'files': [],
           'tags': {},
           'cross_references': {}
       }

       for doc_file in Path('docs/api').rglob('*.md'):
           metadata = extract_frontmatter(doc_file)

           file_entry = {
               'path': str(doc_file),
               'title': metadata['title'],
               'tags': metadata['tags'],
               'source': metadata['source_file'],
               'line_range': metadata['line_range']
           }

           index['files'].append(file_entry)

           # Build tag index
           for tag in metadata['tags']:
               if tag not in index['tags']:
                   index['tags'][tag] = []
               index['tags'][tag].append(str(doc_file))

       # Save index
       with open('docs/index.json', 'w') as f:
           json.dump(index, f, indent=2)
   ```

### Validation Checkpoint

```bash
# Test tagging
cat docs/index.json | jq '.files[0].tags'
# Should show hierarchical tags

# Test search
python -c "
import json
with open('docs/index.json') as f:
    index = json.load(f)
    gpu_files = index['tags'].get('optimization/gpu/cuda', [])
    print(f'Found {len(gpu_files)} GPU-accelerated files')
"
```

---

## Phase 7: LLM Optimization

**Duration**: 2 days
**Risk Level**: Medium

### Features

1. **Token counting and chunking**
   ```python
   # docs/scripts/llm_optimizer.py
   import tiktoken

   class LLMOptimizer:
       def __init__(self, model="gpt-4"):
           self.encoder = tiktoken.encoding_for_model(model)
           self.max_tokens = 8000  # Leave room for system prompt

       def count_tokens(self, text):
           return len(self.encoder.encode(text))

       def smart_chunk(self, content, metadata):
           chunks = []
           current_chunk = {
               'content': '',
               'tokens': 0,
               'metadata': metadata,
               'includes': []
           }

           # Split by logical boundaries (classes, functions)
           sections = self._split_by_sections(content)

           for section in sections:
               section_tokens = self.count_tokens(section['content'])

               if current_chunk['tokens'] + section_tokens > self.max_tokens:
                   # Save current chunk
                   chunks.append(current_chunk)
                   # Start new chunk
                   current_chunk = {
                       'content': section['content'],
                       'tokens': section_tokens,
                       'metadata': metadata,
                       'includes': [section['type']]
                   }
               else:
                   # Add to current chunk
                   current_chunk['content'] += '\n\n' + section['content']
                   current_chunk['tokens'] += section_tokens
                   current_chunk['includes'].append(section['type'])

           if current_chunk['content']:
               chunks.append(current_chunk)

           return chunks
   ```

2. **Generate embeddings**
   ```python
   from sentence_transformers import SentenceTransformer

   class EmbeddingGenerator:
       def __init__(self):
           self.model = SentenceTransformer('all-MiniLM-L6-v2')

       def generate_embeddings(self, chunks):
           embeddings = []

           for chunk in chunks:
               # Create semantic description
               description = f"{chunk['metadata']['title']} {' '.join(chunk['includes'])}"

               # Generate embedding
               embedding = self.model.encode(description)

               embeddings.append({
                   'chunk_id': chunk['id'],
                   'embedding': embedding.tolist(),
                   'metadata': chunk['metadata']
               })

           return embeddings
   ```

3. **Create LLM-friendly JSON schemas**
   ```python
   def generate_llm_json(ast_data, metadata):
       llm_json = {
           'schema_version': '1.0',
           'module': metadata['source_file'],
           'summary': metadata['llm_metadata']['summary'],
           'classes': [],
           'functions': [],
           'examples': [],
           'token_count': 0
       }

       # Add structured data
       for cls in ast_data['classes']:
           llm_json['classes'].append({
               'name': cls['name'],
               'methods': [m['name'] for m in cls['methods']],
               'description': cls.get('doc', ''),
               'complexity': cls.get('complexity', 'O(n)')
           })

       # Calculate tokens
       llm_json['token_count'] = count_tokens(json.dumps(llm_json))

       # Save
       output_path = Path('docs/llm') / f"{metadata['source_file']}.json"
       output_path.parent.mkdir(parents=True, exist_ok=True)

       with open(output_path, 'w') as f:
           json.dump(llm_json, f, indent=2)
   ```

### Validation Checkpoint

```python
# Test token counting
text = "class Image { void Process(); };"
tokens = optimizer.count_tokens(text)
assert tokens < 20

# Test chunking
chunks = optimizer.smart_chunk(large_file_content, metadata)
assert all(c['tokens'] <= 8000 for c in chunks)

# Test embeddings
embeddings = generator.generate_embeddings(chunks)
assert len(embeddings[0]['embedding']) == 384  # all-MiniLM dimension

# Test similarity search
query_embedding = model.encode("FFT processing")
similar = find_most_similar(query_embedding, embeddings, top_k=5)
assert 'fft' in similar[0]['metadata']['title'].lower()
```

---

## Phase 8: CI/CD Integration

**Duration**: 1 day
**Risk Level**: Low

### GitHub Actions Workflow

```yaml
# .github/workflows/documentation.yml
name: Update Documentation

on:
  push:
    branches: [main, feature/new-documentation-system]
    paths:
      - 'src/**'
      - 'include/**'
      - 'docs/**'

jobs:
  update-docs:
    runs-on: ubuntu-22.04

    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Cache Docker layers
      uses: actions/cache@v3
      with:
        path: /tmp/.buildx-cache
        key: ${{ runner.os }}-buildx-${{ github.sha }}
        restore-keys: |
          ${{ runner.os }}-buildx-

    - name: Build documentation container
      run: |
        docker build -t cistem-docs \
          --cache-from type=local,src=/tmp/.buildx-cache \
          --cache-to type=local,dest=/tmp/.buildx-cache-new \
          .

    - name: Parse changed files
      run: |
        # Get changed C++ files
        CHANGED_FILES=$(git diff --name-only HEAD^ HEAD | grep -E '\.(cpp|h|cu)$' || true)

        if [ -n "$CHANGED_FILES" ]; then
          docker run --rm \
            -v ${{ github.workspace }}:/workspace \
            cistem-docs \
            python docs/scripts/parse_cpp_ast.py $CHANGED_FILES
        fi

    - name: Generate documentation
      run: |
        docker run --rm \
          -v ${{ github.workspace }}:/workspace \
          cistem-docs \
          python docs/scripts/generate_docs.py

    - name: Build MkDocs site
      run: |
        docker run --rm \
          -v ${{ github.workspace }}:/workspace \
          cistem-docs \
          mkdocs build --strict

    - name: Run documentation tests
      run: |
        docker run --rm \
          -v ${{ github.workspace }}:/workspace \
          cistem-docs \
          pytest docs/tests/

    - name: Deploy to GitHub Pages
      if: github.ref == 'refs/heads/main'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./site
```

### Build Matrix for Different Configurations

```yaml
strategy:
  matrix:
    config:
      - name: "MKL + CUDA"
        defines: "-DHAVE_MKL -DHAVE_CUDA"
      - name: "FFTW + CPU"
        defines: "-DHAVE_FFTW"
      - name: "Debug"
        defines: "-DDEBUG -DHAVE_MKL"
```

### Validation Checkpoint

```bash
# Push test commit
git commit --allow-empty -m "test: trigger docs build"
git push

# Monitor GitHub Actions
# Should see:
# ✓ Parse changed files
# ✓ Generate documentation
# ✓ Build MkDocs site
# ✓ Run tests
# ✓ Deploy (if on main)
```

---

## Rollback Procedures

### Global Rollback

At any point, restore from backup:
```bash
# Stash current changes
git stash

# Return to main branch
git checkout main

# Restore from backup
tar -xzf cistem_backup_[timestamp].tar.gz

# Remove failed branch
git branch -D feature/new-documentation-system
```

### Phase-Specific Rollbacks

| Phase | Rollback Command |
|-------|------------------|
| Docker | `docker system prune -a && rm -rf .claude/ docs_build/` |
| Docs Migration | `cd docs && git reset --hard HEAD~1 && git push --force` |
| Submodule | `git submodule deinit -f docs && git rm -f docs` |
| AST Parser | `rm -rf docs/scripts/parse_*.py .ast_cache/` |
| Features | Set feature flags: `ENABLE_FEATURE=false` |

---

## Success Criteria

### Week 1: Minimum Viable Documentation
- [ ] Docker environment operational
- [ ] MkDocs serving basic documentation
- [ ] One module fully documented (e.g., `src/core/tensor/`)
- [ ] Basic AST parsing extracts classes and methods
- [ ] Search functionality works

### Week 4: Full Implementation
- [ ] 90% of public APIs documented
- [ ] AST parsing completes in < 5 minutes
- [ ] LLM can query via JSON API
- [ ] Zero broken cross-references
- [ ] Documentation updates within 10 minutes of code push
- [ ] All CUDA kernels documented
- [ ] Performance benchmarks included

### Production Ready Checklist
- [ ] All tests passing
- [ ] Documentation coverage > 80%
- [ ] Search returns relevant results
- [ ] LLM JSON schemas validated
- [ ] CI/CD pipeline stable
- [ ] Monitoring dashboard operational

---

## Monitoring & Maintenance

### Daily Health Check Script

```bash
#!/bin/bash
# docs/scripts/health_check.sh

echo "=== Documentation System Health Check ==="
echo "Date: $(date)"
echo "----------------------------------------"

# Check AST cache freshness
STALE=$(find .ast_cache -mtime +1 -type f | wc -l)
echo "Stale cache files: $STALE"

# Check for broken links
BROKEN=$(mkdocs build 2>&1 | grep -c "WARNING.*404" || echo "0")
echo "Broken links: $BROKEN"

# Check memory usage
docker stats --no-stream --format "Memory usage: {{.MemUsage}}" cistem-docs

# Check index size
echo "Index size: $(du -sh docs/index.json | cut -f1)"
echo "LLM chunks: $(ls docs/llm/*.json | wc -l)"

# Check last build time
if [ -f .last_build ]; then
    echo "Last successful build: $(cat .last_build)"
fi

# Performance metrics
echo ""
echo "=== Performance Metrics ==="
if [ -f .metrics.json ]; then
    cat .metrics.json | jq '.'
fi
```

### Weekly Maintenance Tasks

1. **Clear and rebuild AST cache**
   ```bash
   rm -rf .ast_cache/*
   python docs/scripts/parse_cpp_ast.py --full-rebuild
   ```

2. **Update dependencies**
   ```bash
   docker run --rm cistem-docs pip list --outdated
   docker build --no-cache -t cistem-docs .
   ```

3. **Optimize search index**
   ```bash
   python docs/scripts/optimize_index.py
   ```

4. **Review slow queries**
   ```bash
   grep "SLOW_QUERY" docs/logs/*.log | tail -20
   ```

5. **Backup documentation database**
   ```bash
   tar -czf docs_backup_$(date +%Y%m%d).tar.gz docs/
   ```

### Performance Monitoring Metrics

Track these metrics over time:

```python
metrics = {
    'ast_parse_time': [],      # Target: < 5 minutes
    'index_build_time': [],    # Target: < 1 minute
    'memory_usage': [],        # Target: < 4GB
    'cache_hit_rate': [],      # Target: > 80%
    'failed_builds': [],       # Target: 0
    'doc_coverage': [],        # Target: > 90%
    'avg_page_tokens': [],    # Target: < 8000
    'search_latency': []       # Target: < 100ms
}
```

### Alert Thresholds

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| AST parse time | > 8 min | > 15 min | Check template recursion |
| Memory usage | > 6GB | > 8GB | Clear cache, restart |
| Cache hit rate | < 60% | < 40% | Review change patterns |
| Failed builds | > 1/day | > 3/day | Check libclang compatibility |
| Search latency | > 200ms | > 500ms | Optimize index structure |

---

## Troubleshooting Guide

### Common Issues and Solutions

#### AST Parsing Issues

**Problem**: Template instantiation causes infinite recursion
```bash
# Symptom
Segmentation fault during AST parsing
```
**Solution**:
```python
# Add recursion limit
parser.max_template_depth = 3
```

**Problem**: Can't find CUDA headers
```bash
# Symptom
fatal error: 'cuda_runtime.h' file not found
```
**Solution**:
```bash
export CUDA_PATH=/usr/local/cuda
export CPLUS_INCLUDE_PATH=$CUDA_PATH/include:$CPLUS_INCLUDE_PATH
```

#### Docker Issues

**Problem**: Container runs out of memory
```bash
# Symptom
Container killed with exit code 137
```
**Solution**:
```yaml
# docker-compose.yml
services:
  docs:
    mem_limit: 8g
    memswap_limit: 8g
```

#### Search/Index Issues

**Problem**: Search returns no results
```bash
# Debug
cat docs/index.json | jq '.files | length'
# If 0, index build failed
```
**Solution**:
```bash
# Rebuild index
python docs/scripts/build_index.py --verbose --debug
```

#### LLM Issues

**Problem**: Token count exceeds limit
```python
# Symptom
Token count: 12543 exceeds max: 8000
```
**Solution**:
```python
# Adjust chunking strategy
optimizer.max_tokens = 4000  # More aggressive chunking
```

### Debug Mode

Enable comprehensive debugging:
```bash
# Set environment variables
export DOCS_DEBUG=1
export DOCS_VERBOSE=1
export AST_PARSER_DEBUG=1

# Run with debug output
docker run --rm \
  -e DOCS_DEBUG=1 \
  -v $(pwd):/workspace \
  cistem-docs \
  python docs/scripts/parse_cpp_ast.py --debug src/core/image.h 2>&1 | tee debug.log
```

### Getting Help

1. **Check logs**: `docs/logs/[date].log`
2. **Run diagnostics**: `./docs/scripts/diagnose.sh`
3. **Search issues**: Project GitHub issues
4. **Community**: cisTEM Discord/Slack

---

## Quick Reference

### Essential Commands

```bash
# Start development environment
docker-compose up -d

# Update documentation after code changes
docker exec cistem-docs make update-docs

# View documentation locally
open http://localhost:8000

# Run tests
docker exec cistem-docs pytest docs/tests/

# Check system health
docker exec cistem-docs ./docs/scripts/health_check.sh

# Full rebuild (nuclear option)
docker-compose down
docker system prune -a
docker-compose build --no-cache
docker-compose up
```

### File Locations

| Component | Location |
|-----------|----------|
| AST cache | `.ast_cache/` |
| Generated docs | `docs/api/` |
| LLM outputs | `docs/llm/` |
| Search index | `docs/index.json` |
| Logs | `docs/logs/` |
| Scripts | `docs/scripts/` |
| Tests | `docs/tests/` |

### Configuration Files

| File | Purpose |
|------|---------|
| `mkdocs.yml` | MkDocs configuration |
| `docker-compose.yml` | Container orchestration |
| `.github/workflows/documentation.yml` | CI/CD pipeline |
| `docs/config.yaml` | Documentation system config |

---

## Next Steps

1. **Week 1**: Complete Phases 0-3, establish foundation
2. **Week 2**: Implement AST parser (Phase 4)
3. **Week 3**: Add metadata and tagging (Phases 5-6)
4. **Week 4**: LLM optimization and CI/CD (Phases 7-8)
5. **Week 5**: Testing, optimization, and polish
6. **Week 6**: Deploy to production, monitor

## Notes

This is a living document. Update it as you learn and refine the system.

Last Updated: [Current Date]
Version: 1.0.0